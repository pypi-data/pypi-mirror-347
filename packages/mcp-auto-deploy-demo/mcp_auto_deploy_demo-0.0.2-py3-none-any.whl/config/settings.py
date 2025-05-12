"""
MCP 服务器配置文件

工具配置说明：
1. enabled: 是否启用该工具
2. module: 工具模块的导入路径
3. class: 工具类名
4. 其他配置项根据工具需求添加

配置示例：
{
    "tool_name": {
        "enabled": True,          # 是否启用
        "module": "tools.xxx.tool", # 模块路径
        "class": "XxxTool",      # 工具类名
        # 其他工具特定的配置项
    }
}
"""
import os
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
       username: str = ""
       password: str = ""
       base_url: str = ""
       login_url: str = ""
       
       class Config:
           env_prefix = "auto_deploy_"
           
settings = Settings()

# 加载环境变量
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    print(f"正在加载环境变量文件: {env_path}")
    load_dotenv(env_path)
else:
    print(f"警告: 环境变量文件不存在: {env_path}")

# 服务器基础配置
SERVER_CONFIG = {
    "name": "Personal MCP Service",
    "host": "0.0.0.0",
    "port": 8001,
    "debug": True,
}

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
}

# 公共配置 - 所有工具都会继承这些配置
COMMON_CONFIG = {
    # 浏览器配置
    "browser_type": "chromium",  # 浏览器类型：chromium, firefox, webkit
    "headless": False,  # 是否在无头模式运行
    # 登录配置
    "username": settings.username if settings.username else os.getenv("API_QUERY_USER", ""),  # 登录用户名
    "password": settings.password if settings.password else os.getenv("API_QUERY_PASSWORD", ""),  # 登录密码
    "login_url": settings.login_url if settings.login_url else os.getenv("LOGIN_URL", ""),  # 登录地址
    "base_url": settings.base_url if settings.base_url else os.getenv("BASE_URL", ""),  # 基础地址
}

'''这里控制哪些工具将会被加载'''
# 工具配置
TOOLS_CONFIG: Dict[str, Dict[str, Any]] = {
    'time': {
        "enabled": True,
        "module": "tools.time.tool",
        "class": "TimeQueryTool",
    },
    # 信息流配置工具
    'flowinfo': {
        "enabled": True,
        "module": "tools.flowInfo.tool",
        "class": "FlowInfoTool",
        # 工具特定配置可以在这里添加，会覆盖公共配置中的同名项
    },
    # 信息流栏目配置工具
    'flowinfocolumn': {
        "enabled": True,
        "module": "tools.flowInfoColumn.tool",
        "class": "FlowInfoColumnTool",
        # 工具特定配置可以在这里添加，会覆盖公共配置中的同名项
    },
    # 专题配置工具
    'topic': {
        "enabled": True,
        "module": "tools.topic.tool",
        "class": "TopicTool",
        # 工具特定配置可以在这里添加，会覆盖公共配置中的同名项
    }
}

# 将公共配置应用到每个工具
for tool_name, tool_config in TOOLS_CONFIG.items():
    # 只对启用的工具应用公共配置
    if tool_config.get("enabled", False):
        # 将公共配置复制到工具配置中，保留工具特定配置的优先级
        for key, value in COMMON_CONFIG.items():
            if key not in tool_config:
                tool_config[key] = value
