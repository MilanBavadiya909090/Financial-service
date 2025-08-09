#!/bin/bash

# SecureBank Financial Services - Frontend Docker Management Script

IMAGE_NAME="securebank-frontend"
IMAGE_TAG="latest"
CONTAINER_NAME="securebank-frontend-container"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_usage() {
    echo "🏦 SecureBank Financial Services - Frontend Docker Management"
    echo "============================================================"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build the Docker image"
    echo "  run       Run the Docker container"
    echo "  stop      Stop the running container"
    echo "  restart   Restart the container"
    echo "  logs      Show container logs"
    echo "  status    Show container status"
    echo "  clean     Remove container and image"
    echo "  health    Check application health"
    echo "  shell     Open shell in running container"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build && $0 run    # Build and run"
    echo "  $0 logs -f            # Follow logs"
    echo "  $0 status             # Check status"
}

build_image() {
    echo -e "${YELLOW}🔄 Building Docker image...${NC}"
    ./build-docker.sh
}

run_container() {
    echo -e "${YELLOW}🔄 Running Docker container...${NC}"
    ./run-docker.sh
}

stop_container() {
    echo -e "${YELLOW}🔄 Stopping container...${NC}"
    if docker stop $CONTAINER_NAME > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Container stopped successfully!${NC}"
    else
        echo -e "${RED}❌ Failed to stop container or container not running${NC}"
    fi
}

restart_container() {
    echo -e "${YELLOW}🔄 Restarting container...${NC}"
    if docker restart $CONTAINER_NAME > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Container restarted successfully!${NC}"
        sleep 2
        check_health
    else
        echo -e "${RED}❌ Failed to restart container${NC}"
    fi
}

show_logs() {
    echo -e "${BLUE}📋 Container logs:${NC}"
    if [ "$2" = "-f" ]; then
        docker logs -f $CONTAINER_NAME
    else
        docker logs $CONTAINER_NAME
    fi
}

show_status() {
    echo -e "${BLUE}📋 Container Status:${NC}"
    if docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -q "$CONTAINER_NAME"; then
        docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        echo ""
        echo -e "${GREEN}✅ Container is running${NC}"
    else
        echo -e "${RED}❌ Container is not running${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}📋 Image Information:${NC}"
    docker images $IMAGE_NAME:$IMAGE_TAG
}

clean_all() {
    echo -e "${YELLOW}🔄 Cleaning up container and image...${NC}"
    
    # Stop and remove container
    if docker ps -a --format 'table {{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
        docker stop $CONTAINER_NAME > /dev/null 2>&1
        docker rm $CONTAINER_NAME > /dev/null 2>&1
        echo -e "${GREEN}✅ Container removed${NC}"
    fi
    
    # Remove image
    if docker images --format 'table {{.Repository}}:{{.Tag}}' | grep -q "^$IMAGE_NAME:$IMAGE_TAG$"; then
        docker rmi $IMAGE_NAME:$IMAGE_TAG > /dev/null 2>&1
        echo -e "${GREEN}✅ Image removed${NC}"
    fi
    
    echo -e "${GREEN}✅ Cleanup completed!${NC}"
}

check_health() {
    echo -e "${YELLOW}🔄 Checking application health...${NC}"
    
    if curl -s http://localhost:3000/health > /dev/null; then
        echo -e "${GREEN}✅ Application is healthy!${NC}"
        echo "   Frontend: http://localhost:3000"
        echo "   Health: http://localhost:3000/health"
    else
        echo -e "${RED}❌ Application health check failed${NC}"
        echo -e "${YELLOW}💡 Container may still be starting or there's an issue${NC}"
    fi
}

open_shell() {
    echo -e "${YELLOW}🔄 Opening shell in container...${NC}"
    if docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}" | grep -q "$CONTAINER_NAME"; then
        docker exec -it $CONTAINER_NAME /bin/sh
    else
        echo -e "${RED}❌ Container is not running${NC}"
    fi
}

# Main script logic
case "$1" in
    build)
        build_image
        ;;
    run)
        run_container
        ;;
    stop)
        stop_container
        ;;
    restart)
        restart_container
        ;;
    logs)
        show_logs "$@"
        ;;
    status)
        show_status
        ;;
    clean)
        clean_all
        ;;
    health)
        check_health
        ;;
    shell)
        open_shell
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        if [ -z "$1" ]; then
            show_usage
        else
            echo -e "${RED}❌ Unknown command: $1${NC}"
            echo ""
            show_usage
        fi
        exit 1
        ;;
esac
