import warnings

warnings.warn(
    "The 'dhenara' package is renamed to `dhenara-ai`. Please use 'dhenara-ai' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Import everything from dhenara-ai
try:
    from dhenara.ai import *
except ImportError:
    warnings.warn(
        "Could not import dhenara-ai. Please install it with: pip install dhenara-ai",
        ImportWarning,
        stacklevel=2,
    )
