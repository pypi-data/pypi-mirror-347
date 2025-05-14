"""
uv run test.py
_ENV_BASE=devcn uv run test.py
"""

import logging
from typing import Union
from src.mcp_server_foxit_cloudapi.action.create_pdf import create_pdf
import asyncio

logging.basicConfig(
    filename="./temp/debug.log",
    level=logging.INFO,
)


asyncio.run(
    create_pdf(
        # {"path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/dev.txt", "format": "text"},
        {"path": "https://gitee.com/wtw/dev-file/raw/master/dev.docx", "format": "word"},
        {"clientId": "0b0a248c2c877cd3797d1180cfa69206", "mode": "CLOUD"},
    )
)