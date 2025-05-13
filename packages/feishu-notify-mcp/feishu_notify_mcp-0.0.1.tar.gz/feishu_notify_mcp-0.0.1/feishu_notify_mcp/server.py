import json  # For formatting ExtractionInfoResponse and TextTranslationResultResponse
import logging
import os
import sys

import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

# Create MCP server
mcp = FastMCP("Lark-Notify-MCP")

# 创建client
# Global variable, will be initialized in the main function
client = None


@mcp.tool(
    name="send_msg",
    description="""发送飞书消息给我"""
)
def send_msg(msg: str) -> TextContent:
    logging.info("Tool called: send_msg")

    user_open_id = os.getenv("USER_OPEN_ID")
    if not user_open_id:
        logging.error("USER_OPEN_ID must be set")
        return TextContent(
            type="text",
            text="环境变量缺少USER_OPEN_ID，请设置后重试"
        )

    content = {
        "text": msg
    }
    # 转成json字符串
    content = json.dumps(content, ensure_ascii=False)

    # 构造请求对象
    request: CreateMessageRequest = CreateMessageRequest.builder() \
        .receive_id_type("open_id") \
        .request_body(CreateMessageRequestBody.builder()
                      .receive_id(user_open_id)
                      .msg_type("text")
                      .content(content)
                      .build()) \
        .build()

    # 发起请求
    response: CreateMessageResponse = client.im.v1.message.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return TextContent(
            type="text",
            text=f"发送失败：{response.msg}"
        )

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    return TextContent(
        type="text",
        text="Done!"
    )


def main():
    # Get environment variables
    app_id = os.getenv("LARK_APP_ID")
    app_secret = os.getenv("LARK_APP_SECRET")

    if not app_id or not app_secret:
        logging.error("LARK_APP_ID and LARK_APP_SECRET must be set")
        sys.exit(1)

    # Initialize global variable
    global client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    logging.info("Starting Lark-Notify-MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
