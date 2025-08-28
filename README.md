# AI Trading Assistant Chrome Extension Developed By BHANU

An intelligent Chrome extension that integrates with TradingView to provide AI-powered trading insights and automation using LangChain and Groq LLM.

## 🚀 Features

- **Natural Language Trading Commands**: Interact with TradingView using plain English
- **Real-time Stock Analysis**: Get AI-powered insights on stock performance
- **Automated TradingView Actions**: Execute actions on TradingView pages automatically
- **Smart Watchlist Management**: Add/remove stocks from watchlists intelligently
- **Technical Analysis Support**: Request technical indicators and chart analysis

## 📸 Screenshots

### Extension Popup Interface
![Extension Popup](https://github.com/bhanu1836/Trading-Agent/blob/main/screenshots/Screenshot%20(93).png)
*The main interface where users enter trading commands*

### Backend Server Running
![Backend Server](https://github.com/bhanu1836/Trading-Agent/blob/main/screenshots/Screenshot%20(92).png)
*Backend server successfully running and processing requests*

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Chrome Browser
- Groq API Key ([Get one here](https://console.groq.com/))

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-trading-assistant-extension
   ```

2. **Create virtual environment**
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file in backend directory
   echo GROQ_API_KEY=your_groq_api_key_here > .env
   ```

5. **Start the backend server**
   ```bash
   python src/main.py
   ```
   Server will run on `http://localhost:8000`

### Chrome Extension Setup

1. **Open Chrome Extensions**
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode" (top-right toggle)

2. **Load the extension**
   - Click "Load unpacked"
   - Select the `extension` folder from this project
   - The extension icon should appear in your Chrome toolbar

3. **Verify installation**
   - Click the extension icon
   - Click "Test Backend Connection"
   - Should show "✓ Backend connected"

## 🎯 Usage

### Basic Commands

1. **Stock Analysis**
   ```
   "Find the best performing stocks today"
   "Analyze Apple stock technical indicators"
   "Show me Tesla's price chart"
   ```

2. **Watchlist Management**
   ```
   "Add Bitcoin to my watchlist"
   "Remove AAPL from watchlist"
   "Show my current watchlist"
   ```

3. **Chart Operations**
   ```
   "Switch to 1-hour timeframe"
   "Add RSI indicator to chart"
   "Show me support and resistance levels"
   ```

### Using the Extension

1. **Navigate to TradingView**
   - Go to [tradingview.com](https://tradingview.com)

2. **Open the Extension**
   - Click the extension icon in Chrome toolbar

3. **Enter Commands**
   - Type your trading question or command
   - Click "Submit Command"
   - View AI-generated response

4. **Automated Actions**
   - The extension will automatically execute relevant actions on the TradingView page

## 📁 Project Structure

```
ai-trading-assistant-extension/
├── backend/
│   ├── src/
│   │   ├── agents/
│   │   │   └── trading_agent.py    # Main AI agent
│   │   ├── api/
│   │   │   └── routes.py           # API routes
│   │   ├── services/
│   │   │   ├── groq_service.py     # Groq LLM integration
│   │   │   └── langchain_service.py # LangChain utilities
│   │   └── main.py                 # Flask server
│   ├── requirements.txt
│   └── .env                        # Environment variables
├── extension/
│   ├── manifest.json              # Extension configuration
│   ├── popup/
│   │   ├── popup.html             # Extension popup UI
│   │   ├── popup.js               # Popup logic
│   │   └── popup.css              # Popup styling
│   ├── content/
│   │   └── content.js             # TradingView page interaction
│   ├── background/
│   │   └── background.js          # Background service worker
│   └── icons/
│       └── icon.png               # Extension icon
└── screenshots/                    # Documentation images
    ├── popup.png
    └── backend.png
```

## 🔧 Configuration

### Environment Variables

```bash
# Backend/.env
GROQ_API_KEY=your_groq_api_key_here
```

### Supported TradingView Selectors

The extension targets these TradingView elements:
- Search box: `[data-name="symbol-search-input"]`
- Chart timeframes: `[data-value="1h"], [data-value="4h"], [data-value="1D"]`
- Watchlist items: `[data-symbol]`
- Add to watchlist: `[data-name="add-symbol-to-watchlist"]`

## 🚨 Troubleshooting

### Common Issues

1. **"Cannot connect to backend" error**
   - Ensure backend server is running on port 8000
   - Check if GROQ_API_KEY is set correctly
   - Verify Chrome allows localhost connections

2. **Extension not loading**
   - Check manifest.json syntax
   - Reload extension in Chrome extensions page
   - Check browser console for errors

3. **Commands not working**
   - Verify you're on TradingView website
   - Check extension permissions in Chrome
   - Test backend connection first

### Debug Mode

1. **Enable backend debugging**
   ```bash
   # Backend runs in debug mode by default
   python src/main.py
   ```

2. **Check extension console**
   - Right-click extension popup → "Inspect"
   - Check Console tab for errors

3. **Monitor backend logs**
   - Backend console shows all requests and responses
   - Check for any error messages

## 📊 API Endpoints

- `GET /health` - Check backend status
- `GET /test` - Test connection
- `POST /process_command` - Process trading commands

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Groq Console](https://console.groq.com/)
- [TradingView](https://tradingview.com)
- [Chrome Extension Developer Guide](https://developer.chrome.com/docs/extensions/)
- [LangChain Documentation](https://python.langchain.com/)

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Always do your own research before making trading decisions. The developers are not responsible for any financial losses.
