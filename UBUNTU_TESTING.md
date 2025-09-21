# 🐧 MCP Server Testing na Ubuntu - Alternatívy

## 🎯 PROBLÉM: Claude Desktop nie je dostupný na Linux

**Claude Desktop** podporuje iba:
- ✅ Windows  
- ✅ macOS
- ❌ Linux/Ubuntu ❌

## 🚀 UBUNTU TESTING ALTERNATÍVY

### 1. 📱 **VS Code MCP Extensions** (Odporúčané)

Najlepšie extensions pre MCP testing:

```vscode-extensions
ms-azuretools.vscode-azure-mcp-server,automatalabs.copilot-mcp,semanticworkbenchteam.mcp-server-vscode,zebradev.mcp-server-runner,moonolgerdai.mcp-explorer
```

**Top picks:**
- **`copilot-mcp`** - Manage & install MCP servers
- **`mcp-server-runner`** - Run MCP servers locally  
- **`vscode-mcp-server`** - VSCode as MCP server
- **`mcp-explorer`** - Find & install MCP servers

### 2. 🤖 **AI Assistants s MCP Support**

AI extensions s MCP integráciou:

```vscode-extensions
saoudrizwan.claude-dev,rooveterinaryinc.roo-cline,kilocode.kilo-code,nr-codetools.agentsmith
```

**Odporúčané:**
- **`claude-dev` (Cline)** - Autonomous coding agent s MCP
- **`roo-cline`** - Whole dev team of AI agents
- **`agentsmith`** - Build AI agents using MCP

### 3. 🌐 **Web-based Testing**

```bash
# Spustenie HTTP MCP servera
python src/server.py --host 0.0.0.0 --port 8000

# Testing cez curl
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'

# Web UI pre testing  
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "generate_component",
      "arguments": {
        "component_type": "button",
        "variant": "primary",
        "props": {"text": "Test Button"}
      }
    }
  }'
```

### 4. 🐳 **Docker Container**

```dockerfile
# Dockerfile.test
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip curl wget \
    && rm -rf /var/lib/apt/lists/*

# Copy MCP server
COPY . /app
WORKDIR /app

# Install Python deps
RUN pip3 install -r requirements.txt

# Expose MCP port
EXPOSE 8000

# Start server
CMD ["python3", "src/server.py", "--port", "8000"]
```

```bash
# Build & run
docker build -f Dockerfile.test -t flowbite-mcp-test .
docker run -p 8000:8000 flowbite-mcp-test
```

### 5. 📡 **Claude.ai Web Interface**

Môžeme testovať cez Claude.ai web + ngrok tunnel:

```bash
# Install ngrok
sudo snap install ngrok

# Start MCP server
python src/server.py --port 8000

# Create tunnel  
ngrok http 8000

# Use public URL s Claude.ai web interface
```

---

## 🎯 ODPORÚČANÝ WORKFLOW PRE UBUNTU

### **FÁZA 1: VS Code MCP Setup** (10 min)
1. Nainštaluj **Cline** extension
2. Nainštaluj **MCP Server Runner**  
3. Nakonfiguruj náš Flowbite MCP server

### **FÁZA 2: Dependencies Installation** (5 min)
```bash
cd /mnt/raid1/www/flowbite-mcp
./setup.sh  # Install all dependencies
```

### **FÁZA 3: Local MCP Testing** (15 min)
```bash
# Start MCP server
python src/server.py

# Test cez VS Code Cline:
# - Generate button component
# - Validate HTML code  
# - Suggest components
```

### **FÁZA 4: Web API Testing** (10 min)
```bash
# HTTP API testing
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"method": "generate_component", "params": {...}}'
```

---

## 🚀 QUICK START

Chceš vyskúšať **MCP Server Runner** extension?

```bash
# 1. Install extension vo VS Code
code --install-extension zebradev.mcp-server-runner

# 2. Install dependencies
cd /mnt/raid1/www/flowbite-mcp
pip install fastmcp pydantic jinja2 beautifulsoup4

# 3. Start MCP server  
python src/server.py

# 4. Test v VS Code Command Palette:
# > MCP: Connect to Server
# > URL: http://localhost:8000
```

**Aké riešenie ťa zaujíma najviac?** 🤔

1. **VS Code extensions** - najjednoduchšie
2. **Web API testing** - rýchle prototyping  
3. **Docker setup** - clean environment
4. **Cline AI assistant** - advanced testing