#!/bin/bash

# SecureBank Financial Services - Frontend Docker Build Script

echo "🏦 Building SecureBank Financial Services Frontend Docker Image"
echo "=============================================================="

# Set variables
IMAGE_NAME="securebank-frontend"
IMAGE_TAG="latest"
CONTAINER_NAME="securebank-frontend-container"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Build Configuration:${NC}"
echo "   Image Name: $IMAGE_NAME"
echo "   Image Tag: $IMAGE_TAG"
echo "   Container Name: $CONTAINER_NAME"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

echo -e "${YELLOW}🔄 Step 1: Cleaning up existing containers and images...${NC}"
# Stop and remove existing container if it exists
if docker ps -a --format 'table {{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    echo "   Stopping existing container..."
    docker stop $CONTAINER_NAME > /dev/null 2>&1
    echo "   Removing existing container..."
    docker rm $CONTAINER_NAME > /dev/null 2>&1
fi

# Remove existing image if it exists
if docker images --format 'table {{.Repository}}:{{.Tag}}' | grep -q "^$IMAGE_NAME:$IMAGE_TAG$"; then
    echo "   Removing existing image..."
    docker rmi $IMAGE_NAME:$IMAGE_TAG > /dev/null 2>&1
fi

echo -e "${YELLOW}🔄 Step 2: Building Docker image...${NC}"
echo "   This may take a few minutes..."

# Build the Docker image
if docker build -t $IMAGE_NAME:$IMAGE_TAG .; then
    echo -e "${GREEN}✅ Docker image built successfully!${NC}"
else
    echo -e "${RED}❌ Docker image build failed!${NC}"
    exit 1
fi

echo -e "${YELLOW}🔄 Step 3: Displaying image information...${NC}"
docker images $IMAGE_NAME:$IMAGE_TAG

echo ""
echo -e "${GREEN}🎉 Frontend Docker image is ready!${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "   1. Run the container:"
echo "      docker run -d -p 3000:80 --name $CONTAINER_NAME $IMAGE_NAME:$IMAGE_TAG"
echo ""
echo "   2. Test the application:"
echo "      curl http://localhost:3000/health"
echo ""
echo "   3. View logs:"
echo "      docker logs $CONTAINER_NAME"
echo ""
echo "   4. Stop the container:"
echo "      docker stop $CONTAINER_NAME"
echo ""
echo "   5. Remove the container:"
echo "      docker rm $CONTAINER_NAME"
echo ""
echo -e "${BLUE}🌐 Once running, access the app at: http://localhost:3000${NC}"
