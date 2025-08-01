<?php


include '../includes/header.php';
?>

<div class="about-container">
    <div class="about-header">
        <h2> About Vacation Destinations Manager</h2>
        <p class="last-updated">Last updated: May 5, 2025</p>
    </div>
    
    <div class="about-section">
        <h3>About Our Service</h3>
        <p>
            Welcome to Vacation Destinations Manager, your ultimate tool for discovering and managing dream vacation spots from around the world. 
            Our platform allows you to explore beautiful destinations, organize them by country, and keep track of essential information like costs and attractions.
            Whether you're a travel enthusiast, a vacation planner, or just looking for inspiration for your next trip, our application is designed to make 
            destination discovery simple and enjoyable.
        </p>
    </div>
    
    <div class="about-section">
        <h3>Our Team</h3>
        <div class="team-members">
            <div class="team-member">
                <div class="member-avatar">
                    
                </div>
                <h4>Dumitrascu Constantin-Alexandru</h4>
                <p class="member-title">Founder & Lead Developer</p>
                <p class="member-bio">
                    Dumitrascu Constantin-Alexandru created Vacation Destinations Manager after struggling to organize travel plans for a world tour.
                    With 10+ years of development experience, he built this platform to help fellow travelers.
                </p>
            </div>
            
            <div class="team-member">
                <div class="member-avatar">
                    
                </div>
                <h4>Github Copilot</h4>
                <p class="member-title">Backend Developer</p>
                <p class="member-bio">
                    Github Copilot is a coding assistant that helps us write clean and efficient code. He has been instrumental in optimizing our backend processes,
                    ensuring that our application runs smoothly and efficiently.
                </p>
            </div>
            <div class="team-member">
                <div class="member-avatar">
                    
                </div>
                <h4>Chat GPT</h4>
                <p class="member-title">UX Designer</p>
                <p class="member-bio">
                    Chat GPT is an AI language model that has assisted us in creating user-friendly interfaces and improving the overall user experience of our application.
                    With its help, we have designed a platform that is not only functional but also visually appealing and easy to navigate.
                </p>
            </div>
        </div>
    </div>
    
    <div class="about-section">
        <h3>Our Features</h3>
        <ul class="features-list">
            <li>
                
                <div class="feature-content">
                    <h4>Country-Based Organization</h4>
                    <p>Browse destinations by country with our intuitive filtering system</p>
                </div>
            </li>
            
            <li>
                
                <div class="feature-content">
                    <h4>Cost Estimation</h4>
                    <p>See daily cost estimates for each destination to help plan your budget</p>
                </div>
            </li>
            
            <li>
                
                <div class="feature-content">
                    <h4>Tourist Attractions</h4>
                    <p>Detailed information about must-see attractions at each destination</p>
                </div>
            </li>
            
            <li>
                
                <div class="feature-content">
                    <h4>Personalized Management</h4>
                    <p>Add, edit, and organize destinations to build your personal travel database</p>
                </div>
            </li>
        </ul>
    </div>
    
    <div class="about-section">
        <h3>Technology Stack</h3>
        <p>
            Our application is built using modern web technologies including PHP for server-side processing,
            MySQL for reliable data storage, JavaScript for interactive features, and CSS for a responsive design.
            We use AJAX technology to provide a seamless user experience without page reloads when filtering destinations.
        </p>
    </div>
    
    <div class="about-section">
        <h3>Contact Us</h3>
        <div class="contact-info">
            <p> Email: <a href="mailto:alexdumitrascu???+vacationplanner@gmail.com">alexdumitrascu???+vacationplanner@gmail.com</a></p>
            <p> Phone: +40 757 249 ???</p>
            <p> Address: 523 Baita Street, Sarmin-segetusa, SS 98765</p>
        </div>
    </div>
</div>

<style>
    .about-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: var(--radius);
        box-shadow: var(--shadow);
    }
    
    .about-header {
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--primary-color);
    }
    
    .about-header h2 {
        color: var(--primary-color);
    }
    
    .last-updated {
        font-style: italic;
        color: var(--gray-color);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .about-section {
        margin-bottom: 2.5rem;
    }
    
    .about-section h3 {
        color: var(--dark-color);
        border-left: 4px solid var(--primary-color);
        padding-left: 1rem;
        margin-bottom: 1rem;
    }
    
    .team-members {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 2rem;
        margin-top: 1.5rem;
    }
    
    .team-member {
        background: #f9f9f9;
        padding: 1.5rem;
        border-radius: var(--radius);
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .team-member:hover {
        transform: translateY(-5px);
    }
    
    .member-avatar {
        font-size: 3rem;
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    .member-title {
        color: var(--primary-color);
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .member-bio {
        font-size: 0.9rem;
    }
    
    .features-list {
        list-style: none;
        padding: 0;
    }
    
    .features-list li {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1.5rem;
        background: #f9f9f9;
        padding: 1rem;
        border-radius: var(--radius);
    }
    
    .features-list i {
        font-size: 1.8rem;
        color: var(--primary-color);
        margin-right: 1rem;
        min-width: 40px;
        text-align: center;
    }
    
    .feature-content h4 {
        margin: 0 0 0.5rem 0;
        color: var(--dark-color);
    }
    
    .feature-content p {
        margin: 0;
    }
    
    .contact-info {
        background: #f9f9f9;
        padding: 1.5rem;
        border-radius: var(--radius);
    }
    
    .contact-info p {
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
    }
    
    .contact-info i {
        width: 25px;
        color: var(--primary-color);
        margin-right: 0.8rem;
    }
    
    .contact-info a {
        color: var(--primary-color);
        text-decoration: none;
    }
    
    .contact-info a:hover {
        text-decoration: underline;
    }
    
    @media (max-width: 768px) {
        .team-members {
            grid-template-columns: 1fr;
        }
        
        .about-container {
            padding: 1.5rem;
        }
    }
</style>

<?php include '../includes/footer.php'; ?>