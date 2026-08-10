#!/bin/bash

# Run the Docker container
echo "Starting Referral Management Platform..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Using example configuration."
    echo "Please create .env file with your API keys for full functionality."
fi

# Run with docker-compose
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✓ Container started successfully"
    echo ""
    echo "Application is running at: http://localhost:8000"
    echo "API Documentation: http://localhost:8000/docs"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs -f"
    echo ""
    echo "To stop:"
    echo "  docker-compose down"
else
    echo "✗ Failed to start container"
    exit 1
fi
