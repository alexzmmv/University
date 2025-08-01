from fastapi import FastAPI, HTTPException, File, Form, UploadFile, BackgroundTasks, Depends, Query
from fastapi.responses import FileResponse  
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import random
import uuid
from typing import Optional, Dict, List
import math
import time
import os
import shutil
import subprocess
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.database.database import get_db, engine, Base
from app.database.models.models import CoffeeShop, Drink, Video, User
from app.auth.router import router as auth_router
from app.auth.jwt import get_current_active_user

app = FastAPI(title="Coffee Addict API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This should be more restrictive in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def compute_distance(lat1, lon1, lat2, lon2):
    R = 6371  
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return (R * c).__round__(2)

@app.get("/")
async def root():
    return {"message": "Welcome to Coffee Addict API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include the authentication router
app.include_router(auth_router)

# Protected route example
@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_active_user)):
    """
    Example of a protected route that requires authentication
    """
    return {
        "message": "This is a protected route",
        "user": {
            "username": current_user.username,
            "email": current_user.email
        }
    }

@app.get("/coffee-shops")
async def get_coffee_shops(
    latitude: float,
    longitude: float,
    sort_by: Optional[str] = None,
    open_status: Optional[bool] = Query(None, alias="Open"),
    search: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    max_distance: Optional[float] = None,
    sort_order: Optional[str] = "asc",
    page: Optional[int] = 1,
    page_size: Optional[int] = 10,
    db: Session = Depends(get_db)
    ):
    
    # Input validation
    if max_distance is not None and max_distance < 0:
        raise HTTPException(status_code=400, detail="max_distance must be a positive number")
    if min_rating is not None and (min_rating < 0 or min_rating > 5):
        raise HTTPException(status_code=400, detail="min_rating must be between 0 and 5")
    if max_rating is not None and (max_rating < 0 or max_rating > 5):
        raise HTTPException(status_code=400, detail="max_rating must be between 0 and 5")
    if min_rating is not None and max_rating is not None and min_rating > max_rating:
        raise HTTPException(status_code=400, detail="min_rating cannot be greater than max_rating")
    if sort_by is not None and sort_by not in ["location", "rating"]:
        raise HTTPException(status_code=400, detail="sort_by must be one of: location, rating")
    if sort_order.lower() not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="sort_order must be 'asc' or 'desc'")
    if latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180:
        raise HTTPException(status_code=400, detail="Invalid latitude or longitude, it should be in degree format")
    if search and not isinstance(search, str):
        raise HTTPException(status_code=400, detail="search must be a string")
    if page < 1:
        raise HTTPException(status_code=400, detail="page must be greater than or equal to 1")
    if page_size < 1 or page_size > 50:
        raise HTTPException(status_code=400, detail="page_size must be between 1 and 50")
    
    # Base query
    query = db.query(CoffeeShop)
    
    # Apply filters
    if search:
        query = query.filter(CoffeeShop.name.ilike(f"%{search}%"))
    
    if min_rating is not None:
        query = query.filter(CoffeeShop.rating >= min_rating)
    
    if max_rating is not None:
        query = query.filter(CoffeeShop.rating <= max_rating)
    
    if open_status:
        query = query.filter(CoffeeShop.status.like("Open%"))
    
    # Get all matching coffee shops with distance calculation
    all_shops = query.all()
    
    # Process distance in Python since PostgreSQL geographic functions are not being used
    local_shops = []
    for shop in all_shops:
        distance = compute_distance(latitude, longitude, shop.latitude, shop.longitude)
        
        # Skip if beyond max distance
        if max_distance is not None and distance > max_distance:
            continue
            
        local_shop = {
            "public_id": shop.public_id,
            "name": shop.name,
            "location": {
                "latitude": shop.latitude,
                "longitude": shop.longitude
            },
            "rating": shop.rating,
            "status": shop.status,
            "image": shop.image,
            "distance": distance
        }
        local_shops.append(local_shop)
    
    if sort_by == "location" or sort_by is None:  
        local_shops.sort(key=lambda x: x["distance"], reverse=(sort_order.lower() == "desc"))
    elif sort_by == "rating":
        local_shops.sort(key=lambda x: x["rating"], reverse=(sort_order.lower() == "desc"))
    
    total_shops = len(local_shops)
    total_pages = max(1, math.ceil(total_shops / page_size))
    
    if page > total_pages:
        page = total_pages
    
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_shops)
    
    logging.info(f"Pagination: Page {page}/{total_pages}, Items {start_idx+1}-{end_idx} of {total_shops}")
    logging.info(f"Query params: lat={latitude}, lon={longitude}, sort={sort_by}, filter_open={open_status}, search='{search}'")
    
    paged_shops = local_shops[start_idx:end_idx]
    
    return {
        "coffee_shops": paged_shops,
        "pagination": {
            "total": total_shops,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }

@app.get("/coffee-shops/{public_id}")
async def get_coffee_shop(public_id: str, db: Session = Depends(get_db)):
    shop = db.query(CoffeeShop).filter(CoffeeShop.public_id == public_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Coffee shop not found")
    
    return {
        "coffee_shops": {
            "public_id": shop.public_id,
            "name": shop.name,
            "location": {
                "latitude": shop.latitude,
                "longitude": shop.longitude
            },
            "rating": shop.rating,
            "status": shop.status,
            "image": shop.image
        }
    }

@app.get("/coffee-shops/{public_id}/drinks")
async def get_coffee_shop_drinks(public_id: str, db: Session = Depends(get_db)):
    shop = db.query(CoffeeShop).filter(CoffeeShop.public_id == public_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Coffee shop not found")
    
    drinks = db.query(Drink).filter(Drink.coffee_shop_id == shop.id).all()
    
    drinks_list = []
    for drink in drinks:
        drinks_list.append({
            "id": drink.id,
            "name": drink.name,
            "description": drink.description,
            "price": drink.price,
            "image": drink.image,
            "sales": drink.sales,
            "popularity": drink.popularity
        })
    
    return {"drinks": drinks_list}

@app.post("/coffee-shops/{public_id}/drinks")
async def create_coffee_shop_drink(public_id: str, drink: Dict, db: Session = Depends(get_db)):
    # Validate input
    if not all(key in drink for key in ["name", "description", "price", "image", "sales", "popularity"]):
        raise HTTPException(status_code=400, detail="Missing required fields in drink data")
    if not isinstance(drink["name"], str) or not isinstance(drink["description"], str) or not isinstance(drink["price"], str) or not isinstance(drink["image"], str):
        raise HTTPException(status_code=400, detail="Invalid data types for string fields")
    if not drink["name"] or not drink["description"] or not drink["price"] or not drink["image"]:
        raise HTTPException(status_code=400, detail="Empty fields in drink data")    
    
    try:
        sales = int(drink["sales"])
        popularity = int(drink["popularity"])
        if sales < 0 or popularity < 0:
            raise HTTPException(status_code=400, detail="sales and popularity must be non-negative integers")
    except ValueError:
        raise HTTPException(status_code=400, detail="sales and popularity must be valid integers")
    
    try:
        price_val = float(drink["price"])
        if price_val < 0:
            raise HTTPException(status_code=400, detail="price must be non-negative")
    except ValueError:
        raise HTTPException(status_code=400, detail="price must be a valid number string")
    
    # Find the coffee shop
    shop = db.query(CoffeeShop).filter(CoffeeShop.public_id == public_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Coffee shop not found")
    
    # Create new drink
    new_drink = Drink(
        name=drink["name"],
        description=drink["description"],
        price=drink["price"],
        image=drink["image"],
        sales=sales,
        popularity=popularity,
        coffee_shop_id=shop.id
    )
    
    db.add(new_drink)
    db.commit()
    db.refresh(new_drink)
    
    return {
        "drink": {
            "id": new_drink.id,
            "name": new_drink.name,
            "description": new_drink.description,
            "price": new_drink.price,
            "image": new_drink.image,
            "sales": new_drink.sales,
            "popularity": new_drink.popularity
        }
    }

@app.put("/coffee-shops/{public_id}/drinks/{drink_id}")
async def update_coffee_shop_drink(public_id: str, drink_id: int, drink: Dict, db: Session = Depends(get_db)):
    # Validate input
    if not all(key in drink for key in ["name", "description", "price", "image", "sales", "popularity"]):
        raise HTTPException(status_code=400, detail="Missing required fields in drink data")    
    if not isinstance(drink["name"], str) or not isinstance(drink["description"], str) or not isinstance(drink["price"], str) or not isinstance(drink["image"], str):
        raise HTTPException(status_code=400, detail="Invalid data types for string fields")
    if not drink["name"] or not drink["description"] or not drink["price"] or not drink["image"]:
        raise HTTPException(status_code=400, detail="Empty fields in drink data")
    
    try:
        sales = int(drink["sales"])
        popularity = int(drink["popularity"])
        if sales < 0 or popularity < 0:
            raise HTTPException(status_code=400, detail="sales and popularity must be non-negative integers")
    except ValueError:
        raise HTTPException(status_code=400, detail="sales and popularity must be valid integers")
    
    try:
        price_val = float(drink["price"])
        if price_val < 0:
            raise HTTPException(status_code=400, detail="price must be non-negative")
    except ValueError:
        raise HTTPException(status_code=400, detail="price must be a valid number string")

    # Find the coffee shop
    shop = db.query(CoffeeShop).filter(CoffeeShop.public_id == public_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Coffee shop not found")
    
    # Find the drink
    db_drink = db.query(Drink).filter(
        Drink.id == drink_id,
        Drink.coffee_shop_id == shop.id
    ).first()
    
    if not db_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    
    # Update drink
    db_drink.name = drink["name"]
    db_drink.description = drink["description"]
    db_drink.price = drink["price"]
    db_drink.image = drink["image"]
    db_drink.sales = sales
    db_drink.popularity = popularity
    
    db.commit()
    db.refresh(db_drink)
    
    return {
        "drink": {
            "id": db_drink.id,
            "name": db_drink.name,
            "description": db_drink.description,
            "price": db_drink.price,
            "image": db_drink.image,
            "sales": db_drink.sales,
            "popularity": db_drink.popularity
        }
    }

@app.delete("/coffee-shops/{public_id}/drinks/{drink_id}")
async def delete_coffee_shop_drink(public_id: str, drink_id: int, db: Session = Depends(get_db)):
    # Find the coffee shop
    shop = db.query(CoffeeShop).filter(CoffeeShop.public_id == public_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Coffee shop not found")
    
    # Find the drink
    db_drink = db.query(Drink).filter(
        Drink.id == drink_id,
        Drink.coffee_shop_id == shop.id
    ).first()
    
    if not db_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    
    # Delete the drink
    db.delete(db_drink)
    db.commit()
    
    return {"message": "Drink deleted"}

# Video Upload and Processing

# Video storage paths
UPLOAD_DIR = Path("./vid/uploads")
THUMBNAIL_DIR = Path("./vid/thumbnails")
CHUNK_DIR = Path("./vid/temp_chunks")

# Create directories 
for directory in [UPLOAD_DIR, THUMBNAIL_DIR, CHUNK_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

print(f"Using storage directories: uploads={UPLOAD_DIR}, thumbnails={THUMBNAIL_DIR}, chunks={CHUNK_DIR}")
# In-memory storage for active uploads
active_uploads = {}

# Helper function to generate thumbnail from video
def generate_thumbnail(video_path, output_path, timestamp="00:00:05"):
    try:
        command = [
            "ffmpeg", "-i", str(video_path),
            "-ss", timestamp,
            "-vframes", "1",
            str(output_path),
            "-y"
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print(f"Thumbnail generation error: {e}")
        return False

def process_video(video_id, original_filename, db: Session):
    try:
        video_path = UPLOAD_DIR / f"{video_id}.mp4"
        thumbnail_path = THUMBNAIL_DIR / f"{video_id}.jpg"
        
        thumbnail_success = generate_thumbnail(video_path, thumbnail_path)
        
        if thumbnail_success:
            video = db.query(Video).filter(Video.id == video_id).first()
            if video:
                video.thumbnail = f"/thumbnails/{video_id}.jpg"
                db.commit()
    except Exception as e:
        print(f"Video processing error: {e}")

@app.get("/mybrews/videos")
async def get_videos(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Get all videos for the authenticated user
    """
    # In a real application, you would filter videos by user_id
    # For now, we'll just return all videos
    videos = db.query(Video).all()
    return {
        "videos": [
            {
                "id": video.id,
                "name": video.name,
                "url": video.url,
                "thumbnail": video.thumbnail,
                "uploaded_at": video.uploaded_at
            } for video in videos
        ]
    }

@app.get("/videos/{filename}")
async def get_video_file(filename: str):
    """Stream a video file"""
    video_path = UPLOAD_DIR / filename
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")
    return FileResponse(video_path)

@app.get("/thumbnails/{filename}")
async def get_thumbnail(filename: str):
    """Get a video thumbnail"""
    thumbnail_path = THUMBNAIL_DIR / filename
    if not thumbnail_path.exists():
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    return FileResponse(thumbnail_path)

@app.post("/mybrews/videos/init")
async def init_video_upload(
    filename: str = Form(...),
    fileType: str = Form(...),
    fileSize: int = Form(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Initialize a video upload for the authenticated user
    """
    # Create an upload ID
    upload_id = str(uuid.uuid4())
    
    # In a production app, you would store this in a database along with the user ID
    
    return {"uploadId": upload_id}

@app.post("/mybrews/videos/chunk")
async def upload_video_chunk(
    chunk: UploadFile = File(...),
    uploadId: str = Form(...),
    partNumber: int = Form(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload a chunk of a video file for the authenticated user
    """
    # In a production app, you would validate the upload ID and user ID
    
    # Save the chunk
    chunk_dir = Path("app/vid/temp_chunks") / uploadId
    chunk_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_path = chunk_dir / f"part_{partNumber}"
    with open(chunk_path, "wb") as f:
        shutil.copyfileobj(chunk.file, f)
    
    return {"success": True}

@app.post("/mybrews/videos/complete")
async def complete_video_upload(
    uploadId: str = Form(...),
    filename: str = Form(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Complete the video upload by combining chunks"""
    if uploadId not in active_uploads:
        raise HTTPException(status_code=404, detail="Upload ID not found")
    
    upload = active_uploads[uploadId]
    if upload["completed"]:
        raise HTTPException(status_code=400, detail="Upload already completed")
    
    video_id = str(uuid.uuid4())
    safe_filename = "".join(c if c.isalnum() or c in ['.', '_', '-'] else '_' for c in filename)
    output_filename = f"{video_id}.mp4"
    output_path = UPLOAD_DIR / output_filename
    
    chunk_numbers = sorted(list(map(int, upload["chunks"].keys())))
    
    try:
        with open(output_path, "wb") as outfile:
            for part_num in chunk_numbers:
                chunk_path = upload["chunks"][part_num]["path"]
                with open(chunk_path, "rb") as infile:
                    shutil.copyfileobj(infile, outfile)
        
        # Create video record in database
        video = Video(
            id=video_id,
            name=filename,
            url=f"/videos/{output_filename}",
            thumbnail=None,  # Will be set by background task
            uploaded_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )
        
        db.add(video)
        db.commit()
        db.refresh(video)
        
        # Mark upload as completed
        upload["completed"] = True
        
        # Process video in background
        if background_tasks:
            background_tasks.add_task(
                process_video,
                video_id=video_id,
                original_filename=filename,
                db=db
            )
        
        # Clean up chunks
        chunk_dir = CHUNK_DIR / uploadId
        shutil.rmtree(chunk_dir, ignore_errors=True)
        
        active_uploads.pop(uploadId, None)
        
        return {
            "success": True, 
            "video": {
                "id": video.id,
                "name": video.name,
                "url": video.url,
                "thumbnail": video.thumbnail,
                "uploaded_at": video.uploaded_at
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete upload: {str(e)}")


@app.delete("/mybrews/videos/{video_id}")
async def delete_video(video_id: str, db: Session = Depends(get_db)):
    """Delete a video"""
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Delete video file
    video_path = UPLOAD_DIR / f"{video_id}.mp4"
    if video_path.exists():
        os.remove(video_path)
    
    # Delete thumbnail
    thumbnail_path = THUMBNAIL_DIR / f"{video_id}.jpg"
    if thumbnail_path.exists():
        os.remove(thumbnail_path)
    
    # Delete from database
    db.delete(video)
    db.commit()
    
    return {"success": True}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    print("Starting server on port", sys.argv[1])
    uvicorn.run("app.server:app", host="0.0.0.0", port=int(sys.argv[1]), reload=True)