import requests

api_key = "sk-ekXi4cdzr5m0U5bm1a315a21EdDb42Ec863c0b37C092081e"
base = "https://xh.v1api.cc"

print("测试 DeepSeek API 连接\n")
print(f"Base URL: {base}")
print(f"API Key: {api_key[:20]}...\n")

# 测试不同的模型名称
models_to_test = [
    "deepseek-chat",
    "deepseek-coder", 
    "DeepSeek-V2",
    "deepseek-v2.5",
]

for model in models_to_test:
    try:
        url = f"{base}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 5
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"✓ 模型 '{model}' 可用！")
            result = response.json()
            print(f"  响应：{result['choices'][0]['message']['content'][:50]}")
            break
        else:
            error_data = response.json()
            print(f"✗ 模型 '{model}': {error_data.get('error', {}).get('message', 'Unknown error')}")
    except Exception as e:
        print(f"✗ 模型 '{model}': 错误 - {e}")

print("\n建议：如果所有模型都返回 401，说明 API Key 已失效")
