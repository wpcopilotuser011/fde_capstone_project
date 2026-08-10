#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t referral-management-platform:latest .

if [ $? -eq 0 ]; then
    echo "✓ Docker image built successfully"
    echo ""
    echo "To run the container:"
    echo "  docker run -p 8000:8000 referral-management-platform:latest"
    echo ""
    echo "Or use docker-compose:"
    echo "  docker-compose up -d"
else
    echo "✗ Docker build failed"
    exit 1
fi
