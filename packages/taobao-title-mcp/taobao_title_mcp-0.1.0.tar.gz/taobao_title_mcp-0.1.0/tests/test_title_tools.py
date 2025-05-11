"""淘宝标题生成工具测试。"""

import pytest
from unittest.mock import patch, MagicMock
from taobao_title_mcp.tools.title_tools import download_image_to_base64, generate_taobao_title
from taobao_title_mcp.tools.title_tools import TitleRequest, TitleResponse

# 测试下载图片并转换为base64
@patch('taobao_title_mcp.tools.title_tools.requests.get')
def test_download_image_to_base64_success(mock_get):
    # 模拟成功的请求
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'fake_image_content'
    mock_get.return_value = mock_response
    
    # 模拟PIL.Image
    with patch('taobao_title_mcp.tools.title_tools.Image') as mock_image:
        mock_img = MagicMock()
        mock_img.format = 'JPEG'
        mock_image.open.return_value = mock_img
        
        # 模拟BytesIO
        with patch('taobao_title_mcp.tools.title_tools.BytesIO') as mock_bytesio:
            mock_buffer = MagicMock()
            mock_bytesio.return_value = mock_buffer
            
            # 模拟base64编码
            with patch('taobao_title_mcp.tools.title_tools.base64.b64encode') as mock_b64encode:
                mock_b64encode.return_value = b'fake_base64_content'
                
                result = download_image_to_base64('http://example.com/image.jpg')
                
                # 验证结果
                assert result == 'data:image/jpeg;base64,fake_base64_content'
                mock_get.assert_called_once_with('http://example.com/image.jpg')

# 测试下载图片失败
@patch('taobao_title_mcp.tools.title_tools.requests.get')
def test_download_image_to_base64_failure(mock_get):
    # 模拟失败的请求
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    result = download_image_to_base64('http://example.com/nonexistent.jpg')
    
    # 验证结果
    assert result is None
    mock_get.assert_called_once_with('http://example.com/nonexistent.jpg')

# 测试生成标题工具
@patch('taobao_title_mcp.tools.title_tools.download_image_to_base64')
@patch('taobao_title_mcp.tools.title_tools.requests.post')
@pytest.mark.asyncio
async def test_generate_taobao_title(mock_post, mock_download):
    # 模拟下载图片成功
    mock_download.return_value = 'data:image/jpeg;base64,fake_base64_content'
    
    # 模拟API请求成功
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'title': '测试商品标题'}
    mock_post.return_value = mock_response
    
    # 创建请求对象
    request = TitleRequest(
        image_urls=['http://example.com/image1.jpg', 'http://example.com/image2.jpg'],
        temperature=0.5
    )
    
    # 创建模拟上下文
    mock_ctx = MagicMock()
    mock_ctx.info = MagicMock()
    mock_ctx.debug = MagicMock()
    mock_ctx.error = MagicMock()
    mock_ctx.report_progress = MagicMock()
    
    # 调用工具函数
    result = await generate_taobao_title(request, mock_ctx)
    
    # 验证结果
    assert isinstance(result, TitleResponse)
    assert result.title == '测试商品标题'
    assert result.processing_time > 0
    
    # 验证函数调用
    assert mock_download.call_count == 2
    mock_post.assert_called_once()
    assert mock_ctx.info.call_count >= 2
    assert mock_ctx.report_progress.call_count >= 2 