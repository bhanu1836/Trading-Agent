import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', 'your_groq_api_key')
    LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY', 'your_langchain_api_key')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', 5000))