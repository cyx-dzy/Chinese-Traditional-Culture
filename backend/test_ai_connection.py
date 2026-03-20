import requests
from config import settings

def test_ai_api():
    print("测试AI API连接...")
    print(f"API Key: {settings.modelscope_api_key[:20]}...")
    print(f"Model: {settings.modelscope_model}")
    print(f"Base URL: {settings.modelscope_base_url}")
    
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
                "content": "你好"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        print("\n发送请求到AI API...")
        response = requests.post(
            f"{settings.modelscope_base_url}chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应数据: {data}")
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0].get('message', {}).get('content', '')
                print(f"\nAI回复: {content}")
                return True
            else:
                print("响应中没有choices字段")
                return False
        else:
            print(f"API返回错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"发生异常: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_ai_api()
    if success:
        print("\n✅ AI API测试成功")
    else:
        print("\n❌ AI API测试失败")