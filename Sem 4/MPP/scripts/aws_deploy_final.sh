#!/bin/bash

#================================================================
# COFFEE ADDICT - AWS DEPLOYMENT SCRIPT
#================================================================
# This script handles the complete deployment of the Coffee Addict 
# application to AWS ECS, including fixing the backend startup issue
#================================================================

# Text colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

#================================================================
# CONFIGURATION VARIABLES
#================================================================

# Directory paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/coffe-addict-backend"
FRONTEND_DIR="$PROJECT_ROOT/coffe-addict-frontend"
AWS_DIR="$PROJECT_ROOT/.aws"

# AWS configuration
AWS_REGION=${AWS_REGION:-"eu-central-1"}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text 2>/dev/null)
IMAGE_TAG="latest"

# ECS configuration
CLUSTER_NAME="coffee-addict-cluster"
SERVICE_NAME="coffee-addict-service"
TASK_FAMILY="coffee-addict"

# ECR repositories
BACKEND_REPO="coffee-addict-backend"
FRONTEND_REPO="coffee-addict-frontend"

# Environment variables for the application
API_BASE_URL="http://localhost:8000/"

#================================================================
# UTILITY FUNCTIONS
#================================================================

# Print a section header
print_header() {
  echo -e "\n${BLUE}==================================================================${NC}"
  echo -e "${BLUE} $1 ${NC}"
  echo -e "${BLUE}==================================================================${NC}"
}

# Print success message
print_success() {
  echo -e "${GREEN}✓ $1${NC}"
}

# Print info message
print_info() {
  echo -e "${YELLOW}→ $1${NC}"
}

# Print error message and exit
print_error() {
  echo -e "${RED}✗ ERROR: $1${NC}"
  exit 1
}

# Check if a command exists
check_command() {
  if ! command -v "$1" &> /dev/null; then
    print_error "$1 is required but not installed."
  fi
}

# Check AWS credentials
check_aws_credentials() {
  print_info "Checking AWS credentials..."
  
  if [ -z "$AWS_ACCOUNT_ID" ]; then
    print_error "AWS credentials not found or not configured. Run 'aws configure' to set up your AWS credentials."
  fi
  
  print_success "AWS credentials verified - Account ID: $AWS_ACCOUNT_ID, Region: $AWS_REGION"
}

# Create directory if it doesn't exist
create_directory() {
  if [ ! -d "$1" ]; then
    mkdir -p "$1"
    print_info "Created directory: $1"
  fi
}

# Create ECR repository if it doesn't exist
create_ecr_repository() {
  local repo_name=$1
  
  print_info "Checking if ECR repository '$repo_name' exists..."
  
  aws ecr describe-repositories --repository-names "$repo_name" --region "$AWS_REGION" &> /dev/null
  
  if [ $? -ne 0 ]; then
    print_info "Creating ECR repository '$repo_name'..."
    aws ecr create-repository --repository-name "$repo_name" --region "$AWS_REGION" &> /dev/null
    
    if [ $? -ne 0 ]; then
      print_error "Failed to create ECR repository '$repo_name'."
    fi
    
    print_success "ECR repository '$repo_name' created"
  else
    print_success "ECR repository '$repo_name' already exists"
  fi
}

# Create CloudWatch log group if it doesn't exist
create_cloudwatch_log_group() {
  local log_group_name="/ecs/coffee-addict"
  
  print_info "Checking if CloudWatch log group '$log_group_name' exists..."
  
  aws logs describe-log-groups --log-group-name-prefix "$log_group_name" --region "$AWS_REGION" --query "logGroups[?logGroupName=='$log_group_name']" --output text &> /dev/null
  
  if [ $? -ne 0 ] || [ -z "$(aws logs describe-log-groups --log-group-name-prefix "$log_group_name" --region "$AWS_REGION" --query "logGroups[?logGroupName=='$log_group_name']" --output text 2>/dev/null)" ]; then
    print_info "Creating CloudWatch log group '$log_group_name'..."
    aws logs create-log-group --log-group-name "$log_group_name" --region "$AWS_REGION" &> /dev/null
    
    if [ $? -ne 0 ]; then
      print_error "Failed to create CloudWatch log group '$log_group_name'. Check your AWS permissions."
    fi
    
    print_success "CloudWatch log group '$log_group_name' created"
  else
    print_success "CloudWatch log group '$log_group_name' already exists"
  fi
}

