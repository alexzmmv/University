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

# Call the function to create the log group
create_cloudwatch_log_group
