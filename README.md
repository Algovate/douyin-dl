# Douyin 下载器（命令行）

## 项目用途

一个简单好用的命令行工具，从抖音网页获取真实视频地址，并把视频下载到本地。

## 使用方法

1) 安装依赖（首次使用需要安装 Playwright 浏览器）

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

2) 基本用法

```bash
# 直接下载（支持短链和视频页链接）
./douyin-dl 'https://v.douyin.com/xxxxxx/'
./douyin-dl 'https://www.douyin.com/video/1234567890'

# 指定输出文件名
./douyin-dl 'https://www.douyin.com/video/1234567890' -o out.mp4

# 指定输出目录与超时时间（秒）
./douyin-dl 'https://www.douyin.com/video/1234567890' --outdir downloads --timeout 20

# 显示浏览器窗口（便于调试）
./douyin-dl 'https://v.douyin.com/xxxxxx/' --headful

# 静默模式（不显示进度）与重试次数
./douyin-dl 'https://v.douyin.com/xxxxxx/' --quiet --retries 3
```

说明：

- 下载过程会在终端显示进度（已传输、百分比、速度、预计剩余时间）。
- 如果遇到间歇性失败，可通过 `--retries` 增加重试次数。

