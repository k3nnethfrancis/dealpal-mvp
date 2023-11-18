# base.py
import os
import yaml
import dotenv
import logging
import functools
from pydantic_settings import BaseSettings
from openai import OpenAI, AsyncOpenAI
from langchain.utilities import SearchApiAPIWrapper



class Settings(BaseSettings):
    OPENAI_API_KEY: str
    SEARCHAPI_API_KEY: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

class BaseConfig:
    def __init__(self, name, log_file=None):
        # Set up logger
        self.logger = self.setup_logger(name, log_file)

        # Load API keys
        settings = Settings()
        self.OPENAI_API_KEY = settings.OPENAI_API_KEY
        self.SEARCHAPI_API_KEY = settings.SEARCHAPI_API_KEY

        # Set up paths
        self.AGENT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "agents")
        self.ARI_CONFIG_PATH = os.path.join(self.AGENT_CONFIG_PATH, "ari.yaml")

        # Load Ari assistant ID from yaml config
        with open(self.ARI_CONFIG_PATH, "r") as f:
            ari_config = yaml.safe_load(f)

        self.ASSISTANT_ID = ari_config.get("ID")


    def setup_logger(self, name, log_file=None):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)

        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)

        logger.addHandler(c_handler)

        if log_file is None:
            parent_dir = os.path.basename(os.path.dirname(__file__))
            file_name, _ = os.path.splitext(os.path.basename(__file__))  # Split the file name and the extension
            log_file = f"{parent_dir}-{file_name}.log"  # Use just the file name for the log file name
        
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'log')
        os.makedirs(log_dir, exist_ok=True)  # Create log directory if it doesn't exist

        log_file_path = os.path.join(log_dir, log_file)
        f_handler = logging.FileHandler(log_file_path)
        f_handler.setLevel(logging.DEBUG)

        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)

        logger.addHandler(f_handler)

        return logger

    def _logger(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(f'Running {func.__name__} with args: {args} and kwargs: {kwargs}')
            result = func(*args, **kwargs)
            self.logger.info(f'{func.__name__} returned: {result}')
            return result
        return wrapper
    
    def get_openai_client(self):
        return OpenAI(api_key=self.OPENAI_API_KEY)

    def get_async_openai_client(self):
        return AsyncOpenAI(api_key=self.OPENAI_API_KEY)  # Return the asynchronous client

    def get_search_client(self):
        return SearchApiAPIWrapper(searchapi_api_key=self.SEARCHAPI_API_KEY)