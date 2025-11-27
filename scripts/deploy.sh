#!/bin/bash

# Deploy Script for FIAP MLE Book Store
# Usage: ./scripts/deploy.sh [staging|production]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Environment URLs
STAGING_URL="https://fiap-mle-bookstore-staging-d571c9f02bed.herokuapp.com"
PRODUCTION_URL="https://fiap-mle-bookstore-prod-d748bdd0abdc.herokuapp.com"

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to test environment
test_environment() {
    local env=$1
    local url=$2
    
    print_info "Testing $env environment..."
    
    # Test health endpoint
    echo -n "  - Health check: "
    health_response=$(curl -s "$url/health")
    if echo "$health_response" | grep -q "healthy"; then
        print_success "OK"
    else
        print_error "FAILED"
        return 1
    fi
    
    # Test login
    echo -n "  - Authentication: "
    login_response=$(curl -s -X POST "$url/api/v1/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"username":"admin","password":"admin123"}')
    
    if echo "$login_response" | grep -q "access_token"; then
        print_success "OK"
        TOKEN=$(echo "$login_response" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null || echo "")
    else
        print_error "FAILED"
        return 1
    fi
    
    # Test books endpoint
    echo -n "  - Books endpoint: "
    books_response=$(curl -s "$url/api/v1/books" -H "Authorization: Bearer $TOKEN")
    if echo "$books_response" | grep -q "books"; then
        print_success "OK"
    else
        print_error "FAILED"
        return 1
    fi
    
    # Test search endpoint
    echo -n "  - Search endpoint: "
    search_response=$(curl -s "$url/api/v1/books/search?title=Python" -H "Authorization: Bearer $TOKEN")
    if echo "$search_response" | grep -q "total"; then
        print_success "OK"
    else
        print_error "FAILED"
        return 1
    fi
    
    # Test categories endpoint
    echo -n "  - Categories endpoint: "
    categories_response=$(curl -s "$url/api/v1/categories" -H "Authorization: Bearer $TOKEN")
    if echo "$categories_response" | grep -q "categories"; then
        print_success "OK"
    else
        print_error "FAILED"
        return 1
    fi
    
    # Test Swagger
    echo -n "  - Swagger docs: "
    swagger_response=$(curl -s "$url/api/v1/docs")
    if echo "$swagger_response" | grep -q "swagger"; then
        print_success "OK"
    else
        print_error "FAILED"
        return 1
    fi
    
    print_success "All tests passed for $env!"
    return 0
}

# Main deployment logic
deploy() {
    local environment=$1
    
    if [ "$environment" != "staging" ] && [ "$environment" != "production" ]; then
        print_error "Invalid environment. Use 'staging' or 'production'"
        exit 1
    fi
    
    print_info "Starting deployment to $environment..."
    
    # Deploy to staging first
    if [ "$environment" == "production" ]; then
        print_warning "Production deployment requires staging validation first"
        print_info "Deploying to staging..."
        
        git push staging main
        
        print_info "Waiting for staging deployment to complete..."
        sleep 10
        
        if ! test_environment "STAGING" "$STAGING_URL"; then
            print_error "Staging tests failed. Aborting production deployment."
            exit 1
        fi
        
        print_warning "Staging tests passed. Ready to deploy to production."
        read -p "Do you want to continue with production deployment? (yes/no): " confirm
        
        if [ "$confirm" != "yes" ]; then
            print_warning "Production deployment cancelled."
            exit 0
        fi
        
        print_info "Deploying to production..."
        git push production main
        
        print_info "Waiting for production deployment to complete..."
        sleep 10
        
        if ! test_environment "PRODUCTION" "$PRODUCTION_URL"; then
            print_error "Production tests failed!"
            exit 1
        fi
        
        print_success "Successfully deployed to production! 🚀"
        
    else
        # Deploy to staging only
        print_info "Deploying to staging..."
        git push staging main
        
        print_info "Waiting for staging deployment to complete..."
        sleep 10
        
        if ! test_environment "STAGING" "$STAGING_URL"; then
            print_error "Staging tests failed!"
            exit 1
        fi
        
        print_success "Successfully deployed to staging! 🎯"
    fi
}

# Show usage if no arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 [staging|production]"
    echo ""
    echo "Examples:"
    echo "  $0 staging      # Deploy to staging only"
    echo "  $0 production   # Deploy to staging, test, then production"
    exit 1
fi

# Run deployment
deploy "$1"

