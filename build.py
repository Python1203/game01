import os
from jinja2 import Template

# 假设这是从 API 拿到的热门数据
hot_topics = [
    {"name": "Bitcoin", "trend": "Bullish", "link": "你的币安返佣链接"},
    {"name": "Nvidia", "trend": "Strong Buy", "link": "你的券商链接"}
]

# SEO 网页模板
html_tpl = """
<html>
<head><title>{{ name }} Price Prediction 2026</title></head>
<body>
    <h1>Latest Analysis for {{ name }}</h1>
    <p>Market Sentiment: {{ trend }}</p>
    <a href="{{ link }}">Register & Get Bonus</a>
</body>
</html>
"""

def generate():
    os.makedirs('public', exist_ok=True)  # Vercel 默认发布 public 文件夹
    template = Template(html_tpl)
    for item in hot_topics:
        content = template.render(item)
        with open(f"public/{item['name'].lower()}.html", "w") as f:
            f.write(content)

if __name__ == "__main__":
    generate()
