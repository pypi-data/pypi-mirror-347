# MCard package initialization
import os
from .config.logging_config import setup_logging, get_logger
from .model.card import MCard
from .model.card_collection import CardCollection
from .engine.sqlite_engine import SQLiteConnection, SQLiteEngine
from .config.env_parameters import EnvParameters
from .mcard_utility import MCardUtility

# Try to import optional engines

try:
    from .engine.duckdb_engine import DuckDBConnection, DuckDBEngine
    DUCKDB_AVAILABLE = True
except ImportError:
    DUCKDB_AVAILABLE = False
    DuckDBConnection = None
    DuckDBEngine = None

# Initialize logging
setup_logging()
logger = get_logger('init')
logger.debug('Logging initialized in __init__.py')

# Define the most commonly used classes in __all__
__all__ = [
    'MCard',
    'CardCollection',
    'SQLiteConnection',
    'SQLiteEngine',
    'EnvParameters',
    'MCardUtility',
    'setup_logging',
    'get_logger'
]

# Add optional engines to __all__ if available

if DUCKDB_AVAILABLE:
    __all__.extend(['DuckDBConnection', 'DuckDBEngine'])
    logger.debug('DuckDB engine is available')
else:
    logger.debug('DuckDB engine is not available')

# Get engine type from environment variable or use 'sqlite' as default
engine_type = os.environ.get('MCARD_ENGINE_TYPE', 'sqlite')
logger.info(f"Using {engine_type} as the default engine type")


# Create a default utility instance for quick access
default_utility = MCardUtility(engine_type=engine_type)

# Log creation
logger.debug(f"Created default utility with engine type: {engine_type}")
