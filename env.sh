#!/bin/bash

# Define the SSM parameter names
PARAMETER_NAME="test-project-env"
DB_PARAMETER_NAME="test-project-env-db"

# Fetch the SSM parameter values as string lists
PARAMETER_VALUE=$(aws ssm get-parameter --name "$PARAMETER_NAME" --query 'Parameter.Value' --output text)
DB_PARAMETER_VALUE=$(aws ssm get-parameter --name "$DB_PARAMETER_NAME" --query 'Parameter.Value' --output text)

# Split the string lists into arrays
IFS=',' read -ra VALUES <<< "$PARAMETER_VALUE"
IFS=',' read -ra DB_VALUES <<< "$DB_PARAMETER_VALUE"

# Create environment files
mkdir /home/ubuntu/test_project/env
ENV_FILE="/home/ubuntu/test_project/env/.env.prod"
DB_ENV_FILE="/home/ubuntu/test_project/env/.env.prod.db"

# Loop through the values and append them to the environment files
for value in "${VALUES[@]}"; do
  echo "$value" >> "$ENV_FILE"
done

for db_value in "${DB_VALUES[@]}"; do
  echo "$db_value" >> "$DB_ENV_FILE"
done

echo "Environment file '$ENV_FILE' has been created with values from SSM parameter '$PARAMETER_NAME'."
echo "Database environment file '$DB_ENV_FILE' has been created with values from SSM parameter '$DB_PARAMETER_NAME'."