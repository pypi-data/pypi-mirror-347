"""淘宝标题生成工具实现。"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image
import time
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from mcp.server.fastmcp import Context

from ..server import mcp

class TitleRequest(BaseModel):
    """淘宝标题生成请求模型。"""
    image_urls: List[str] = Field(..., description="商品图片URL列表，至少提供一张图片")
    temperature: float = Field(0.7, description="控制生成结果的随机性（0.0-1.0）")

class TitleResponse(BaseModel):
    """淘宝标题生成响应模型。"""
    title: str = Field(..., description="生成的淘宝商品标题")
    processing_time: float = Field(..., description="处理时间（秒）")

def download_image_to_base64(image_url: str) -> str | None:
    """下载图片并转换为base64编码。
    
    Args:
        image_url: 图片的URL地址
        
    Returns:
        base64编码的图片字符串，如果下载失败则返回None
    """
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            # 获取图片内容
            image_content = response.content
            
            # 使用PIL库打开图片并调整大小（如果需要）
            image = Image.open(BytesIO(image_content))
            
            # 将图片转换为base64编码
            buffered = BytesIO()
            image.save(buffered, format=image.format)
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # 返回base64编码的字符串
            return f"data:image/{image.format.lower()};base64,{img_str}"
        else:
            return None
    except Exception:
        return None

@mcp.tool()
async def generate_taobao_title(request: TitleRequest, ctx: Context) -> TitleResponse:
    """根据商品图片生成优化的淘宝商品标题。
    
    此工具接收商品图片URL列表，将图片转换为base64编码后调用API生成标题。
    生成的标题会遵循淘宝平台规范，突出商品核心卖点和关键词。
    
    Args:
        request: 包含图片URL列表和可选参数的请求对象
        ctx: MCP上下文对象，用于记录日志和报告进度
    
    Returns:
        包含生成的标题和处理时间的响应对象
    """
    await ctx.info(f"开始处理淘宝标题生成请求，共 {len(request.image_urls)} 张图片")
    
    # 将图片URL转换为base64编码
    base64_images = []
    for i, url in enumerate(request.image_urls):
        await ctx.report_progress(i, len(request.image_urls), f"正在处理图片 {i+1}/{len(request.image_urls)}")
        await ctx.debug(f"正在处理图片: {url}")
        base64_img = download_image_to_base64(url)
        if base64_img:
            base64_images.append(base64_img)
    
    if not base64_images:
        await ctx.error("没有成功转换任何图片")
        raise ValueError("无法处理提供的图片URL，请检查URL是否有效")
    
    await ctx.report_progress(len(request.image_urls), len(request.image_urls), "图片处理完成，正在生成标题")
    
    # API请求参数
    api_url = 'http://api2.sanshaokeji.top/taobao_title_generator.php'
    data = {
        'api_key': 'sk-T3APBxMht7BbKMGUiauSeRwEWBbno8dVH5qclHsBaUlItdtH',
        'model': 'o4-mini',
        'images': base64_images,
        'api_endpoint_url': 'https://api.ssopen.top/v1/chat/completions',
        'temperature': request.temperature,
        'max_tokens': 15500
    }
    
    # 发送请求
    await ctx.info("正在发送API请求...")
    start_time = time.time()
    try:
        response = requests.post(api_url, json=data)
        end_time = time.time()
        processing_time = end_time - start_time
        await ctx.info(f"请求耗时: {processing_time:.2f}秒")
        
        if response.status_code == 200:
            result = response.json()
            title = result.get('title', '')
            await ctx.info(f"成功生成标题: {title}")
            return TitleResponse(title=title, processing_time=processing_time)
        else:
            error_msg = f"API请求失败，状态码: {response.status_code}"
            await ctx.error(error_msg)
            raise RuntimeError(error_msg)
    except Exception as e:
        await ctx.error(f"请求出错: {str(e)}")
        raise 