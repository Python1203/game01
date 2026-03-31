# DeepSeek API 超时问题解决方案

## 🔍 问题诊断

**错误信息：**
```
AI 生成失败：DeepSeek API 网络错误：HTTPSConnectionPool(host='xh.v1api.cc', port=443): Read timed out. (read timeout=30)
```

**根本原因：**
1. ❌ **第三方代理不稳定** - `xh.v1api.cc` 是非官方代理服务器，可能已失效或响应慢
2. ❌ **网络连接问题** - 服务器可能在海外，连接超时
3. ❌ **API Key 可能失效** - 凭证过期或被限制

---

## ✅ 解决方案（按推荐顺序）

### 方案 1：切换到 OpenAI（⭐⭐⭐⭐⭐ 最稳定）

如果你有 OpenAI API Key，这是最佳选择：

**步骤：**
1. 编辑 `.env` 文件：
```bash
# AI 配置（使用 OpenAI - 更稳定）
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1

# DeepSeek 配置（备用）
# DEEPSEEK_API_KEY=sk-xxx
# DEEPSEEK_BASE_URL=https://api.deepseek.com
```

2. 测试配置：
```bash
python test_ai_config.py
```

---

### 方案 2：使用 DeepSeek 官方 API（⭐⭐⭐⭐ 性价比高）

DeepSeek 官方 API 价格低廉且性能优秀：

**步骤：**

1. **获取官方 API Key**
   - 访问：https://platform.deepseek.com/
   - 注册登录 → 个人中心 → API Keys
   - 创建新 Key 并复制保存

2. **更新 .env 配置**
```bash
# 使用 DeepSeek 官方 API
DEEPSEEK_API_KEY=你的 sk-xxxxx  # 从官网获取
DEEPSEEK_BASE_URL=https://api.deepseek.com

# 注释掉旧的第三方代理配置
# DEEPSEEK_BASE_URL=https://xh.v1api.cc
```

3. **验证配置**
```bash
python test_ai_config.py
```

**优势：**
- ✅ 官方服务，稳定性高
- ✅ 价格极低（比 GPT-4 便宜 90%+）
- ✅ 完全兼容 OpenAI SDK
- ✅ 中文优化，性能优秀

---

### 方案 3：增加超时时间（临时方案）

如果必须使用当前配置，可以尝试增加超时时间：

**已在代码中优化：**
- ✅ 超时从 30 秒增加到 60 秒
- ✅ 添加更详细的错误提示
- ✅ 提供故障排除建议

**修改位置：** `src/ai_content_generator.py` 第 127 行

---

## 🛠️ 故障排查工具

### 1. 快速测试脚本
```bash
python test_ai_config.py
```

### 2. 手动测试 API 连接
```bash
python diagnose_deepseek.py
```

### 3. 检查当前配置
```bash
cat .env
```

---

## 📊 各方案对比

| 方案 | 稳定性 | 成本 | 速度 | 推荐度 |
|------|--------|------|------|--------|
| OpenAI | ⭐⭐⭐⭐⭐ | 高 | 快 | ⭐⭐⭐⭐⭐ |
| DeepSeek 官方 | ⭐⭐⭐⭐ | 极低 | 快 | ⭐⭐⭐⭐ |
| 第三方代理 | ⭐⭐ | 免费/低 | 慢 | ⭐⭐ |

---

## 💡 最佳实践建议

1. **生产环境**：使用 OpenAI 或 DeepSeek 官方 API
2. **开发测试**：可以使用 DeepSeek（成本低）
3. **避免使用**：来路不明的第三方代理服务

---

## 🔗 参考资料

- **DeepSeek 官方文档**：https://platform.deepseek.com/
- **OpenAI API 文档**：https://platform.openai.com/docs
- **模型配置示例**：`.env.example`

---

## 🚀 下一步行动

**立即执行：**
```bash
# 1. 查看当前配置
cat .env

# 2. 根据上述方案选择合适的配置并编辑 .env

# 3. 测试配置
python test_ai_config.py

# 4. 运行主程序
python main.py
```

**认证完成通知**：配置修改完成后，系统会自动检测并使用正确的 AI 模型。请运行测试脚本确认配置有效后，再继续执行后续部署命令。
