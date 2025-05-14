from typing import Callable, Dict, Any
class ToolBase:
    def __init__(self, name: str, description: str, parameters: Any, execute: Callable[[Any], Any]):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.execute = execute
