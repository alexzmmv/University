'use client';
import { useState, useEffect, useRef, useCallback } from 'react';
import { Footer } from "@/app/components/Footer";
import axios from 'axios';
import { FaCloudUploadAlt, FaTrash, FaPlay } from 'react-icons/fa';
import { Header } from '../components/homeWindow/Header';
import { useAuth } from '../utils/AuthContext';
import { useApi, API_URL } from '../utils/ApiUrlContext';
import ProtectedRoute from '../components/auth/ProtectedRoute';

const CHUNK_SIZE = 1024 * 1024 * 2; // 2MB chunks

function MyBrews() {
    const { user } = useAuth();
    const { apiUrl, fetchWithAuth } = useApi();
    const [isUploading, setIsUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [videos, setVideos] = useState([]);
    const [error, setError] = useState('');
    const [activeVideo, setActiveVideo] = useState(null);
    const [isCancelled, setIsCancelled] = useState(false);
    const [protectedData, setProtectedData] = useState(null);
    const fileInputRef = useRef(null);
    const [uploadId, setUploadId] = useState(null);

    const fetchProtectedData = useCallback(async () => {
        try {
            const response = await fetchWithAuth('protected', {
                method: 'GET',
            }, true); // requireAuth = true

            if (response.ok) {
                const data = await response.json();
                setProtectedData(data);
            }
        } catch (err) {
            console.error('Error fetching protected data:', err);
        }
    }, [fetchWithAuth]);

    const fetchVideos = useCallback(async () => {
        try {
            // Use the authenticated fetch for API calls
            const response = await fetchWithAuth('mybrews/videos', {
                method: 'GET'
            }, true);
            
            if (response.ok) {
                const data = await response.json();
                if (data && data.videos) {
                    setVideos(data.videos);
                }
            }
        } catch (error) {
            console.error('Error fetching videos:', error);
        }
    }, [fetchWithAuth]);

    // Fetch videos on component mount
    useEffect(() => {
        if (user) {
            fetchVideos();
            fetchProtectedData();
        }
    }, [user, fetchVideos, fetchProtectedData]);

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        // Reset error state
        setError('');
        
        if (!file.type.includes('video/')) {
            setError('Please select a video file');
            return;
        }
        
        if (file.size > 500 * 1024 * 1024) { // 500MB limit
            setError('File size exceeds the 500MB limit');
            return;
        }
        
        uploadFile(file);
    };

    const uploadFile = async (file) => {
        try {
            setIsUploading(true);
            setUploadProgress(0);
            setError('');
            setIsCancelled(false);
            
            // Step 1: Initialize the upload
            const formData = new FormData();
            formData.append('filename', file.name);
            formData.append('fileType', file.type);
            formData.append('fileSize', file.size);
            
            const initResponse = await fetchWithAuth('mybrews/videos/init', {
                method: 'POST',
                body: formData
            }, true);
            
            if (!initResponse.ok) {
                const errorData = await initResponse.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Failed to initialize upload');
            }
            
            const initData = await initResponse.json();
            const newUploadId = initData.uploadId;
            
            if (!newUploadId) {
                throw new Error('Invalid upload ID received from server');
            }
            
            // Store the upload ID
            setUploadId(newUploadId);
            // Also store in localStorage as a backup
            localStorage.setItem('currentUploadId', newUploadId);
            
            // Step 2: Upload the file in chunks
            const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
            let uploadedChunks = 0;
            const maxRetries = 3;
            
            for (let start = 0; start < file.size; start += CHUNK_SIZE) {
                // If upload was cancelled, stop the process
                if (isCancelled) {
                    console.log('Upload cancelled by user');
                    return;
                }
                
                const chunk = file.slice(start, start + CHUNK_SIZE);
                const chunkFormData = new FormData();
                chunkFormData.append('chunk', chunk);
                chunkFormData.append('uploadId', newUploadId);
                chunkFormData.append('partNumber', uploadedChunks + 1);
                
                let chunkUploaded = false;
                let retryCount = 0;
                
                // Attempt to upload chunk with retries
                while (!chunkUploaded && retryCount < maxRetries) {
                    try {
                        const chunkResponse = await fetchWithAuth('mybrews/videos/chunk', {
                            method: 'POST',
                            body: chunkFormData
                        }, true);
                        
                        if (chunkResponse.ok) {
                            chunkUploaded = true;
                        } else {
                            // Increment retry count and wait before retrying
                            retryCount++;
                            if (retryCount < maxRetries) {
                                await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
                                console.log(`Retrying chunk upload (${retryCount}/${maxRetries})`);
                            }
                        }
                    } catch (error) {
                        // Increment retry count and wait before retrying
                        retryCount++;
                        if (retryCount < maxRetries) {
                            await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
                            console.log(`Retrying chunk upload after error (${retryCount}/${maxRetries})`);
                        }
                    }
                }
                
                if (!chunkUploaded) {
                    throw new Error(`Failed to upload chunk ${uploadedChunks + 1} after ${maxRetries} attempts`);
                }
                
                uploadedChunks++;
                const progress = Math.round((uploadedChunks / totalChunks) * 100);
                setUploadProgress(progress);
            }
            
            // Step 3: Complete the upload
            const completeFormData = new FormData();
            completeFormData.append('uploadId', newUploadId);
            completeFormData.append('filename', file.name);
            
            const completeResponse = await fetchWithAuth('mybrews/videos/complete', {
                method: 'POST',
                body: completeFormData
            }, true);
            
            if (!completeResponse.ok) {
                throw new Error('Failed to complete upload');
            }
            
            const completeData = await completeResponse.json();
            if (completeData && completeData.video) {
                // Add the new video to our state
                setVideos(prevVideos => [...prevVideos, completeData.video]);
            }
            
            // Clear file input
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
            
            setError('');
            // Refetch videos to ensure we have the latest list
            fetchVideos();
        } catch (error) {
            console.error('Error uploading video:', error);
            setError(`Upload failed: ${error.message || 'Please try again'}`);
            
            // Attempt to clean up the failed upload
            try {
                if (newUploadId) {
                    await fetchWithAuth(`mybrews/videos/cancel/${newUploadId}`, {
                        method: 'POST'
                    }, true);
                    console.log('Cleaned up failed upload');
                }
            } catch (cleanupError) {
                console.error('Error cleaning up failed upload:', cleanupError);
            }
        } finally {
            setIsUploading(false);
            setUploadProgress(0);
            setUploadId(null);
            localStorage.removeItem('currentUploadId');
        }
    };
    
    const cancelUpload = async () => {
        setIsCancelled(true);
        setIsUploading(false);
        
        // Clear file input
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
        
        // Try to cancel the upload on the server using state first
        if (uploadId) {
            try {
                await fetchWithAuth(`mybrews/videos/cancel/${uploadId}`, {
                    method: 'POST'
                }, true);
                console.log('Cancelled upload on server');
            } catch (error) {
                console.error('Error cancelling upload on server:', error);
            }
        } else {
            // Fallback to localStorage if state is not available
            const storedUploadId = localStorage.getItem('currentUploadId');
            if (storedUploadId) {
                try {
                    await fetchWithAuth(`mybrews/videos/cancel/${storedUploadId}`, {
                        method: 'POST'
                    }, true);
                } catch (error) {
                    console.error('Error cancelling upload on server:', error);
                }
            }
        }
        
        // Clear upload ID
        setUploadId(null);
        localStorage.removeItem('currentUploadId');
    };

    const deleteVideo = async (videoId) => {
        try {
            const response = await fetchWithAuth(`mybrews/videos/${videoId}`, {
                method: 'DELETE'
            }, true);
            
            if (response.ok) {
                setVideos(videos.filter(video => video.id !== videoId));
                if (activeVideo?.id === videoId) {
                    setActiveVideo(null);
                }
            } else {
                throw new Error('Failed to delete video');
            }
        } catch (error) {
            console.error('Error deleting video:', error);
        }
    };

    const openVideoPlayer = (video) => {
        setActiveVideo(video);
    };

    const closeVideoPlayer = () => {
        setActiveVideo(null);
    };

    // Cleanup on unmount
    useEffect(() => {
        // Store the current values to use in cleanup function
        const currentUploadId = uploadId;
        const currentIsUploading = isUploading;
        // Use API_URL as fallback to avoid dependency on potentially changing apiUrl
        const currentApiUrl = apiUrl || API_URL;
        
        return () => {
            // If there's an active upload when component unmounts, try to cancel it
            if (currentIsUploading && currentUploadId) {
                const storedUploadId = currentUploadId || localStorage.getItem('currentUploadId');
                if (storedUploadId) {
                    // Use a simple fetch here since we're in cleanup and might not have access to hooks
                    fetch(`${currentApiUrl}mybrews/videos/cancel/${storedUploadId}`, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    }).catch(err => console.error('Failed to cancel upload during cleanup:', err));
                    
                    localStorage.removeItem('currentUploadId');
                }
            }
        };
    }, [/* empty dependency array to avoid re-creating the cleanup function */]);

    return (
        <div className="min-h-screen flex flex-col bg-[#fdf8f5]">
            <Header />
            
            <main className="flex-grow px-4 py-6 container mx-auto">
                <h1 className="text-3xl font-bold text-center mb-8 text-[#54372A]">My Brews</h1>
                
                {/* Upload Section */}
                <div className="mb-10 bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4 text-[#54372A]">Share Your Coffee Brewing</h2>
                    
                    <div className={`border-2 border-dashed rounded-lg p-8 transition-all ${isUploading ? 'border-[#C94C10]' : 'border-gray-300'}`}>
                        <div className="flex flex-col items-center">
                            <FaCloudUploadAlt className={`text-5xl mb-4 ${isUploading ? 'text-[#C94C10]' : 'text-gray-400'}`} />
                            
                            <input 
                                type="file"
                                accept="video/*"
                                onChange={handleFileSelect}
                                className="hidden"
                                ref={fileInputRef}
                                disabled={isUploading}
                            />
                            
                            {!isUploading ? (
                                <div className="text-center">
                                    <button
                                        onClick={() => fileInputRef.current.click()}
                                        className="bg-[#C94C10] hover:bg-[#A83C08] text-white px-6 py-3 rounded-full transition-colors mb-3"
                                    >
                                        Select Video File
                                    </button>
                                    <p className="text-gray-500 text-sm">
                                        Maximum file size: 500MB
                                    </p>
                                </div>
                            ) : (
                                <div className="w-full">
                                    <div className="flex justify-between items-center mb-2">
                                        <span>Uploading video...</span>
                                        <span>{uploadProgress}%</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                                        <div
                                            className="bg-[#C94C10] h-2.5 rounded-full transition-all"
                                            style={{ width: `${uploadProgress}%` }}
                                        ></div>
                                    </div>
                                    <button
                                        onClick={cancelUpload}
                                        className="mt-4 text-[#C94C10] hover:text-[#A83C08] transition-colors"
                                    >
                                        Cancel Upload
                                    </button>
                                </div>
                            )}
                            
                            {error && (
                                <div className="mt-4 text-red-500 text-sm">
                                    {error}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
                
                {/* Videos Gallery */}
                <div>
                    <h2 className="text-xl font-semibold mb-4 text-[#54372A]">My Brew Videos</h2>
                    
                    {videos.length === 0 ? (
                        <div className="bg-white p-10 rounded-lg shadow-md text-center">
                            <p className="text-gray-500">You haven&apos;t uploaded any videos yet.</p>
                            <button
                                onClick={() => fileInputRef.current.click()}
                                className="bg-[#C94C10] hover:bg-[#A83C08] text-white px-4 py-2 rounded-full transition-colors mt-4"
                            >
                                Upload Your First Brew
                            </button>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                            {videos.map((video) => (
                                <div key={video.id} className="bg-white rounded-lg overflow-hidden shadow-md">
                                    <div 
                                        className="relative aspect-video cursor-pointer bg-gray-100"
                                        onClick={() => openVideoPlayer(video)}
                                    >
                                        {video.thumbnail ? (
                                            <img 
                                                src={`${apiUrl}${video.thumbnail.substring(1)}`} 
                                                alt={video.name}
                                                className="w-full h-full object-cover"
                                            />
                                        ) : (
                                            <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                                                <FaPlay className="text-gray-400 text-4xl" />
                                            </div>
                                        )}
                                        <div className="absolute inset-0 bg-black bg-opacity-20 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                                            <FaPlay className="text-white text-4xl" />
                                        </div>
                                    </div>
                                    <div className="p-4">
                                        <div className="flex justify-between items-center">
                                            <h3 className="font-medium">{video.name}</h3>
                                            <button 
                                                onClick={() => deleteVideo(video.id)}
                                                className="text-red-500 hover:text-red-700 transition-colors"
                                                title="Delete video"
                                            >
                                                <FaTrash />
                                            </button>
                                        </div>
                                        <p className="text-gray-500 text-sm mt-1">
                                            {new Date(video.uploaded_at).toLocaleDateString()}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
                
                {/* Video Player Modal */}
                {activeVideo && (
                    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
                        <div className="bg-white rounded-lg overflow-hidden max-w-4xl w-full max-h-[90vh] flex flex-col">
                            <div className="p-4 border-b border-gray-200 flex justify-between items-center">
                                <h3 className="font-medium truncate">{activeVideo.name}</h3>
                                <button 
                                    onClick={closeVideoPlayer}
                                    className="text-gray-500 hover:text-gray-700"
                                >
                                    ✕
                                </button>
                            </div>
                            <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
                                <video
                                    className="absolute inset-0 w-full h-full"
                                    controls
                                    autoPlay
                                    src={`${apiUrl}${activeVideo.url.substring(1)}`}
                                >
                                    Your browser does not support the video tag.
                                </video>
                            </div>
                        </div>
                    </div>
                )}
            </main>
            
            <Footer index={3} />
        </div>
    );
}

// Wrap the component with ProtectedRoute
export default function ProtectedMyBrews() {
    return (
        <ProtectedRoute>
            <MyBrews />
        </ProtectedRoute>
    );
}