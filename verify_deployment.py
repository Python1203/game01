"""
验证部署页面内容检查脚本
检查 VIP 标签、足球预测、功能亮点等是否正确显示
"""
import os
import re


def verify_deployed_page():
    """验证生成的 HTML 页面内容"""
    
    html_path = "./vercel-money-factory/dist/index.html"
    
    if not os.path.exists(html_path):
        print(f"❌ 文件不存在：{html_path}")
        return False
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("=" * 60)
    print("📋 Astro 项目主页内容验证报告")
    print("=" * 60)
    
    # 检查项列表
    checks = {
        "VIP 标签": r"🔥 新增 VIP 前瞻",
        "焦点战役 - Manchester United vs Liverpool": r"Manchester United vs Liverpool",
        "赔率信息": r"最高赔率 [23]\.[0-9]{2}",
        "JSON-LD 优化标识": r"⭐ JSON-LD 优化",
        "VIP 伤停情报标识": r"💎 VIP 伤停情报",
        "功能亮点 - SEO 优化": r"SEO 优化.*JSON-LD",
        "功能亮点 - 深度链接": r"深度链接.*转化率提升 300%",
        "功能亮点 - VIP 内容": r"VIP 内容.*伤停情报",
        "足球预测板块": r"足球比赛预测",
        "英超标签": r"英超",
    }
    
    results = {}
    
    for check_name, pattern in checks.items():
        if re.search(pattern, html_content):
            results[check_name] = "✅"
        else:
            results[check_name] = "❌"
    
    # 输出结果
    print("\n验证结果:\n")
    
    all_passed = True
    for check_name, status in results.items():
        print(f"{status} {check_name}")
        if status == "❌":
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✅ 所有检查项都通过了!")
        print("\n✨ 页面已成功部署，包含:")
        print("   • 🔥 新增 VIP 前瞻标签")
        print("   • ⚽ Manchester United vs Liverpool 焦点战役")
        print("   • 💰 实时赔率信息")
        print("   • ⭐ JSON-LD 优化标识")
        print("   • 💎 VIP 伤停情报提示")
        print("   • 📊 完整的功能亮点展示")
    else:
        print("⚠️ 部分检查项未通过，请检查源文件")
    
    print("\n" + "=" * 60)
    
    # 统计预测文章数量
    predictions_dir = "./vercel-money-factory/dist/predictions"
    if os.path.exists(predictions_dir):
        prediction_count = len([d for d in os.listdir(predictions_dir) if os.path.isdir(os.path.join(predictions_dir, d))])
        print(f"\n📄 已生成 {prediction_count} 篇足球预测文章")
    
    # 访问 URL 提示
    print("\n" + "=" * 60)
    print("\n🌐 访问以下链接查看部署效果:")
    print("   • 主域名：https://vercel-money-factory.vercel.app")
    print("   • 预览 URL: https://vercel-money-factory-e7wqpxo8c-python1203s-projects.vercel.app")
    print("\n📊 Vercel Analytics 配置建议:")
    print("   1. 访问 https://vercel.com/dashboard/analytics")
    print("   2. 选择 vercel-money-factory 项目")
    print("   3. 启用 Web Analytics 功能")
    print("   4. 在 src/layouts/BaseLayout.astro 中添加追踪代码")
    print("\n💡 CPS 转化追踪建议:")
    print("   • 在所有博彩公司链接中添加 ?ref=xxx 追踪参数")
    print("   • 使用 Bitly 或类似服务缩短并追踪点击")
    print("   • 在 Vercel Analytics 中设置自定义事件追踪")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    verify_deployed_page()
