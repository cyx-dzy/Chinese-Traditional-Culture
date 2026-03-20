from fastapi import APIRouter, HTTPException
import requests
from pydantic import BaseModel
from config import settings


router = APIRouter(prefix="/ai", tags=["ai"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
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
        
        response = requests.post(
            f"{settings.modelscope_base_url}chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0].get('message', {}).get('content', '')
                return ChatResponse(response=content)
        
        raise HTTPException(status_code=500, detail="AI服务暂时不可用")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务错误: {str(e)}")
