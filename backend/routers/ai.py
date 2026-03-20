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
                    "content": "你是一个中国古代建筑专家，请简洁准确地回答用户关于中国古代建筑的问题。"
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
