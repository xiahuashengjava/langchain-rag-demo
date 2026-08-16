import requests
from bs4 import BeautifulSoup

# 维基百科中文：黑洞词条（科普类，内容约5000字以上）
url = "https://zh.wikipedia.org/zh-cn/%E9%BB%91%E6%B4%9E"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers, timeout=15)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

extracted_content = []

# 提取主标题
title = soup.find("h1", id="firstHeading")
if title:
    extracted_content.append(f"========== {title.get_text(strip=True)} ==========\n")

# 维基百科正文容器 id="mw-content-text"
main_body = soup.find("div", id="mw-content-text")

if main_body:
    # 遍历所有标题和段落，按层级输出
    for tag in main_body.find_all(["h2", "h3", "h4", "p"]):
        text = tag.get_text(strip=True)
        if not text:
            continue
        
        if tag.name == "h2":
            extracted_content.append(f"\n## {text}")
        elif tag.name == "h3":
            extracted_content.append(f"\n### {text}")
        elif tag.name == "h4":
            extracted_content.append(f"\n#### {text}")
        else:
            # 普通段落
            extracted_content.append(text)
else:
    print("警告：没有找到正文区域")

# 写入文件
with open('./黑洞科普知识库.txt', 'w', encoding='utf-8') as f:
    for item in extracted_content:
        f.write(item + '\n')

# 统计字数
total_chars = sum(len(item) for item in extracted_content)
print("✅内容已成功提取到 黑洞科普知识库.txt 文件")
print(f"✅一共提取到 {len(extracted_content)} 条内容")
print(f"✅总字数约：{total_chars} 字")
