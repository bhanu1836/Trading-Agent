import os
import json
from typing import Dict, Any, List
from groq import Groq
from dotenv import load_dotenv
import requests

load_dotenv()

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.default_model = "llama3-8b-8192"
        self.advanced_model = "llama3-70b-8192"

    def check_connection(self) -> bool:
        """Check if Groq API is accessible"""
        try:
            # Simple test call
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model=self.default_model,
                max_tokens=10
            )
            return True
        except Exception as e:
            print(f"Groq connection failed: {e}")
            return False

    def analyze_page_context(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze page context with Groq AI"""
        try:
            context_prompt = f"""
Analyze this TradingView page context and extract key insights:

Context Data: {json.dumps(context_data, indent=2)}

Provide a JSON response with:
1. "key_insights": Important observations about the page
2. "tradeable_assets": List of stocks/assets found
3. "page_type": Type of TradingView page (chart, screener, portfolio, etc.)
4. "actionable_elements": UI elements that can be interacted with
5. "market_sentiment": Overall market sentiment if detectable

Return only valid JSON.
"""
            
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": context_prompt}],
                model=self.default_model,
                temperature=0.1,
                max_tokens=1024
            )
            
            result_text = response.choices[0].message.content
            
            # Try to parse JSON
            if "{" in result_text and "}" in result_text:
                start = result_text.find("{")
                end = result_text.rfind("}") + 1
                json_str = result_text[start:end]
                return json.loads(json_str)
            
            return {"analysis": result_text}
            
        except Exception as e:
            return {"error": f"Context analysis failed: {str(e)}"}

    def generate_trading_actions(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific trading actions based on prompt and context"""
        try:
            action_prompt = f"""
You are a TradingView automation assistant. Based on the user prompt and page context, generate specific DOM actions.

User Prompt: "{prompt}"
Page Context: {json.dumps(context, indent=2)}

Generate a JSON response with:
{{
  "intent": "What the user wants to do",
  "actions": [
    {{
      "type": "click|type|scroll|extract",
      "selector": "CSS selector for the element",
      "value": "text to type (if applicable)",
      "description": "What this action accomplishes",
      "wait_after": 1000
    }}
  ],
  "explanation": "Step-by-step explanation of what will happen"
}}

Available action types:
- click: Click buttons, links, chart elements
- type: Enter text in search boxes, input fields
- scroll: Scroll to make elements visible
- extract: Get data from elements

Common TradingView selectors:
- Search: "[data-name='symbol-search']", ".tv-symbol-search"
- Charts: "[data-name='chart']", ".tv-chart-container"
- Timeframes: "[data-name='time-interval']"
- Watchlist: "[data-name='watchlist-item']"
- Symbols: "[data-symbol]", ".tv-symbol-header"

Return only valid JSON.
"""
            
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": action_prompt}],
                model=self.advanced_model,
                temperature=0.1,
                max_tokens=2048
            )
            
            result_text = response.choices[0].message.content
            
            # Parse JSON response
            if "{" in result_text and "}" in result_text:
                start = result_text.find("{")
                end = result_text.rfind("}") + 1
                json_str = result_text[start:end]
                return json.loads(json_str)
            
            return {
                "intent": "Parse error",
                "actions": [],
                "explanation": result_text
            }
            
        except Exception as e:
            return {
                "intent": "Error",
                "actions": [],
                "explanation": f"Failed to generate actions: {str(e)}"
            }

    def get_available_models(self) -> List[str]:
        """Get list of available Groq models"""
        return [
            "llama3-8b-8192",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ]

    def analyze_stock_data(self, stock_data: Dict[str, Any]) -> str:
        """Analyze stock/trading data with AI"""
        try:
            analysis_prompt = f"""
Analyze this stock/trading data and provide insights:

Data: {json.dumps(stock_data, indent=2)}

Provide:
1. Key observations about price movements
2. Technical indicators analysis
3. Potential trading opportunities
4. Risk assessment
5. Actionable recommendations

Keep it concise and practical for traders.
"""
            
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": analysis_prompt}],
                model=self.advanced_model,
                temperature=0.2,
                max_tokens=1024
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Analysis failed: {str(e)}"

    def send_prompt(self, prompt: str) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt
        }
        response = requests.post(f"{self.base_url}/v1/queries", headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_market_data(self, symbol: str) -> Dict[str, Any]:
        # Example function to get market data for a specific symbol
        response = requests.get(f"{self.base_url}/v1/marketdata/{symbol}", headers={"Authorization": f"Bearer {self.api_key}"})
        response.raise_for_status()
        return response.json()