# Setup IAM permissions for CloudWatch logging
setup_cloudwatch_iam_permissions() {
  local execution_role_name="ecsTaskExecutionRole"
  local policy_name="CloudWatchLogsPolicy"
  
  print_info "Setting up IAM permissions for CloudWatch logging..."
  
  # Check if the execution role exists
  aws iam get-role --role-name "$execution_role_name" --region "$AWS_REGION" &> /dev/null
  
  if [ $? -ne 0 ]; then
    print_info "Creating ECS task execution role..."
    
    # Create trust policy for ECS tasks
    local trust_policy=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
)
    
    aws iam create-role --role-name "$execution_role_name" --assume-role-policy-document "$trust_policy" &> /dev/null
    
    if [ $? -ne 0 ]; then
      print_error "Failed to create ECS task execution role. Check your AWS permissions."
    fi
    
    # Attach the managed policy for ECS task execution
    aws iam attach-role-policy --role-name "$execution_role_name" --policy-arn "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy" &> /dev/null
    
    print_success "ECS task execution role created"
  else
    print_success "ECS task execution role already exists"
  fi
  
  # Create or update CloudWatch logs policy
  local logs_policy=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:$AWS_REGION:$AWS_ACCOUNT_ID:log-group:/ecs/coffee-addict*:*"
    }
  ]
}
EOF
)
  
  # Check if the policy already exists on the role
  aws iam get-role-policy --role-name "$execution_role_name" --policy-name "$policy_name" &> /dev/null
  
  if [ $? -ne 0 ]; then
    print_info "Adding CloudWatch logs policy to execution role..."
    aws iam put-role-policy --role-name "$execution_role_name" --policy-name "$policy_name" --policy-document "$logs_policy" &> /dev/null
    
    if [ $? -ne 0 ]; then
      print_error "Failed to add CloudWatch logs policy. Check your AWS permissions."
    fi
    
    print_success "CloudWatch logs policy added to execution role"
  else
    print_success "CloudWatch logs policy already exists on execution role"
  fi
}

#================================================================
# DEPLOYMENT STEPS
#================================================================

# Step 1: Fix backend Dockerfile
fix_backend_dockerfile() {
  print_header "STEP 1: Fixing Backend Dockerfile"
  
  # Check if Dockerfile exists
  if [ ! -f "$BACKEND_DIR/Dockerfile" ]; then
    print_error "Backend Dockerfile not found at $BACKEND_DIR/Dockerfile"
  fi
  
  print_info "Updating backend Dockerfile to fix startup issues..."
  
  # Create backup of original Dockerfile
  cp "$BACKEND_DIR/Dockerfile" "$BACKEND_DIR/Dockerfile.bak"
  print_info "Backup created at $BACKEND_DIR/Dockerfile.bak"
  
  # Update CMD directive to directly run uvicorn instead of using start.sh
  # This fixes the "exec format error" issue
  sed -i.tmp '/CMD/c\# Command to run the application directly\nCMD ["python", "-m", "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]' "$BACKEND_DIR/Dockerfile"
  rm -f "$BACKEND_DIR/Dockerfile.tmp"
  
  print_success "Backend Dockerfile updated to use direct command"
  print_info "This avoids the 'exec format error' issue in AWS ECS"
}

