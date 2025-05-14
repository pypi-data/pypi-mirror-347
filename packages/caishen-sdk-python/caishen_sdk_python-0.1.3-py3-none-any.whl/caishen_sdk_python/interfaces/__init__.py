from typing import Dict
from typing import Callable, Awaitable, Any

ToolType = Callable[[Any], Awaitable[Any]]
Tools = Dict[str, ToolType]

__all__ = ["Tools"]
