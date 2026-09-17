#!/usr/bin/env bash
# Performance baseline script
# Run after: docker-compose up -d && sleep 5

echo "=== Protreptic Performance Baseline ==="
echo "Date: $(date)"
echo ""

# Test /figures endpoint
echo "Testing /figures endpoint..."
wrk -t4 -c100 -d30s http://localhost:8000/figures 2>/dev/null || echo "wrk not available or service not running"

echo ""
echo "Testing /vector/search endpoint..."
wrk -t4 -c100 -d30s -s search_post.lua http://localhost:8000/vector/search 2>/dev/null || echo "wrk not available or service not running"

# Create search_post.lua for POST requests
cat > search_post.lua << 'EOF'
wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.body = '{"query": "战略 思维", "lang": "zh", "top_k": 5}'
EOF
