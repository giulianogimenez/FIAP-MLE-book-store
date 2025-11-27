#!/bin/bash

# Quick Test Script for Environments
# Usage: ./scripts/test_env.sh [staging|production]

set -e

# Environment URLs
STAGING_URL="https://fiap-mle-bookstore-staging-d571c9f02bed.herokuapp.com"
PRODUCTION_URL="https://fiap-mle-bookstore-prod-d748bdd0abdc.herokuapp.com"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

if [ "$1" == "production" ]; then
    URL=$PRODUCTION_URL
    ENV="PRODUCTION 🟢"
else
    URL=$STAGING_URL
    ENV="STAGING 🔵"
fi

echo -e "${BLUE}Testing $ENV${NC}"
echo "URL: $URL"
echo ""

# Health check
echo "1. Health Check:"
curl -s "$URL/health" | python3 -m json.tool
echo ""

# Login and get token
echo "2. Login (admin):"
LOGIN_RESPONSE=$(curl -s -X POST "$URL/api/v1/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"admin123"}')

TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null || echo "")

if [ -z "$TOKEN" ]; then
    echo "❌ Login failed"
    exit 1
fi
echo "✅ Token obtained"
echo ""

# Test endpoints
echo "3. Books List:"
curl -s "$URL/api/v1/books" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool | head -20
echo ""

echo "4. Search (title=Python):"
curl -s "$URL/api/v1/books/search?title=Python" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo "5. Categories:"
curl -s "$URL/api/v1/categories" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo -e "${GREEN}✅ All tests completed for $ENV${NC}"
echo ""
echo "Swagger UI: $URL/api/v1/docs"

