from langchain import OpenAI, LLMChain
from langchain.prompts import PromptTemplate

class LangchainService:
    def __init__(self, api_key):
        self.llm = OpenAI(api_key=api_key)
        self.prompt_template = PromptTemplate(
            input_variables=["command"],
            template="You are an AI trading assistant. Analyze the following command: {command}"
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def process_command(self, command):
        response = self.chain.run(command)
        return response

    def analyze_market_data(self, market_data):
        command = f"Analyze the following market data: {market_data}"
        return self.process_command(command)

    def execute_trade_action(self, action):
        command = f"Execute the following trade action: {action}"
        return self.process_command(command)