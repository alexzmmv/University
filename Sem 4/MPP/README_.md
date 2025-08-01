# Coffee Addict Application

A full-stack coffee shop discovery application built with React/Next.js frontend and Python/FastAPI backend.

## Local Development

### Prerequisites

- Node.js 18+ and npm
- Python 3.12+
- PostgreSQL (or use SQLite for local development)
- Docker (optional, for containerized deployment)

### How to Run Locally

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/MPP-repo.git
    cd MPP-repo
    ```

2. Set up environment variables:
    ```bash
    # Copy example environment files
    cp .env.example .env
    cp coffe-addict-backend/.env.example coffe-addict-backend/.env
    
    # Edit the .env files with your actual values
    ```

3. Start the backend:
    ```bash
    cd coffe-addict-backend
    pip install -r requirements.txt
    python -m uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
    ```

4. Start the frontend:
    ```bash
    cd coffe-addict-frontend
    npm install
    npm run dev
    ```

5. Open your browser and navigate to `http://localhost:3000`.

## Environment Variables

### Backend Environment Variables

The backend application requires the following environment variables:

#### Database Configuration
- `DATABASE_URL`: Complete PostgreSQL connection string (optional if using individual Supabase variables)
- `USE_SQLITE`: Set to `"true"` to use SQLite instead of PostgreSQL (default: `"false"`)
- `USE_SUPABASE`: Set to `"true"` to use Supabase PostgreSQL (default: `"true"`)

#### Supabase Database Settings
- `SUPABASE_DB_NAME`: Database name (default: `"postgres"`)
- `SUPABASE_DB_USER`: Database username (required)
- `SUPABASE_DB_PASSWORD`: Database password (required)
- `SUPABASE_DB_HOST`: Database host (required, e.g., `"db.abcdefghijklm.supabase.co"`)
- `SUPABASE_DB_PORT`: Database port (default: `"5432"`)

