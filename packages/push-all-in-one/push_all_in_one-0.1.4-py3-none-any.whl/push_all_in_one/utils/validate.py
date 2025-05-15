from typing import Any, Dict
from ..interfaces.schema import ConfigSchema

def validate(config: Dict[str, Any], schema: ConfigSchema) -> bool:
    """
    验证配置是否符合模式定义
    
    Args:
        config: 配置
        schema: 模式定义
        
    Returns:
        bool: 是否通过验证
        
    Raises:
        ValueError: 验证失败
    """
    for key, field in schema.items():
        if field.required and (key not in config or config[key] is None):
            raise ValueError(f"缺少必要参数: {key}")
    
    return True 