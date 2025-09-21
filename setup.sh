#!/bin/bash

# Flowbite MCP Server - Quick Setup Script
# This script automates the installation and configuration process

set -e  # Exit on any error

echo "🚀 Flowbite MCP Server - Quick Setup"
echo "===================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION found"
else
    print_error "Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null || python3 -m pip --version &> /dev/null; then
    print_status "pip found"
else
    print_warning "pip not found. Will try to install..."
    # Try to install pip
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3-pip
    elif command -v brew &> /dev/null; then
        brew install python
    else
        print_error "Cannot install pip automatically. Please install it manually."
        exit 1
    fi
fi

# Create virtual environment
echo ""
echo "📦 Setting up virtual environment..."

if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
print_status "Virtual environment created"

# Activate virtual environment
source venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
python -m pip install --upgrade pip
print_status "pip upgraded"

# Install dependencies
echo ""
echo "📚 Installing dependencies..."

# Try to install from requirements.txt
if [ -f "requirements.txt" ]; then
    print_info "Installing from requirements.txt..."
    pip install -r requirements.txt
    print_status "Dependencies installed from requirements.txt"
else
    print_info "requirements.txt not found. Installing core dependencies..."
    pip install fastmcp pydantic jinja2 beautifulsoup4
    print_status "Core dependencies installed"
fi

# Setup environment file
echo ""
echo "⚙️  Setting up configuration..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_status "Environment file created from .env.example"
    else
        print_warning ".env.example not found. Creating basic .env file..."
        cat > .env << EOF
# Flowbite MCP Server Configuration
MCP_SERVER_NAME=flowbite-mcp-server
MCP_SERVER_VERSION=0.1.0
DEBUG=false
LOG_LEVEL=INFO
EOF
        print_status "Basic .env file created"
    fi
else
    print_info ".env file already exists"
fi

# Create necessary directories
echo ""
echo "📁 Creating directories..."

mkdir -p data/components data/examples logs
print_status "Directories created"

# Run tests
echo ""
echo "🧪 Running tests..."

if [ -f "test_simplified.py" ]; then
    python test_simplified.py
    if [ $? -eq 0 ]; then
        print_status "All tests passed!"
    else
        print_warning "Some tests failed, but setup continues..."
    fi
else
    print_warning "test_simplified.py not found. Skipping tests."
fi

# Generate configuration examples
echo ""
echo "📋 Generating MCP configuration examples..."

# Get current directory
CURRENT_DIR=$(pwd)

# Claude Desktop configuration
cat > claude_desktop_config.json << EOF
{
  "mcpServers": {
    "flowbite": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "$CURRENT_DIR",
      "env": {
        "PYTHONPATH": "$CURRENT_DIR"
      }
    }
  }
}
EOF

print_status "Claude Desktop config generated: claude_desktop_config.json"

# VS Code configuration
cat > vscode_settings.json << EOF
{
  "mcp.servers": {
    "flowbite": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "$CURRENT_DIR"
    }
  }
}
EOF

print_status "VS Code config generated: vscode_settings.json"

# Docker setup
if command -v docker &> /dev/null; then
    print_info "Docker found. You can also use: docker-compose up"
fi

# Final instructions
echo ""
echo "🎉 Setup completed successfully!"
echo "================================"
echo ""
print_info "Next steps:"
echo "1. Add the MCP server to your AI assistant:"
echo ""
echo "   📱 Claude Desktop:"
echo "   - Copy contents of claude_desktop_config.json"
echo "   - Add to your Claude Desktop config file"
echo "   - Restart Claude Desktop"
echo ""
echo "   🔧 VS Code:"
echo "   - Copy contents of vscode_settings.json"  
echo "   - Add to your VS Code settings.json"
echo "   - Restart VS Code"
echo ""
echo "2. Test the integration:"
echo "   - Ask Claude: 'Vygeneruj mi primary button s textom Click me'"
echo "   - You should get Flowbite HTML code!"
echo ""
echo "3. Development commands:"
echo "   - Start server: source venv/bin/activate && python -m src.server"
echo "   - Run tests: python test_simplified.py"
echo "   - View logs: tail -f logs/server.log"
echo ""
print_status "Happy coding with Flowbite MCP Server! 🚀"

# Deactivate virtual environment
deactivate 2>/dev/null || true