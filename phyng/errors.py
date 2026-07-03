"""
Custom exceptions for Phyng.

Clear, specific errors — no silent failures, no generic messages.
"""


class PhyngError(Exception):
    """Base exception for all Phyng errors."""


class InvalidMassError(PhyngError):
    """Raised when a mass value is non-positive or physically invalid."""


class InvalidProbabilityError(PhyngError):
    """Raised when a probability value is outside [0, 1]."""


class InvalidScaleError(PhyngError):
    """Raised when an operational scale is invalid or unjustified."""


class InvalidDistributionError(PhyngError):
    """Raised when a probability distribution is invalid (negative, zero-sum, etc.)."""


class InvalidClaimError(PhyngError):
    """Raised when a claim is structurally invalid for evaluation."""
