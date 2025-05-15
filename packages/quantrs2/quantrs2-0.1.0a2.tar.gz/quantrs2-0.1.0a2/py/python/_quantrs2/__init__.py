"""
Internal module for QuantRS2 native bindings.

This module is not meant to be imported directly.
Please use the 'quantrs2' package instead.
"""

# Re-export all symbols from the native module
from ._quantrs2 import *

# List of public symbols (used by Python's dir() function)
__all__ = ['PyCircuit', 'PySimulationResult']