"""
ZeebeeAI Python Client SDK

This package provides a comprehensive client for interacting with the ZeebeeAI Chat Platform.
"""

from .client import ZeebeeClient
from .exceptions import (
    AuthenticationError,
    RateLimitError,
    AgentException,
    PipelineException,
    RoutingException,
)
from .agents import AgentController, AgentTypes
from .pipelines import PipelineController
from .routing import RoutingController, IntentCategory, LayoutType, RoutingPipeline

__version__ = "0.1.3"
__all__ = [
    "ZeebeeClient",
    "AgentController",
    "PipelineController",
    "RoutingController",
    "AuthenticationError",
    "RateLimitError",
    "AgentException",
    "PipelineException",
    "RoutingException",
    "AgentTypes",
    "IntentCategory",
    "LayoutType",
    "RoutingPipeline",
]
