from fastapi import APIRouter, HTTPException
import requests
from pydantic import BaseModel
from config import settings
import logging
import time

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    start_time = time.time()
    logger.info(f"收到AI聊天请求: {request.message[:50]}...")
    
    try:
        headers = {
            "Authorization": f"Bearer {settings.modelscope_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": settings.modelscope_model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是'溯光而行'中国古代建筑成就数字展的智能助手。当用户打招呼或问候时，请热情地介绍这个项目：'溯光而行'是一个展示中国古代建筑辉煌成就的数字展览平台，通过现代数字技术让用户领略中国古代建筑的魅力。对于用户关于中国古代建筑的问题，请简洁准确地回答，涵盖建筑风格、结构特点、历史背景、文化内涵等方面。"
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        logger.info(f"发送请求到ModelScope API...")
        response = requests.post(
            f"{settings.modelscope_base_url}chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        elapsed_time = time.time() - start_time
        logger.info(f"API响应时间: {elapsed_time:.2f}秒, 状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logger.debug(f"API响应数据: {data}")
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0].get('message', {}).get('content', '')
                logger.info(f"成功获取AI回复，长度: {len(content)}字符")
                return ChatResponse(response=content)
            else:
                logger.error(f"API响应格式异常: {data}")
                raise HTTPException(status_code=500, detail="AI服务响应格式异常")
        else:
            logger.error(f"API返回错误状态码: {response.status_code}, 响应内容: {response.text[:200]}")
            raise HTTPException(status_code=500, detail=f"AI服务暂时不可用 (状态码: {response.status_code})")
        
    except requests.exceptions.Timeout as e:
        elapsed_time = time.time() - start_time
        logger.error(f"API请求超时: {str(e)}, 耗时: {elapsed_time:.2f}秒")
        raise HTTPException(status_code=504, detail="AI服务响应超时，请稍后再试")
    except requests.exceptions.ConnectionError as e:
        elapsed_time = time.time() - start_time
        logger.error(f"API连接错误: {str(e)}, 耗时: {elapsed_time:.2f}秒")
        raise HTTPException(status_code=503, detail="AI服务连接失败，请检查网络")
    except requests.exceptions.RequestException as e:
        elapsed_time = time.time() - start_time
        logger.error(f"API请求异常: {str(e)}, 耗时: {elapsed_time:.2f}秒")
        raise HTTPException(status_code=500, detail="AI服务暂时不可用，请稍后再试")
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.error(f"未知错误: {str(e)}, 耗时: {elapsed_time:.2f}秒", exc_info=True)
        raise HTTPException(status_code=500, detail="AI服务暂时不可用，请稍后再试")
