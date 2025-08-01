<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Management System - Java Servlets</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        .tech-badge {
            background-color: #007396;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            margin-left: 10px;
        }
        .user-section {
            background-color: #e8f4f8;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .section h3 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        input[type="text"], select, textarea {
            width: 100%;
            padding: 10px;
            margin: 5px 0 15px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background-color: #2980b9;
        }
        .projects-grid, .developers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .project-card, .developer-card {
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 8px;
            background-color: #f9f9f9;
        }
        .project-card h4, .developer-card h4 {
            margin-top: 0;
            color: #2c3e50;
        }
        .user-projects {
            background-color: #e8f5e8;
        }
        .assign-section {
            background-color: #fff3cd;
        }
        .filter-section {
            background-color: #f8d7da;
        }
        .hidden {
            display: none;
        }
        .current-user {
            font-weight: bold;
            color: #e74c3c;
        }
        ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .checkbox-group {
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            margin: 10px 0;
        }
        .checkbox-item {
            margin: 5px 0;
        }
        .setup-link {
            background-color: #e74c3c;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 20px;
        }
        .setup-link:hover {
            background-color: #c0392b;
            color: white;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Project Management System</h1>
            <span class="tech-badge">Java Servlets + Tomcat</span>
            <p>Manage software developers and projects efficiently</p>
            
            <!-- Database Setup Link -->
            <div style="margin: 20px 0;">
                <a href="setup-database" class="setup-link">🔧 Setup Database First</a>
                <p style="font-size: 14px; color: #666;">Click above to create database tables and sample data</p>
            </div>
        </div>

        <!-- User Login Section -->
        <div class="user-section">
            <h3>👤 User Login</h3>
            <input type="text" id="username" placeholder="Enter your name to start using the application">
            <button onclick="setUser()">Set Current User</button>
            <div id="currentUser" class="hidden">
                <p>Current User: <span id="currentUserName" class="current-user"></span></p>
            </div>
        </div>

        <!-- All Projects Section -->
        <div class="section">
            <h3>📋 All Projects in Database</h3>
            <button onclick="loadAllProjects()">Display All Projects</button>
            <div id="allProjects" class="projects-grid"></div>
        </div>

        <!-- User Projects Section -->
        <div class="section user-projects">
            <h3>🔍 My Projects</h3>
            <button onclick="loadUserProjects()" id="loadUserProjectsBtn" disabled>Load My Projects</button>
            <div id="userProjects"></div>
        </div>

        <!-- Assign Developer Section -->
        <div class="section assign-section">
            <h3>➕ Assign Developer to Projects</h3>
            <input type="text" id="developerName" placeholder="Developer name to assign">
            <p>Select projects to assign the developer to:</p>
            <div id="projectsList" class="checkbox-group"></div>
            <input type="text" id="newProjectName" placeholder="Or enter new project name">
            <button onclick="assignDeveloper()">Assign Developer to Selected Projects</button>
            <div id="assignResult"></div>
        </div>

        <!-- All Developers Section -->
        <div class="section filter-section">
            <h3>👥 All Software Developers</h3>
            <button onclick="loadAllDevelopers()">Display All Developers</button>
            <div style="margin: 20px 0;">
                <input type="text" id="skillFilter" placeholder="Enter skill to filter (e.g., Java, PHP, Python)">
                <button onclick="filterDevelopersBySkill()">Filter by Skill</button>
                <button onclick="showAllDevelopers()">Show All</button>
            </div>
            <div id="allDevelopers" class="developers-grid"></div>
        </div>
    </div>

    <script>
        let currentUser = '';
        let allProjectsData = [];
        let allDevelopersData = [];
        
        // Base URL for API calls - use relative path to avoid CORS issues
        const API_BASE = '<%= request.getContextPath() %>/api';

        function setUser() {
            const username = document.getElementById('username').value.trim();
            if (username) {
                currentUser = username;
                document.getElementById('currentUserName').textContent = username;
                document.getElementById('currentUser').classList.remove('hidden');
                document.getElementById('loadUserProjectsBtn').disabled = false;
                loadProjectsForAssignment();
            } else {
                alert('Please enter a valid username');
            }
        }

        async function loadAllProjects() {
            try {
                const response = await fetch(API_BASE + '/projects');
                if (!response.ok) {
                    throw new Error('HTTP error! status: ' + response.status);
                }
                
                const projects = await response.json();
                allProjectsData = projects;
                
                const container = document.getElementById('allProjects');
                container.innerHTML = '';
                
                if (projects && projects.length > 0) {
                    projects.forEach(project => {
                        const projectCard = document.createElement('div');
                        projectCard.className = 'project-card';
                        
                        const projectName = project.name ? String(project.name) : 'Unknown Project';
                        const projectId = project.id !== null && project.id !== undefined ? String(project.id) : 'N/A';
                        const description = project.description ? String(project.description) : 'No description';
                        const managerId = project.projectManagerID !== null && project.projectManagerID !== undefined ? String(project.projectManagerID) : 'Not assigned';
                        const managerName = project.managerName ? String(project.managerName) : 'Not assigned';
                        const members = project.members ? String(project.members) : 'No members';
                        
                        projectCard.innerHTML = 
                            '<h4>🎯 ' + projectName + '</h4>' +
                            '<p><strong>ID:</strong> ' + projectId + '</p>' +
                            '<p><strong>Description:</strong> ' + description + '</p>' +
                            '<p><strong>Project Manager ID:</strong> ' + managerId + '</p>' +
                            '<p><strong>Manager:</strong> ' + managerName + '</p>' +
                            '<p><strong>Members:</strong> ' + members + '</p>';
                        
                        container.appendChild(projectCard);
                    });
                } else {
                    container.innerHTML = '<p>No projects found. Please setup the database first.</p>';
                }
            } catch (error) {
                const container = document.getElementById('allProjects');
                container.innerHTML = '<p style="color: red;">Error loading projects: ' + error.message + '</p>';
            }
        }

        async function loadUserProjects() {
            if (!currentUser) {
                alert('Please set your username first');
                return;
            }

            try {
                const response = await fetch(API_BASE + '/projects', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        action: 'get_user_projects',
                        username: currentUser
                    })
                });
                
                const projects = await response.json();
                const container = document.getElementById('userProjects');
                
                if (projects.length > 0) {
                    container.innerHTML = '<h4>Projects you are a member of:</h4><ul>';
                    projects.forEach(project => {
                        container.innerHTML += '<li><strong>' + project.name + '</strong></li>';
                    });
                    container.innerHTML += '</ul>';
                } else {
                    container.innerHTML = '<p>You are not a member of any projects.</p>';
                }
            } catch (error) {
                alert('Error loading user projects');
            }
        }

        async function loadProjectsForAssignment() {
            try {
                const response = await fetch(API_BASE + '/projects');
                const projects = await response.json();
                
                const container = document.getElementById('projectsList');
                container.innerHTML = '';
                
                projects.forEach(project => {
                    const checkboxDiv = document.createElement('div');
                    checkboxDiv.className = 'checkbox-item';
                    checkboxDiv.innerHTML = 
                        '<input type="checkbox" id="project_' + project.id + '" value="' + project.name + '">' +
                        '<label for="project_' + project.id + '">' + project.name + '</label>';
                    container.appendChild(checkboxDiv);
                });
            } catch (error) {
                console.error('Error loading projects for assignment:', error);
            }
        }

        async function assignDeveloper() {
            const developerName = document.getElementById('developerName').value.trim();
            const newProjectName = document.getElementById('newProjectName').value.trim();
            
            if (!developerName) {
                alert('Please enter a developer name');
                return;
            }

            // Get selected projects
            const selectedProjects = [];
            const checkboxes = document.querySelectorAll('#projectsList input[type="checkbox"]:checked');
            checkboxes.forEach(checkbox => {
                selectedProjects.push(checkbox.value);
            });

            // Add new project if specified
            if (newProjectName) {
                selectedProjects.push(newProjectName);
            }

            if (selectedProjects.length === 0) {
                alert('Please select at least one project or enter a new project name');
                return;
            }

            try {
                const response = await fetch(API_BASE + '/projects', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        action: 'assign_developer',
                        developer: developerName,
                        projects: selectedProjects
                    })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    let resultHtml = '<h4>Assignment Results:</h4><ul>';
                    result.results.forEach(res => {
                        resultHtml += '<li><strong>' + res.project + ':</strong> ' + res.status + '</li>';
                    });
                    resultHtml += '</ul>';
                    document.getElementById('assignResult').innerHTML = resultHtml;
                    
                    // Clear form
                    document.getElementById('developerName').value = '';
                    document.getElementById('newProjectName').value = '';
                    checkboxes.forEach(checkbox => checkbox.checked = false);
                    
                    // Reload projects list
                    loadProjectsForAssignment();
                } else {
                    document.getElementById('assignResult').innerHTML = '<p style="color: red;">Error: ' + result.message + '</p>';
                }
            } catch (error) {
                alert('Error assigning developer');
            }
        }

        async function loadAllDevelopers() {
            try {
                const response = await fetch(API_BASE + '/developers');
                if (!response.ok) {
                    throw new Error('HTTP error! status: ' + response.status);
                }
                
                const developers = await response.json();
                allDevelopersData = developers;
                displayDevelopers(developers);
            } catch (error) {
                const container = document.getElementById('allDevelopers');
                container.innerHTML = '<p style="color: red;">Error loading developers: ' + error.message + '</p>';
            }
        }

        function displayDevelopers(developers) {
            const container = document.getElementById('allDevelopers');
            container.innerHTML = '';
            
            if (developers && developers.length > 0) {
                developers.forEach(developer => {
                    const developerCard = document.createElement('div');
                    developerCard.className = 'developer-card';
                    
                    const devName = developer.name ? String(developer.name) : 'Unknown Developer';
                    const devId = developer.id !== null && developer.id !== undefined ? String(developer.id) : 'N/A';
                    const devAge = developer.age !== null && developer.age !== undefined && developer.age !== 0 
                        ? String(developer.age) 
                        : 'Not specified';
                    const devSkills = developer.skills && String(developer.skills).trim() !== '' 
                        ? String(developer.skills) 
                        : 'No skills listed';
                    
                    developerCard.innerHTML = 
                        '<h4>👨‍💻 ' + devName + '</h4>' +
                        '<p><strong>ID:</strong> ' + devId + '</p>' +
                        '<p><strong>Age:</strong> ' + devAge + '</p>' +
                        '<p><strong>Skills:</strong> ' + devSkills + '</p>';
                    
                    container.appendChild(developerCard);
                });
            } else {
                container.innerHTML = '<p>No developers found.</p>';
            }
        }

        function filterDevelopersBySkill() {
            const skill = document.getElementById('skillFilter').value.trim().toLowerCase();
            if (!skill) {
                alert('Please enter a skill to filter by');
                return;
            }

            const filteredDevelopers = allDevelopersData.filter(developer => 
                developer.skills && developer.skills.toLowerCase().includes(skill)
            );

            displayDevelopers(filteredDevelopers);
            
            if (filteredDevelopers.length === 0) {
                document.getElementById('allDevelopers').innerHTML = 
                    '<p>No developers found with skill: <strong>' + skill + '</strong></p>';
            }
        }

        function showAllDevelopers() {
            displayDevelopers(allDevelopersData);
            document.getElementById('skillFilter').value = '';
        }

        // Load initial data when page loads
        window.onload = function() {
            // Application ready
        };
    </script>
</body>
</html>
