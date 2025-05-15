class Config:
    """Configuration for the MDAS SDK"""
    API_BASE_URL = "https://mdas-api-dev.viewtrade.dev"
    DEFAULT_TIMEOUT = 30  # seconds
    
    @staticmethod
    def get_api_base_url():
        """Get the API base URL"""
        return Config.API_BASE_URL
    
    @staticmethod
    def get_default_timeout():
        """Get the default request timeout"""
        return Config.DEFAULT_TIMEOUT
