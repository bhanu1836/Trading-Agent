// This file contains a content script that interacts with the TradingView website.
// It listens for messages from the popup, processes natural language commands,
// and performs actions on the TradingView page based on the AI's responses.

class TradingViewInterface {
    constructor() {
        this.agent_url = 'http://localhost:8000'; // Your Python backend
        this.initializeInterface();
    }

    initializeInterface() {
        // Create floating chat interface
        this.createChatWidget();
        // Monitor page changes
        this.observePageChanges();
    }

    async sendCommand(command) {
        const pageContext = this.extractPageContext();
        
        try {
            const response = await fetch(`${this.agent_url}/process_command`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    command: command,
                    page_context: pageContext
                })
            });
            
            const result = await response.json();
            this.executeActions(result.actions);
            return result.response;
        } catch (error) {
            console.error('Agent communication error:', error);
            return 'Sorry, I cannot connect to the trading assistant.';
        }
    }

    extractPageContext() {
        return {
            url: window.location.href,
            current_symbol: this.getCurrentSymbol(),
            watchlist_items: this.getWatchlistItems(),
            chart_timeframe: this.getChartTimeframe(),
            page_type: this.getPageType()
        };
    }

    getCurrentSymbol() {
        // Extract current symbol from TradingView
        const symbolElement = document.querySelector('[data-name="legend-source-title"]');
        return symbolElement ? symbolElement.textContent : null;
    }

    getWatchlistItems() {
        const items = document.querySelectorAll('[data-symbol]');
        return Array.from(items).map(item => item.dataset.symbol);
    }

    executeActions(actions) {
        actions.forEach(action => {
            setTimeout(() => {
                switch(action.type) {
                    case 'click':
                        this.clickElement(action.selector);
                        break;
                    case 'type':
                        this.typeText(action.selector, action.text);
                        break;
                    case 'scroll':
                        this.scrollToElement(action.selector);
                        break;
                }
            }, action.delay || 500);
        });
    }
}

// Initialize when TradingView loads
if (window.location.hostname.includes('tradingview.com')) {
    const tvInterface = new TradingViewInterface();
}