#### JWT Authentication
- `JWT_SECRET_KEY`: Secret key for JWT tokens (required for production)
- `JWT_ALGORITHM`: JWT algorithm (default: `"HS256"`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration in minutes (default: `"30"`)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration in days (default: `"7"`)

#### SMS Service (Twilio)
- `TWILIO_ACCOUNT_SID`: Twilio account SID (required for SMS functionality)
- `TWILIO_AUTH_TOKEN`: Twilio authentication token (required for SMS functionality)
- `TWILIO_PHONE_NUMBER`: Twilio phone number for sending SMS (required for SMS functionality)

#### Other Backend Settings
- `BACKEND_URL`: Backend URL for internal references
- `NODE_ENV`: Environment mode (`development`, `production`)

### Frontend Environment Variables

The frontend application uses the following environment variables:

- `API_BASE_URL`: The URL of the backend API (default: `"http://localhost:8000/"`)
- `NODE_ENV`: Environment mode (automatically set by Next.js)
- `NEXT_TELEMETRY_DISABLED`: Disable Next.js telemetry (set to `1` to disable)

### AWS Deployment Variables

For AWS ECS deployment, the following environment variables are used:

- `AWS_REGION`: AWS region for deployment (default: `"eu-central-1"`)
- `AWS_ACCOUNT_ID`: Your AWS account ID (required for ECR)
- `CLUSTER_NAME`: ECS cluster name (default: `"coffee-addict-cluster"`)
- `SERVICE_NAME`: ECS service name (default: `"coffee-addict-service"`)
- `TASK_FAMILY`: ECS task definition family (default: `"coffee-addict"`)
- `IMAGE_TAG`: Docker image tag for deployment

## Deployment

### Using Docker Compose (Recommended for Local Testing)

You can run the application using Docker Compose for local testing:

```bash
# Copy .env.example to .env and update the values
cp .env.example .env

# Build and start the containers
docker-compose up -d --build
```

### Using the AWS ECS Deploy Script

We've created a comprehensive deploy script for AWS ECS deployment:

1. Set up your AWS credentials and ensure you have the required permissions for:
   - Amazon ECS (Elastic Container Service)
   - Amazon ECR (Elastic Container Registry)
   - Amazon EFS (Elastic File System)
   - IAM (Identity and Access Management)
   - VPC (Virtual Private Cloud)

2. Configure your environment variables:
    ```bash
    export AWS_ACCOUNT_ID=your-account-id
    export AWS_REGION=eu-central-1  # or your preferred region
    export IMAGE_TAG=latest
    ```

3. Make the script executable and deploy:
    ```bash
    chmod +x scripts/aws_deploy_final.sh
    ./scripts/aws_deploy_final.sh
    ```

4. The script supports various options:
    ```bash
    # Deploy only the frontend
    ./scripts/aws_deploy_final.sh --frontend-only
    
    # Deploy only the backend
    ./scripts/aws_deploy_final.sh --backend-only
    
    # Skip building images (just update the service)
    ./scripts/aws_deploy_final.sh --skip-build
    
    # Specify a different AWS region
    ./scripts/aws_deploy_final.sh --region us-east-1
    
    # Show all available options
    ./scripts/aws_deploy_final.sh --help
    ```

### Managing Your AWS ECS Application

Use the provided management scripts to control your deployed application:

#### Start the Application
```bash
./scripts/start.sh
```

#### Stop the Application
```bash
./scripts/stop.sh
```

#### Check Application Status
```bash
# View ECS service status
aws ecs describe-services --cluster coffee-addict-cluster --services coffee-addict-service

# View running tasks
aws ecs list-tasks --cluster coffee-addict-cluster --service-name coffee-addict-service
```

### Environment Configuration for Production

For production deployment, ensure you have set all required environment variables:

1. **Database Configuration**: Set up your Supabase or PostgreSQL database and configure the connection variables.

2. **JWT Security**: Generate a secure JWT secret key:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **SMS Service** (optional): Configure Twilio credentials if you need SMS functionality.

4. **AWS Configuration**: Set up your AWS credentials and region.

### Troubleshooting Deployment Issues

#### Frontend Not Connecting to Backend on ECS

If the frontend is using localhost instead of the API_BASE_URL environment variable:

1. Ensure the `API_BASE_URL` is correctly set in the task definition.
2. Rebuild the frontend image with the correct API_BASE_URL as a build argument.
3. Update the ECS service to use the new image.

#### Database Connection Issues

1. Verify your database credentials are correct.
2. Ensure your database allows connections from your ECS tasks.
3. Check the security groups allow traffic on the database port.

#### Container Startup Issues

1. Check the ECS task logs for error messages.
2. Verify all required environment variables are set.
3. Ensure the Docker images are built correctly and pushed to ECR.

## Architecture Overview

The Coffee Addict application consists of two main components:

### Backend (FastAPI + Python)
- **Framework**: FastAPI with Python 3.12
- **Database**: PostgreSQL (Supabase) with SQLAlchemy ORM
- **Authentication**: JWT-based authentication with refresh tokens
- **SMS Service**: Twilio integration for SMS notifications
- **API Documentation**: Automatic OpenAPI/Swagger documentation at `/docs`

### Frontend (Next.js + React)
- **Framework**: Next.js 14 with React
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React hooks and context
- **Build**: Optimized for production with standalone output

## Features

- **Coffee Shop Discovery**: Browse and search coffee shops
- **User Authentication**: JWT-based login/registration system
- **SMS Notifications**: Twilio-powered SMS alerts
- **Real-time Updates**: Live connection status monitoring
- **Responsive Design**: Mobile-first responsive interface
- **Location Services**: GPS-based coffee shop discovery
- **Rating System**: User reviews and ratings
- **Admin Dashboard**: Coffee shop management interface

## Development

### Project Structure

```
MPP-repo/
├── coffe-addict-backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── auth/                  # Authentication logic
│   │   ├── database/              # Database models and connections
│   │   ├── routers/               # API route handlers
│   │   └── server.py              # Main application entry point
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Backend container configuration
├── coffe-addict-frontend/         # Next.js React frontend
│   ├── src/app/                   # Next.js app directory
│   ├── package.json               # Node.js dependencies
│   └── Dockerfile                 # Frontend container configuration
├── scripts/                       # Deployment and management scripts
│   ├── aws_deploy_final.sh        # Main AWS deployment script
│   ├── start.sh                   # Start ECS service
│   └── stop.sh                    # Stop ECS service
└── .env.example                   # Environment variables template
```

### API Documentation

When running the backend locally, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Database Migrations

The application uses Alembic for database migrations:

```bash
cd coffe-addict-backend

# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

### Testing

```bash
# Backend tests
cd coffe-addict-backend
python -m pytest

# Frontend tests
cd coffe-addict-frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security Considerations

- Always use environment variables for sensitive data
- Generate secure JWT secret keys for production
- Use HTTPS in production environments
- Regularly update dependencies for security patches
- Configure proper CORS settings for production