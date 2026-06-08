class TradingBotError(Exception):
    pass

class ValidationError(TradingBotError):
    pass

class AuthenticationError(TradingBotError):
    pass

class BinanceAPIError(TradingBotError):
    def __init__(self, message: str, code: int | None = None) -> None:
        super().__init__(message)
        self.code = code

class NetworkError(TradingBotError):
    pass

class ConfigurationError(TradingBotError):
    pass