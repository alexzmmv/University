#!/bin/bash

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# AWS Configuration
AWS_REGION=${AWS_REGION:-"eu-central-1"}
CLUSTER_NAME=${CLUSTER_NAME:-"coffee-addict-cluster"}
SERVICE_NAME=${SERVICE_NAME:-"coffee-addict-service"}

echo -e "${YELLOW}Stopping Coffee Addict Application on AWS ECS...${NC}"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI is required but not installed.${NC}"
    exit 1
fi

# Check if the service exists
echo -e "${YELLOW}Checking if service exists...${NC}"
SERVICE_EXISTS=$(aws ecs describe-services --cluster "$CLUSTER_NAME" --services "$SERVICE_NAME" --region "$AWS_REGION" --query "services[0].status" --output text 2>/dev/null)

if [[ "$SERVICE_EXISTS" != "ACTIVE" ]]; then
    echo -e "${RED}Service $SERVICE_NAME does not exist in cluster $CLUSTER_NAME.${NC}"
    exit 1
fi

# Update service to set desired count to 0
echo -e "${YELLOW}Setting desired task count to 0...${NC}"
aws ecs update-service --cluster "$CLUSTER_NAME" --service "$SERVICE_NAME" --desired-count 0 --region "$AWS_REGION" > /dev/null

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to update service. Check AWS credentials and permissions.${NC}"
    exit 1
fi

echo -e "${GREEN}Successfully set desired task count to 0.${NC}"
echo -e "${YELLOW}Waiting for tasks to stop...${NC}"

# Wait for tasks to stop
aws ecs wait services-stable --cluster "$CLUSTER_NAME" --services "$SERVICE_NAME" --region "$AWS_REGION"

# Verify no tasks are running
RUNNING_TASKS=$(aws ecs list-tasks --cluster "$CLUSTER_NAME" --service-name "$SERVICE_NAME" --region "$AWS_REGION" --query "taskArns" --output text)

if [[ "$RUNNING_TASKS" == "None" || -z "$RUNNING_TASKS" ]]; then
    echo -e "${GREEN}Application stopped successfully. No tasks are running.${NC}"
else
    echo -e "${YELLOW}Warning: Some tasks might still be running.${NC}"
fi

echo -e "${GREEN}Coffee Addict application on AWS ECS has been stopped.${NC}"
echo -e "${YELLOW}To start the application again, run: ./scripts/start.sh${NC}"