# Step 2: Build and push Docker images
build_and_push_images() {
  print_header "STEP 2: Building and Pushing Docker Images"
  
  # Login to Amazon ECR
  print_info "Logging in to Amazon ECR..."
  aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
  
  if [ $? -ne 0 ]; then
    print_error "Failed to login to Amazon ECR"
  fi
  
  print_success "Logged in to Amazon ECR"
  
  # Build and push backend image
  print_info "Building backend Docker image with platform linux/amd64..."
  cd "$BACKEND_DIR" || print_error "Failed to navigate to backend directory"
  
  docker build --platform=linux/amd64 -t "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$BACKEND_REPO:$IMAGE_TAG" .
  
  if [ $? -ne 0 ]; then
    print_error "Failed to build backend Docker image"
  fi
  
  print_success "Backend Docker image built successfully"
  
  print_info "Pushing backend Docker image to ECR..."
  docker push "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$BACKEND_REPO:$IMAGE_TAG"
  
  if [ $? -ne 0 ]; then
    print_error "Failed to push backend Docker image to ECR"
  fi
  
  print_success "Backend Docker image pushed to ECR"
  
  # Build and push frontend image
  print_info "Building frontend Docker image..."
  cd "$FRONTEND_DIR" || print_error "Failed to navigate to frontend directory"
  
  # Build frontend with proper API_BASE_URL
  docker build --platform=linux/amd64 --build-arg API_BASE_URL="$API_BASE_URL" -t "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$FRONTEND_REPO:$IMAGE_TAG" .
  
  if [ $? -ne 0 ]; then
    print_error "Failed to build frontend Docker image"
  fi
  
  print_success "Frontend Docker image built successfully"
  
  print_info "Pushing frontend Docker image to ECR..."
  docker push "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$FRONTEND_REPO:$IMAGE_TAG"
  
  if [ $? -ne 0 ]; then
    print_error "Failed to push frontend Docker image to ECR"
  fi
  
  print_success "Frontend Docker image pushed to ECR"
  
  # Return to project root
  cd "$PROJECT_ROOT" || print_error "Failed to navigate to project root"
}

