#!/bin/bash

# SecureBank Financial Services - Frontend Docker Run Script

echo "🏦 Running SecureBank Financial Services Frontend Container"
echo "=========================================================="

# Set variables
IMAGE_NAME="securebank-frontend"
IMAGE_TAG="latest"
CONTAINER_NAME="securebank-frontend-container"
HOST_PORT="3000"
CONTAINER_PORT="80"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Run Configuration:${NC}"
echo "   Image: $IMAGE_NAME:$IMAGE_TAG"
echo "   Container: $CONTAINER_NAME"
echo "   Port Mapping: $HOST_PORT:$CONTAINER_PORT"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Check if image exists
if ! docker images --format 'table {{.Repository}}:{{.Tag}}' | grep -q "^$IMAGE_NAME:$IMAGE_TAG$"; then
    echo -e "${RED}❌ Docker image $IMAGE_NAME:$IMAGE_TAG not found!${NC}"
    echo -e "${YELLOW}💡 Please build the image first by running: ./build-docker.sh${NC}"
    exit 1
fi

# Stop and remove existing container if it exists
if docker ps -a --format 'table {{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    echo -e "${YELLOW}🔄 Stopping existing container...${NC}"
    docker stop $CONTAINER_NAME > /dev/null 2>&1
    echo -e "${YELLOW}🔄 Removing existing container...${NC}"
    docker rm $CONTAINER_NAME > /dev/null 2>&1
fi

echo -e "${YELLOW}🔄 Starting new container...${NC}"

# Run the container
if docker run -d \
    --name $CONTAINER_NAME \
    -p $HOST_PORT:$CONTAINER_PORT \
    --restart unless-stopped \
    $IMAGE_NAME:$IMAGE_TAG; then
    
    echo -e "${GREEN}✅ Container started successfully!${NC}"
    
    # Wait a moment for container to start
    sleep 3
    
    # Check container status
    if docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -q "^$CONTAINER_NAME"; then
        echo -e "${GREEN}✅ Container is running!${NC}"
        
        # Test health endpoint
        echo -e "${YELLOW}🔄 Testing health endpoint...${NC}"
        sleep 2
        
        if curl -s http://localhost:$HOST_PORT/health > /dev/null; then
            echo -e "${GREEN}✅ Health check passed!${NC}"
        else
            echo -e "${YELLOW}⚠️  Health check failed (container may still be starting)${NC}"
        fi
        
        echo ""
        echo -e "${GREEN}🎉 Frontend is now running in Docker!${NC}"
        echo ""
        echo -e "${BLUE}📋 Container Information:${NC}"
        docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        
        echo ""
        echo -e "${BLUE}🌐 Access Points:${NC}"
        echo "   Frontend App: http://localhost:$HOST_PORT"
        echo "   Health Check: http://localhost:$HOST_PORT/health"
        
        echo ""
        echo -e "${BLUE}📋 Useful Commands:${NC}"
        echo "   View logs: docker logs $CONTAINER_NAME"
        echo "   Follow logs: docker logs -f $CONTAINER_NAME"
        echo "   Stop container: docker stop $CONTAINER_NAME"
        echo "   Restart container: docker restart $CONTAINER_NAME"
        echo "   Remove container: docker rm $CONTAINER_NAME"
        
    else
        echo -e "${RED}❌ Container failed to start properly!${NC}"
        echo -e "${YELLOW}📋 Check logs with: docker logs $CONTAINER_NAME${NC}"
        exit 1
    fi
    
else
    echo -e "${RED}❌ Failed to start container!${NC}"
    exit 1
fi
