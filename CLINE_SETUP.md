# 🚀 Flowbite MCP Server - Setup Guide pre Cline Extension

## ✅ Aktuálny stav

### Čo je hotové:
1. **Simplified MCP Server** - `mcp_server_simple.py`
   - Funguje bez external dependencies
   - Obsahuje 3 main tools: generate_component, validate_component, suggest_components
   - Podporuje button, form, card komponenty s rôznymi variantmi

2. **Cline Extension** - Úspešne nainštalovaný
   - Extension ID: `saoudrizwan.claude-dev`
   - Ready pre MCP server testing

3. **Test Coverage** - 100% mock test success rate
   - Všetky komponenty testované a funkčné
   - Logic validation confirmed

## 🔧 Cline Extension Setup

### Krok 1: Konfigurácia MCP servera v Cline

V VS Code:
1. Otvor Command Palette (`Ctrl+Shift+P`)
2. Spusť: `Cline: Open MCP Settings`
3. Pridaj našu konfiguráciu:

```json
{
  "mcpServers": {
    "flowbite": {
      "command": "python3",
      "args": ["/mnt/raid1/www/flowbite-mcp/mcp_server_simple.py", "--stdio"],
      "cwd": "/mnt/raid1/www/flowbite-mcp",
      "env": {}
    }
  }
}
```

### Krok 2: Test MCP connection

1. Otvor Cline extension panel
2. Spusť prompt: "Use the flowbite MCP server to generate a primary button with text 'Click Me'"
3. Cline by mal automaticky použiť náš MCP server

## 🎯 Testing Scenarios

### Základné testy:

1. **Button Generation:**
   ```
   Generate a primary button with text "Submit Form"
   ```

2. **Form Creation:**
   ```
   Create a contact form component
   ```

3. **Component Validation:**
   ```
   Validate this HTML: <button class="bg-blue-500">Test</button>
   ```

4. **Component Suggestions:**
   ```
   Suggest components for an e-shop product page
   ```

### Pokročilé testy:

1. **Multiple Variants:**
   ```
   Generate three buttons: primary, secondary, and danger variants
   ```

2. **Custom Props:**
   ```
   Generate a card with title "Product Name" and content "Product description"
   ```

3. **Validation with Context:**
   ```
   Validate this button HTML for e-commerce use: [paste HTML]
   ```

## 📊 Available Components

### Button Component
- **Variants:** primary, secondary, danger
- **Props:** text
- **Example:** Primary blue button, secondary gray button, danger red button

### Form Component  
- **Variants:** contact
- **Props:** (none currently)
- **Example:** Email + message contact form

### Card Component
- **Variants:** basic
- **Props:** title, content
- **Example:** Product card with title and description

## 🔍 Troubleshooting

### Ak Cline nevidí MCP server:
1. Skontroluj či je `mcp_server_simple.py` executable
2. Overe path v konfigurácii
3. Reštartuj VS Code
4. Skontroluj Cline extension logs

### Ak MCP server crashes:
1. Spusť: `python3 mcp_server_simple.py` na testovanie
2. Skontroluj Python verziu (need 3.6+)
3. Pozri stderr logs

### Ak chýbajú komponenty:
1. Môžeš pridať nové do `components_db` v serveri
2. Každý komponent potrebuje HTML template a CSS classes
3. Podporované sú {{variable}} placeholders

## 🎯 Next Steps

1. **Test Basic Functionality** - Overiť že Cline komunikuje s MCP serverom
2. **Component Expansion** - Pridať ďalšie Flowbite komponenty podľa analýzy
3. **Advanced Features** - Template system, component composition
4. **Real-world Testing** - Použiť na skutočných projektoch

## 📝 Quick Commands

```bash
# Test MCP server directly
python3 mcp_server_simple.py

# Run in stdio mode (for Cline)
python3 mcp_server_simple.py --stdio

# Check if executable
ls -la mcp_server_simple.py
```

Ready pre testing! 🚀