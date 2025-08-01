# Transportation Route Selection Web Application

A Java web application built with JSP/Servlets that allows users to plan transportation routes by selecting connected cities.

## Features

- **User Authentication**: Secure login/logout with session management
- **Route Planning**: Interactive city selection with real-time route building
- **Route History**: View and modify planned routes with ability to go back to previous cities
- **Distance Tracking**: Calculate and display total route distance
- **Responsive Design**: Modern UI that works on desktop and mobile devices
- **Input Validation**: Client-side and server-side validation for all forms
- **Confirmation Dialogs**: User confirmations for destructive actions

## Technology Stack

- **Backend**: Java Servlets, JSP, JSTL
- **Database**: H2 Database (in-memory for development)
- **Build Tool**: Apache Maven
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Security**: BCrypt password hashing, Authentication filters
- **Server**: Apache Tomcat (embedded via Maven plugin)

## Prerequisites

- Java 11 or higher
- Maven 3.6 or higher
- Modern web browser

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Lab10
   ```

2. **Build the project**
   ```bash
   mvn clean compile
   ```

3. **Run the application**
   ```bash
   mvn jetty:run
   ```
   
   Or alternatively with Tomcat:
   ```bash
   mvn tomcat7:run
   ```

4. **Access the application**
   - Open your browser and navigate to: `http://localhost:8080/route-app`
   - Login with demo credentials: `admin` / `admin123` or `user1` / `admin123`

## Project Structure

```
src/
├── main/
│   ├── java/com/routeapp/
│   │   ├── dao/           # Data Access Objects
│   │   ├── model/         # Entity classes
│   │   ├── servlets/      # Servlet controllers
│   │   └── util/          # Utility classes
│   ├── resources/
│   │   └── init.sql       # Database initialization
│   └── webapp/
│       ├── css/           # Stylesheets
│       ├── js/            # JavaScript files
│       ├── *.jsp          # JSP view pages
│       └── WEB-INF/       # Web configuration
└── pom.xml                # Maven configuration
```

## Database Schema

The application uses an H2 in-memory database with the following tables:

- **users**: User accounts with hashed passwords
- **cities**: Available cities with country information  
- **city_connections**: Bidirectional connections between cities with distances

## API Endpoints

- `GET /login` - Display login page
- `POST /login` - Process login/registration
- `GET /logout` - Logout user
- `GET /route/select` - Route selection page
- `POST /route/select` - Process city selection
- `GET /route/route` - Display complete route
- `POST /route/route` - Route actions (new route, etc.)

## Features in Detail

### User Authentication
- Secure password hashing using BCrypt
- Session-based authentication
- Authentication filter protects all route pages
- Automatic session timeout after 30 minutes

### Route Planning
- Start by selecting any city
- Navigate through connected cities only
- Real-time route building with distance calculation
- Ability to go back to any previous city in the route
- Clear route or start new route options

### Input Validation
- Client-side validation for immediate feedback
- Server-side validation for security
- Proper error messages and user guidance
- Form field sanitization and validation

### User Experience
- Responsive design for all device sizes
- Interactive city cards with hover effects
- Confirmation dialogs for destructive actions
- Auto-hiding success/error messages
- Print and share functionality for routes

## Development

### Building for Production
```bash
mvn clean package
```

### Running Tests
```bash
mvn test
```

### Development Server
```bash
mvn jetty:run
```

## Configuration

- **Database**: Configure in `web.xml` context parameters
- **Session Timeout**: Set in `web.xml` session-config
- **Server Port**: Configure in Maven plugins section

## Security Features

- Password hashing with BCrypt
- SQL injection prevention through prepared statements
- Input validation and sanitization
- Session-based authentication
- CSRF protection through proper form handling

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes as part of a Web Programming lab assignment.

## Demo Data

The application comes with pre-loaded demo data including:

- **Cities**: Major European cities (Cluj-Napoca, Budapest, Vienna, Prague, etc.)
- **Routes**: Realistic connections between cities with distances
- **Users**: Demo accounts for testing

Default login credentials:
- Username: `admin` or `user1`
- Password: `admin123`