# Step 3: Create or update task definition
create_or_update_task_definition() {
  print_header "STEP 3: Creating or Updating Task Definition"
  
  # Create AWS directory if it doesn't exist
  create_directory "$AWS_DIR"
  
  # Path to task definition file
  TASK_DEF_FILE="$AWS_DIR/task-definition.json"
  
  # Check if task definition file exists
  if [ -f "$TASK_DEF_FILE" ]; then
    print_info "Using existing task definition file: $TASK_DEF_FILE"
    TASK_DEF=$(cat "$TASK_DEF_FILE")
  else
    print_info "Task definition file not found, checking if task definition exists in AWS..."
    
    # Try to get existing task definition from AWS
    aws ecs describe-task-definition --task-definition "$TASK_FAMILY" --region "$AWS_REGION" &> /dev/null
    
    if [ $? -eq 0 ]; then
      print_info "Found existing task definition in AWS"
      
      # Get the current task definition without unnecessary fields
      TASK_DEF=$(aws ecs describe-task-definition --task-definition "$TASK_FAMILY" --region "$AWS_REGION" | \
        jq '.taskDefinition | del(.taskDefinitionArn, .revision, .status, .requiresAttributes, .compatibilities, .registeredAt, .registeredBy)')
      
      # Save to file for future use
      echo "$TASK_DEF" > "$TASK_DEF_FILE"
      print_info "Saved task definition to $TASK_DEF_FILE"
    else
      print_info "No existing task definition found, creating a new one..."
      
      # Create a basic task definition for Fargate
      TASK_DEF=$(cat <<EOF
{
  "family": "$TASK_FAMILY",
  "networkMode": "awsvpc",
  "executionRoleArn": "arn:aws:iam::$AWS_ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "coffee-addict-backend",
      "image": "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$BACKEND_REPO:$IMAGE_TAG",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "NODE_ENV",
          "value": "production"
        },
        {
          "name": "USE_TEMP_STORAGE",
          "value": "true"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/coffee-addict",
          "awslogs-region": "$AWS_REGION",
          "awslogs-stream-prefix": "backend"
        }
      }
    },
    {
      "name": "coffee-addict-frontend",
      "image": "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$FRONTEND_REPO:$IMAGE_TAG",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 3000,
          "hostPort": 3000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "NODE_ENV",
          "value": "production"
        },
        {
          "name": "API_BASE_URL",
          "value": "$API_BASE_URL"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/coffee-addict",
          "awslogs-region": "$AWS_REGION",
          "awslogs-stream-prefix": "frontend"
        }
      }
    }
  ],
  "requiresCompatibilities": [
    "FARGATE"
  ],
  "cpu": "512",
  "memory": "1024"
}
EOF
)
      
      # Save to file for future use
      echo "$TASK_DEF" > "$TASK_DEF_FILE"
      print_info "Created new task definition and saved to $TASK_DEF_FILE"
    fi
  fi
  
  # Update the container images in the task definition
  print_info "Updating container images in task definition..."
  
  # Update backend image
  TASK_DEF=$(echo "$TASK_DEF" | jq --arg image "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$BACKEND_REPO:$IMAGE_TAG" \
    '.containerDefinitions |= map(if .name == "coffee-addict-backend" then .image = $image else . end)')
  
  # Update frontend image
  TASK_DEF=$(echo "$TASK_DEF" | jq --arg image "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$FRONTEND_REPO:$IMAGE_TAG" \
    '.containerDefinitions |= map(if .name == "coffee-addict-frontend" then .image = $image else . end)')
  
  # Register the updated task definition
  print_info "Registering task definition with AWS ECS..."
  
  # Save updated task definition to a temporary file
  TEMP_TASK_DEF_FILE="/tmp/coffee-addict-task-def.json"
  echo "$TASK_DEF" > "$TEMP_TASK_DEF_FILE"
  
  # Register the task definition
  NEW_TASK_DEF_ARN=$(aws ecs register-task-definition --cli-input-json "file://$TEMP_TASK_DEF_FILE" --region "$AWS_REGION" | \
    jq -r '.taskDefinition.taskDefinitionArn')
  
  if [ -z "$NEW_TASK_DEF_ARN" ]; then
    print_error "Failed to register task definition"
  fi
  
  print_success "Task definition registered: $NEW_TASK_DEF_ARN"
  
  # Save the task definition ARN to a file for later use
  echo "$NEW_TASK_DEF_ARN" > "/tmp/coffee-addict-task-def-arn.txt"
}

