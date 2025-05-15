import logging
import colorlog
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a color formatter with function name and line number
color_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(funcName)s - line %(lineno)d - %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# Create a stream handler with the color formatter
handler = logging.StreamHandler()
handler.setFormatter(color_formatter)
logger.addHandler(handler)



def elapsed_time_logger(func):
    """Decorator to log the elapsed time of a function."""
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.debug(f"Starting execution of {func.__name__}")
        
        # Execute the wrapped function
        result = func(*args, **kwargs)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.debug(f"Finished execution of {func.__name__}")
        logger.info(f"Elapsed time for {func.__name__}: {elapsed_time:.10f}s")
        print(f"Elapsed time for {func.__name__}: {elapsed_time:.10f}s")
        
        return result
    
    return wrapper

__all__ = ["logger", "elapsed_time_logger"]