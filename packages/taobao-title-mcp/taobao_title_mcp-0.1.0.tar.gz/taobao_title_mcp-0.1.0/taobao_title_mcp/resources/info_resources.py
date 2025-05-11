"""淘宝标题生成服务器信息资源。"""

from ..server import mcp

@mcp.resource("info://api_description")
def get_api_description() -> dict:
    """获取API的描述信息。"""
    return {
        "name": "淘宝商品标题生成API",
        "description": "根据商品图片自动生成优化的淘宝商品标题，利用AI图像识别和自然语言处理能力分析商品特点。",
        "version": "0.1.0",
        "provider": "三少科技",
        "endpoint": "http://api2.sanshaokeji.top/taobao_title_generator.php"
    }

@mcp.resource("info://usage_guidelines")
def get_usage_guidelines() -> dict:
    """获取API使用指南。"""
    return {
        "best_practices": [
            "提供多角度的商品图片以获得更全面的商品描述",
            "调整temperature参数可控制标题的创意程度",
            "图片URL必须可公开访问",
            "单次请求最多处理10张图片",
            "图片大小不应超过4MB"
        ],
        "limitations": [
            "请求频率限制为每分钟10次",
            "API请求可能需要较长时间（最多60秒超时）",
            "生成的标题会自动避免淘宝违规词和极限词"
        ],
        "example_urls": [
            "https://gw.alicdn.com/imgextra/i4/215590895/O1CN01wcB8AU1ITxVvVRZyZ_!!215590895.jpg",
            "https://img.alicdn.com/imgextra/i3/215590895/O1CN01aKTYIT1ITxVvnKJVM_!!215590895.jpg",
            "https://img.alicdn.com/bao/uploaded/i2/2211615841274/O1CN018znKRb1LHXXxtbI9I_!!2211615841274.jpg"
        ]
    }

@mcp.resource("examples://{example_id}")
def get_example(example_id: str) -> dict | None:
    """获取示例数据。
    
    Args:
        example_id: 示例ID，可选值为"shoes"、"clothes"或"electronics"
    
    Returns:
        示例数据，如果ID无效则返回None
    """
    examples = {
        "shoes": {
            "image_urls": [
                "https://gw.alicdn.com/imgextra/i4/215590895/O1CN01wcB8AU1ITxVvVRZyZ_!!215590895.jpg",
                "https://img.alicdn.com/imgextra/i3/215590895/O1CN01aKTYIT1ITxVvnKJVM_!!215590895.jpg"
            ],
            "generated_title": "复古玛丽珍厚底松糕防滑平底单鞋女2025春夏气质百搭"
        },
        "clothes": {
            "image_urls": [
                "https://img.alicdn.com/bao/uploaded/i1/2201504856387/O1CN01S7Kx8U1x3IEtfPnUv_!!2201504856387.jpg"
            ],
            "generated_title": "2023夏季新款宽松显瘦印花短袖T恤女韩版百搭休闲上衣"
        },
        "electronics": {
            "image_urls": [
                "https://img.alicdn.com/bao/uploaded/i1/2616970884/O1CN01IOg95v1IOueSRn1Oj_!!2616970884.jpg"
            ],
            "generated_title": "新款无线蓝牙耳机双耳降噪高音质长续航适用苹果华为小米"
        }
    }
    return examples.get(example_id) 