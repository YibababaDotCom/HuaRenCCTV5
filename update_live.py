import re
import requests

# 目标网页 URL
PAGE_URL = "https://huavod.cc/viv/detail/id/536/nid/1.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://huavod.cc/"
}

def get_latest_url():
    try:
        response = requests.get(PAGE_URL, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        html = response.text
        
        # 精准匹配包含 auth 的 m3u8 链接
        pattern = r'https://live\.huarenlivewebsite1\.top/stream/CCTV5_MG\.m3u8\?auth=[^\s\'"]+'
        match = re.search(pattern, html)
        
        if match:
            return match.group(0)
    except Exception as e:
        print(f"抓取失败: {e}")
    return None

def save_files(url):
    if not url:
        return
        
    # 【格式一】：生成标准的 M3U 播放列表文件 (适合用作软件里的节目列表导入)
    m3u_content = f"#EXTM3U\n#EXTINF:-1,CCTV-5 体育\n{url}\n"
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
        
    # 【格式二】：生成纯 M3U8 主索引文件 (适合作为单个独立播放源)
    # 使用 #EXT-X-STREAM-INF 标签告诉播放器这是一个 1080p 的视频流，真正的流地址在下面
    m3u8_content = (
        "#EXTM3U\n"
        "#EXT-X-VERSION:3\n"
        "#EXT-X-STREAM-INF:BANDWIDTH=8000000,RESOLUTION=1920x1080\n"
        f"{url}\n"
    )
    with open("live.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u8_content)
        
    print("live.m3u 和 live.m3u8 文件均已同步更新！")

if __name__ == "__main__":
    latest_url = get_latest_url()
    save_files(latest_url)
