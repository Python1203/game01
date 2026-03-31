# DeepSeek API 集成指南

## ⚠️ 重要提示

**当前提供的 DeepSeek API Key 已失效**，显示"无效的令牌"错误。

### 问题诊断

```bash
python3 diagnose_deepseek.py
```

**测试结果**:
- Status: 401 Unauthorized
- Error: 无效的令牌 (request id: 20260331101320535541880erKoD8TP)

---

## ✅ 已完成的工作

### 1. **代码集成完成**
- ✓ [ai_content_generator.py](file:///Users/zzw868/PycharmProjects/PythonProject/src/ai_content_generator.py) 已支持 DeepSeek
- ✓ 自动故障转移机制
- ✓ 完善的错误处理
- ✓ 支持 OpenAI 和 DeepSeek 双模型

### 2. **配置文件更新**
- ✓ `.env.example` 已添加 DeepSeek 配置项
- ✓ `main.py` 支持自动检测 AI 模型

### 3. **测试脚本**
- ✓ `test_deepseek.py` - DeepSeek 专用测试
- ✓ `diagnose_deepseek.py` - API 连接诊断

---

## 🔧 解决方案

### 方案 1: 使用 OpenAI（推荐）

1. 获取 OpenAI API Key: https://platform.openai.com/api-keys
2. 创建 `.env` 文件：
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```
3. 运行主程序：
```bash
python3 main.py
```

### 方案 2: 使用有效的 DeepSeek API Key

1. **获取新的 DeepSeek API Key**:
   - 访问 DeepSeek 官网：https://www.deepseek.com/
   - 或联系 API 提供商获取有效凭证

2. **配置环境变量**:
```bash
# 创建 .env 文件
cat > .env << EOF
DEEPSEEK_API_KEY=your-new-valid-api-key-here
DEEPSEEK_BASE_URL=https://xh.v1api.cc
EOF
```

3. **测试连接**:
```bash
python3 test_deepseek.py
```

4. **运行主程序**:
```bash
python3 main.py
```

---

## 📊 当前状态

| 组件 | 状态 | 说明 |
|------|------|------|
| **代码集成** | ✅ 完成 | DeepSeek 已完全集成到项目中 |
| **API Key** | ❌ 失效 | 提供的 Key 显示"无效的令牌" |
| **Base URL** | ⚠️ 待确认 | https://xh.v1api.cc 可访问但需要有效凭证 |
| **OpenAI 兼容** | ✅ 可用 | 可随时切换到 OpenAI |

---

## 💡 建议

### 立即可用
- 使用 OpenAI API（更稳定，文档完善）
- 或使用模板文章（当 AI 调用失败时自动生成）

### 长期使用
- 申请自己的 DeepSeek API Key
- 考虑多个 AI 服务商备份（OpenAI + DeepSeek + Claude）

---

## 🔗 参考资料

- [DeepSeek 官方文档](https://platform.deepseek.com/)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [项目集成代码](file:///Users/zzw868/PycharmProjects/PythonProject/src/ai_content_generator.py)

---

## 🧪 测试命令

```bash
# 诊断 API 连接
python3 diagnose_deepseek.py

# 测试 DeepSeek（需要有效 Key）
python3 test_deepseek.py

# 运行完整流程
python3 main.py
```

---

**认证完成通知**: 
- ✅ DeepSeek API 代码集成已完成并通过编译测试
- ⚠️ 提供的 API Key 已失效，需要获取新的有效凭证
- 💡 建议暂时使用 OpenAI 或等待获取新的 DeepSeek API Key

**下一步操作**:
1. 如果有有效的 DeepSeek API Key，更新 `.env` 文件后运行 `python3 test_deepseek.py`
2. 如果没有，建议使用 OpenAI 或直接运行（会使用模板文章）
3. 查看 [QUICK_REFERENCE.md](file:///Users/zzw868/PycharmProjects/PythonProject/QUICK_REFERENCE.md) 获取更多帮助

---

**更新时间**: 2026-03-31  
**状态**: ⚠️ 代码就绪，等待有效 API Key
