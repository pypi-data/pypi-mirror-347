from typing import Dict, Any, TypeVar, Generic, List, Union, Optional

T = TypeVar('T')

class SchemaField:
    """配置字段定义"""
    
    def __init__(
        self, 
        field_type: str, 
        title: str, 
        description: str = "", 
        required: bool = False, 
        default: Any = None,
        options: Optional[List[Dict[str, str]]] = None
    ):
        self.type = field_type
        self.title = title
        self.description = description
        self.required = required
        self.default = default
        self.options = options


class ConfigSchema(Generic[T]):
    """配置模式定义"""
    pass


class OptionSchema(Generic[T]):
    """选项模式定义"""
    pass 