# Step 4: Create or update ECS cluster and service
create_or_update_ecs_service() {
  print_header "STEP 4: Creating or Updating ECS Cluster and Service"
  
  # Get the task definition ARN
  NEW_TASK_DEF_ARN=$(cat "/tmp/coffee-addict-task-def-arn.txt")
  
  # Check if cluster exists
  print_info "Checking if ECS cluster '$CLUSTER_NAME' exists..."
  
  CLUSTER_EXISTS=$(aws ecs describe-clusters --clusters "$CLUSTER_NAME" --region "$AWS_REGION" --query "clusters[0].status" --output text 2>/dev/null)
  
  if [[ "$CLUSTER_EXISTS" != "ACTIVE" ]]; then
    print_info "Creating ECS cluster '$CLUSTER_NAME'..."
    
    aws ecs create-cluster --cluster-name "$CLUSTER_NAME" --region "$AWS_REGION" > /dev/null
    
    if [ $? -ne 0 ]; then
      print_error "Failed to create ECS cluster '$CLUSTER_NAME'"
    fi
    
    print_success "ECS cluster '$CLUSTER_NAME' created"
  else
    print_success "ECS cluster '$CLUSTER_NAME' already exists"
  fi
  
  # Check if service exists
  print_info "Checking if ECS service '$SERVICE_NAME' exists..."
  
  SERVICE_EXISTS=$(aws ecs describe-services --cluster "$CLUSTER_NAME" --services "$SERVICE_NAME" --region "$AWS_REGION" --query "services[0].status" --output text 2>/dev/null)
  
  if [[ "$SERVICE_EXISTS" != "ACTIVE" ]]; then
    print_info "ECS service '$SERVICE_NAME' does not exist"
    print_info "To create a new service, you need subnet IDs and security group IDs"
    print_info "Please enter these values or press Enter to skip service creation"
    
    # Get subnet IDs
    read -p "Enter subnet ID(s) (comma-separated): " SUBNETS
    
    if [ -z "$SUBNETS" ]; then
      print_info "Subnet IDs not provided, skipping service creation"
      print_info "You will need to create the service manually in the AWS Console"
      return
    fi
    
    # Get security group IDs
    read -p "Enter security group ID(s) (comma-separated): " SECURITY_GROUPS
    
    if [ -z "$SECURITY_GROUPS" ]; then
      print_info "Security group IDs not provided, skipping service creation"
      print_info "You will need to create the service manually in the AWS Console"
      return
    fi
    
    # Convert comma-separated values to JSON arrays
    SUBNETS_JSON="$(echo $SUBNETS | sed 's/,/","/g' | sed 's/^/["/' | sed 's/$/"]/')"
    SECURITY_GROUPS_JSON="$(echo $SECURITY_GROUPS | sed 's/,/","/g' | sed 's/^/["/' | sed 's/$/"]/')"
    
    # Create network configuration JSON
    NETWORK_CONFIG="{\"awsvpcConfiguration\":{\"subnets\":$SUBNETS_JSON,\"securityGroups\":$SECURITY_GROUPS_JSON,\"assignPublicIp\":\"ENABLED\"}}"
    
    print_info "Creating ECS service '$SERVICE_NAME'..."
    
    # Create the service
    aws ecs create-service \
      --cluster "$CLUSTER_NAME" \
      --service-name "$SERVICE_NAME" \
      --task-definition "$NEW_TASK_DEF_ARN" \
      --desired-count 1 \
      --launch-type "FARGATE" \
      --network-configuration "$NETWORK_CONFIG" \
      --region "$AWS_REGION" > /dev/null
    
    if [ $? -ne 0 ]; then
      print_error "Failed to create ECS service '$SERVICE_NAME'"
    fi
    
    print_success "ECS service '$SERVICE_NAME' created"
  else
    print_info "Updating ECS service '$SERVICE_NAME'..."
    
    # Update the service to use the new task definition
    aws ecs update-service \
      --cluster "$CLUSTER_NAME" \
      --service "$SERVICE_NAME" \
      --task-definition "$NEW_TASK_DEF_ARN" \
      --region "$AWS_REGION" > /dev/null
    
    if [ $? -ne 0 ]; then
      print_error "Failed to update ECS service '$SERVICE_NAME'"
    fi
    
    print_success "ECS service '$SERVICE_NAME' updated"
  fi
  
  # Wait for service to stabilize
  print_info "Waiting for service to stabilize (this may take a few minutes)..."
  aws ecs wait services-stable --cluster "$CLUSTER_NAME" --services "$SERVICE_NAME" --region "$AWS_REGION"
  
  print_success "ECS service is now stable"
}

