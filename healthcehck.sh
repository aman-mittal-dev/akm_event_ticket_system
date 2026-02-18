#!/bin/bash

# Define the URL for the health check (temp container on port 8001)
HEALTH_CHECK_URL="http://localhost:8001/health"  # Health check URL for temp container on port 8001

# Perform the health check
response=$(curl -s $HEALTH_CHECK_URL)

# Check if the response contains the expected healthy status
if [[ "$response" == '{"status":"healthy"}' ]]; then
  echo "healthy"
else
  echo "unhealthy"
fi