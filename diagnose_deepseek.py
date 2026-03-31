"""
诊断 DeepSeek API 连接问题
"""
import requests

api_key = "sk-ekXi4cdzr5m0U5bm1a315a21EdDb42Ec863c0b37C092081e"
base = "https://xh.v1api.cc"

print("🔍 诊断 DeepSeek API 连接\n")
print(f"API Key: {api_key[:20]}...")
print(f"Base URL: {base}\n")

# 测试不同的端点
endpoints = [
    "/v1/chat/completions",
    "/v1/models",
]

for endpoint in endpoints:
    try:
        url = f"{base}{endpoint}"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        if endpoint == "/v1/chat/completions":
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            r = requests.post(url, json=payload, headers=headers, timeout=10)
        else:
            r = requests.get(url, headers=headers, timeout=10)
        
        print(f"\n{endpoint}:")
        print(f"  Status: {r.status_code}")
        if r.status_code != 200:
            try:
                error_data = r.json()
                print(f"  Error: {error_data}")
            except:
                print(f"  Raw: {r.text[:200]}")
        else:
            print(f"  ✓ Success!")
            
    except Exception as e:
        print(f"\n{endpoint}: ERROR - {e}")

print("\n💡 建议:")
print("1. 检查 API Key 是否正确（可能已失效）")
print("2. 确认 Base URL 是否可访问")
print("3. 联系 API 提供商获取新的凭证")