# Step 5: Get the application URL
get_application_url() {
  print_header "STEP 5: Getting Application URL"
  
  print_info "Getting task information..."
  
  # Get the latest task ARN
  TASK_ARN=$(aws ecs list-tasks --cluster "$CLUSTER_NAME" --service-name "$SERVICE_NAME" --region "$AWS_REGION" --query "taskArns[0]" --output text)
  
  if [[ "$TASK_ARN" == "None" || -z "$TASK_ARN" ]]; then
    print_info "No running tasks found"
    print_info "The service might still be starting up"
    print_info "Check the AWS Console for more information"
    return
  fi
  
  print_info "Found task: $TASK_ARN"
  
  # Get the network interface ID
  print_info "Getting network interface ID..."
  ENI_ID=$(aws ecs describe-tasks --cluster "$CLUSTER_NAME" --tasks "$TASK_ARN" --region "$AWS_REGION" --query "tasks[0].attachments[0].details[?name=='networkInterfaceId'].value" --output text)
  
  if [ -z "$ENI_ID" ]; then
    print_info "No network interface found for task"
    print_info "Check the AWS Console for more information"
    return
  fi
  
  print_info "Found network interface: $ENI_ID"
  
  # Get the public IP address
  print_info "Getting public IP address..."
  PUBLIC_IP=$(aws ec2 describe-network-interfaces --network-interface-ids "$ENI_ID" --region "$AWS_REGION" --query "NetworkInterfaces[0].Association.PublicIp" --output text)
  
  if [[ "$PUBLIC_IP" == "None" || -z "$PUBLIC_IP" ]]; then
    print_info "No public IP address found for network interface"
    print_info "Check the AWS Console for more information"
    return
  fi
  
  # Display the URLs
  echo -e "\n${GREEN}==================================================================${NC}"
  echo -e "${GREEN}              COFFEE ADDICT APPLICATION DEPLOYED!                 ${NC}"
  echo -e "${GREEN}==================================================================${NC}"
  echo -e "${YELLOW}  Frontend URL: ${GREEN}http://$PUBLIC_IP:3000${NC}"
  echo -e "${YELLOW}  Backend URL:  ${GREEN}http://$PUBLIC_IP:8000${NC}"
  echo -e "${GREEN}==================================================================${NC}"
  
  # Save URLs to a file
  URL_FILE="$PROJECT_ROOT/coffee-addict-urls.txt"
  echo "Frontend URL: http://$PUBLIC_IP:3000" > "$URL_FILE"
  echo "Backend URL: http://$PUBLIC_IP:8000" >> "$URL_FILE"
  
  print_info "URLs have been saved to: $URL_FILE"
}

#================================================================
# MAIN SCRIPT
#================================================================

# Display banner
echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}                  COFFEE ADDICT AWS DEPLOYMENT                    ${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo -e "${YELLOW}This script will:${NC}"
echo -e "${YELLOW}  1. Fix the backend Dockerfile to prevent startup issues${NC}"
echo -e "${YELLOW}  2. Build and push Docker images to Amazon ECR${NC}"
echo -e "${YELLOW}  3. Create or update the ECS task definition${NC}"
echo -e "${YELLOW}  4. Create or update the ECS cluster and service${NC}"
echo -e "${YELLOW}  5. Get the application URL${NC}"
echo -e "${BLUE}==================================================================${NC}"

# Ask for confirmation
read -p "Do you want to continue? (y/n): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo -e "${YELLOW}Deployment cancelled.${NC}"
  exit 0
fi

# Check for required tools
print_info "Checking for required tools..."
check_command "aws"
check_command "docker"
check_command "jq"
print_success "All required tools are installed"

# Check AWS credentials
check_aws_credentials

# Create ECR repositories
create_ecr_repository "$BACKEND_REPO"
create_ecr_repository "$FRONTEND_REPO"

# Setup CloudWatch logging
create_cloudwatch_log_group
setup_cloudwatch_iam_permissions

# Run deployment steps
fix_backend_dockerfile
build_and_push_images
create_or_update_task_definition
create_or_update_ecs_service
get_application_url

# Display completion message
echo -e "\n${BLUE}==================================================================${NC}"
echo -e "${GREEN}                DEPLOYMENT COMPLETED SUCCESSFULLY!                ${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo -e "${YELLOW}To stop the application:${NC}"
echo -e "${GREEN}aws ecs update-service --cluster \"$CLUSTER_NAME\" --service \"$SERVICE_NAME\" --desired-count 0 --region \"$AWS_REGION\"${NC}"
echo -e "${BLUE}==================================================================${NC}"
