"""淘宝标题生成提示实现。"""

from mcp.server.types import Message, TextContent, EmbeddedResource
from ..server import mcp

@mcp.prompt("generate_title_from_images")
def title_generation_prompt(image_urls: list[str]) -> list[Message]:
    """创建一个淘宝标题生成提示，包含示例图片URL。
    
    Args:
        image_urls: 示例商品图片URL列表
    
    Returns:
        包含提示消息的列表
    """
    messages = [
        Message(
            role="user",
            content=TextContent(
                type="text",
                text="我需要为淘宝商品生成一个优化的标题。请使用淘宝标题生成工具帮我完成。"
            )
        ),
        Message(
            role="user",
            content=TextContent(
                type="text",
                text="以下是我的商品图片链接，请根据这些图片生成一个吸引人的淘宝标题："
            )
        )
    ]
    
    # 添加图片URL
    for url in image_urls:
        messages.append(
            Message(
                role="user",
                content=TextContent(
                    type="text",
                    text=url
                )
            )
        )
    
    # 添加使用指南
    messages.append(
        Message(
            role="user",
            content=EmbeddedResource(
                type="resource",
                resource={
                    "uri": "info://usage_guidelines",
                    "text": "请参考这些最佳实践来生成标题。"
                }
            )
        )
    )
    
    return messages

@mcp.prompt("analyze_title_quality")
def title_analysis_prompt(title: str) -> list[Message]:
    """创建一个分析淘宝标题质量的提示。
    
    Args:
        title: 要分析的淘宝商品标题
    
    Returns:
        包含提示消息的列表
    """
    return [
        Message(
            role="user",
            content=TextContent(
                type="text",
                text="请分析以下淘宝商品标题的质量，并给出改进建议："
            )
        ),
        Message(
            role="user",
            content=TextContent(
                type="text",
                text=title
            )
        ),
        Message(
            role="user",
            content=TextContent(
                type="text",
                text="""
请从以下几个方面进行分析：
1. 标题长度是否合适（建议30个汉字以内）
2. 是否包含关键的商品信息（类别、材质、功能、款式等）
3. 关键词排序是否合理（重要关键词是否靠前）
4. 是否有违规词或极限词
5. 可读性如何
6. SEO友好度如何

请给出具体的改进建议。
"""
            )
        )
    ] 