from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import json

load_dotenv()

TRADINGVIEW_SELECTORS = {
    'search_box': '[data-name="symbol-search-input"]',
    'chart_timeframes': '[data-value="1h"], [data-value="4h"], [data-value="1D"]',
    'watchlist_items': '[data-symbol]',
    'add_to_watchlist': '[data-name="add-symbol-to-watchlist"]',
    'chart_tools': '[data-name="drawing-toolbar"]',
    'indicators': '[data-name="indicators-toolbar"]'
}

class TradingAgent:
    def __init__(self, groq_api_key=None):
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        
        # Initialize Groq LLM with specific model
        self.llm = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name="llama3-70b-8192",
            temperature=0.1,
            max_tokens=2048
        )
        
        # Alternative: Use more powerful model for complex analysis
        self.advanced_llm = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name="llama3-70b-8192",
            temperature=0.1,
            max_tokens=4096
        )
        
        self.tools = [
            Tool(
                name="ExtractPageData",
                func=self.extract_page_data,
                description="Extract trading data from TradingView DOM elements"
            ),
            Tool(
                name="AnalyzeStocks",
                func=self.analyze_stocks,
                description="Analyze stock performance and trends"
            ),
            Tool(
                name="GenerateActions",
                func=self.generate_page_actions,
                description="Generate DOM actions to execute on TradingView page"
            )
        ]
        
        self.agent = initialize_agent(
            self.tools, 
            self.llm, 
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
            verbose=True,
            max_iterations=3
        )

    def process_command(self, command, page_context=None):
        """Process user command with page context"""
        try:
            # Create enhanced prompt with context
            enhanced_prompt = self._create_enhanced_prompt(command, page_context)
            
            # For complex queries, use advanced LLM directly
            if self._is_complex_query(command):
                response = self.advanced_llm.invoke([HumanMessage(content=enhanced_prompt)])
                return self._parse_llm_response(response.content)
            else:
                # Use agent for simpler queries
                response = self.agent.run(enhanced_prompt)
                return self._parse_agent_response(response)
                
        except Exception as e:
            return {
                "intent": "Error",
                "response": f"Sorry, I encountered an error: {str(e)}",
                "actions": [],
                "analysis": ""
            }

    def _create_enhanced_prompt(self, command, page_context):
        """Create enhanced prompt with page context"""
        context_str = json.dumps(page_context, indent=2) if page_context else "No page context available"
        
        return f"""
        You are a trading assistant helping users analyze TradingView.
        
        User Command: {command}
        Page Context: {context_str}
        
        Please provide a helpful response and suggest actions if needed.
        """

    def _is_complex_query(self, command):
        """Determine if query requires complex analysis"""
        complex_keywords = ['analyze', 'predict', 'forecast', 'strategy', 'technical analysis', 'fundamental']
        return any(keyword in command.lower() for keyword in complex_keywords)

    def _parse_llm_response(self, response_text):
        """Parse LLM response into structured format"""
        try:
            # Try to extract JSON from response
            if "{" in response_text and "}" in response_text:
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                json_str = response_text[start:end]
                return json.loads(json_str)
            else:
                # If no JSON found, return structured response
                return {
                    "intent": "General query",
                    "response": response_text,
                    "actions": [],
                    "analysis": response_text
                }
        except json.JSONDecodeError:
            return {
                "intent": "Parse error", 
                "response": response_text,
                "actions": [],
                "analysis": ""
            }

    def _parse_agent_response(self, response):
        """Parse agent response"""
        if isinstance(response, str):
            return {
                "intent": "Agent response",
                "response": response,
                "actions": [],
                "analysis": response
            }
        return response

    def extract_page_data(self, selector_info):
        """Extract data from TradingView page - mock implementation"""
        # This would normally extract real data from the page
        # For now, return mock data for testing
        mock_data = {
            "stocks": [
                {"symbol": "AAPL", "price": 185.50, "change": "+2.5%"},
                {"symbol": "GOOGL", "price": 2850.75, "change": "+1.8%"},
                {"symbol": "TSLA", "price": 250.30, "change": "+3.2%"},
                {"symbol": "MSFT", "price": 415.20, "change": "+1.1%"},
                {"symbol": "AMZN", "price": 3380.45, "change": "+2.8%"}
            ]
        }
        
        return f"Extracted data from: {selector_info}\nData: {json.dumps(mock_data, indent=2)}"

    def analyze_stocks(self, stock_data):
        """Analyze stock performance"""
        # Mock analysis - in real implementation, this would analyze the actual data
        analysis = """
        Based on current market data:
        
        Top Performing Stocks Today:
        1. TSLA - +3.2% (Strong momentum in EV sector)
        2. AMZN - +2.8% (Positive earnings outlook)
        3. AAPL - +2.5% (Strong iPhone sales)
        4. GOOGL - +1.8% (AI developments boost)
        5. MSFT - +1.1% (Cloud growth continues)
        
        Market sentiment is generally positive with tech stocks leading gains.
        """
        
        return f"Analysis of stocks: {stock_data}\n\nResult: {analysis}"

    def generate_page_actions(self, intent):
        """Generate actions to execute on TradingView page"""
        # Generate DOM actions based on intent
        actions = [
            {
                "type": "click",
                "selector": TRADINGVIEW_SELECTORS['search_box'],
                "description": "Click search box"
            },
            {
                "type": "type",
                "selector": TRADINGVIEW_SELECTORS['search_box'],
                "text": "TSLA",
                "description": "Search for Tesla stock"
            }
        ]
        
        return f"Generated actions for: {intent}\nActions: {json.dumps(actions, indent=2)}"

    def get_model_info(self):
        """Get model information"""
        return {
            "model": "llama3-70b-8192",
            "provider": "Groq",
            "status": "active"
        }