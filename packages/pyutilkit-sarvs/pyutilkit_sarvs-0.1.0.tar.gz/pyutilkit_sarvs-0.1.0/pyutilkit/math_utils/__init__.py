"""
Math utility functions for common mathematical operations.

This module provides utility functions for mathematical operations,
including safe arithmetic, statistics, and number theory.
"""

from .arithmetic import (
    safe_divide,
    percent_change,
    normalize,
    z_score
)

from .statistics import (
    mean,
    median,
    mode,
    standard_deviation
)

from .number_theory import (
    is_prime,
    factorial,
    gcd,
    lcm
)

__all__ = [
    'safe_divide',
    'percent_change',
    'normalize',
    'z_score',
    'mean',
    'median',
    'mode',
    'standard_deviation',
    'is_prime',
    'factorial',
    'gcd',
    'lcm'
] 