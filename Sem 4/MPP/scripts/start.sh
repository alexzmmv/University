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
TASK_FAMILY=${TASK_FAMILY:-"coffee-addict"}

echo -e "${YELLOW}Starting Coffee Addict Application on AWS ECS...${NC}"

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
    echo -e "${YELLOW}Please run the full deployment script first: ./deploy.sh${NC}"
    exit 1
fi

# Get the latest task definition
echo -e "${YELLOW}Getting the latest task definition...${NC}"
TASK_DEF=$(aws ecs describe-task-definition --task-definition "$TASK_FAMILY" --region "$AWS_REGION" 2>/dev/null)

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Task definition $TASK_FAMILY not found.${NC}"
    echo -e "${YELLOW}Please run the full deployment script first: ./deploy.sh${NC}"
    exit 1
fi

TASK_DEF_ARN=$(echo "$TASK_DEF" | jq -r '.taskDefinition.taskDefinitionArn')

# Update service to set desired count to 1
echo -e "${YELLOW}Starting the service with desired count 1...${NC}"
aws ecs update-service --cluster "$CLUSTER_NAME" --service "$SERVICE_NAME" --task-definition "$TASK_DEF_ARN" --desired-count 1 --region "$AWS_REGION" > /dev/null

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to start service. Check AWS credentials and permissions.${NC}"
    exit 1
fi

echo -e "${GREEN}Successfully set desired task count to 1.${NC}"
echo -e "${YELLOW}Waiting for service to stabilize...${NC}"

# Wait for service to stabilize
aws ecs wait services-stable --cluster "$CLUSTER_NAME" --services "$SERVICE_NAME" --region "$AWS_REGION"

# Get task info
echo -e "${YELLOW}Getting task information...${NC}"
TASK_ARN=$(aws ecs list-tasks --cluster "$CLUSTER_NAME" --service-name "$SERVICE_NAME" --region "$AWS_REGION" --query "taskArns[0]" --output text)

if [[ "$TASK_ARN" == "None" || -z "$TASK_ARN" ]]; then
    echo -e "${RED}No running tasks found for service $SERVICE_NAME.${NC}"
    exit 1
fi

echo -e "${GREEN}Task started: $TASK_ARN${NC}"

# Get the public IP of the task
echo -e "${YELLOW}Getting public IP of the task...${NC}"
ENI_ID=$(aws ecs describe-tasks --cluster "$CLUSTER_NAME" --tasks "$TASK_ARN" --region "$AWS_REGION" \
  --query "tasks[0].attachments[0].details[?name=='networkInterfaceId'].value" --output text)

if [ -z "$ENI_ID" ]; then
    echo -e "${RED}No network interface found for task $TASK_ARN.${NC}"
    exit 1
fi

PUBLIC_IP=$(aws ec2 describe-network-interfaces --network-interface-ids "$ENI_ID" --region "$AWS_REGION" \
  --query "NetworkInterfaces[0].Association.PublicIp" --output text)

if [[ "$PUBLIC_IP" == "None" || -z "$PUBLIC_IP" ]]; then
    echo -e "${RED}No public IP found for task $TASK_ARN.${NC}"
    exit 1
fi

echo -e "${GREEN}Coffee Addict application is now running!${NC}"
echo -e "${GREEN}Application is available at:${NC}"
echo -e "${YELLOW}Backend: http://$PUBLIC_IP:8000${NC}"
echo -e "${YELLOW}Frontend: http://$PUBLIC_IP:3000${NC}"

# Create a helper script for AWS CloudWatch logs
LOG_GROUP="/ecs/coffee-addict"
TASK_ID=$(echo "$TASK_ARN" | awk -F '/' '{print $3}')

echo -e "${YELLOW}To view logs, use:${NC}"
echo -e "${GREEN}Backend logs:${NC} aws logs get-log-events --log-group-name $LOG_GROUP --log-stream-name backend/coffee-addict/$TASK_ID --region $AWS_REGION"
echo -e "${GREEN}Frontend logs:${NC} aws logs get-log-events --log-group-name $LOG_GROUP --log-stream-name frontend/coffee-addict/$TASK_ID --region $AWS_REGION"

echo -e "${YELLOW}To stop the application, run: ./scripts/stop.sh${NC}"