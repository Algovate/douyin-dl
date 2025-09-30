---
noteId: "89dea6809d9a11f09ecf0f3fdc071175"
tags: []

---

# FFmpeg MP4转MP3简明指南

## 基本转换命令

```bash
ffmpeg -i input.mp4 output.mp3
```

## 常用参数说明

### 音频质量设置
```bash
# 设置比特率为128kbps（推荐）
ffmpeg -i input.mp4 -b:a 128k output.mp3

# 设置比特率为320kbps（高质量）
ffmpeg -i input.mp4 -b:a 320k output.mp3
```

### 音频采样率设置
```bash
# 设置采样率为44.1kHz（CD质量）
ffmpeg -i input.mp4 -ar 44100 output.mp3

# 设置采样率为48kHz（高质量）
ffmpeg -i input.mp4 -ar 48000 output.mp3
```

## 实用命令示例

### 批量转换
```bash
# 转换当前目录下所有MP4文件
for file in *.mp4; do
    ffmpeg -i "$file" -b:a 128k "${file%.mp4}.mp3"
done
```

### 指定输出目录
```bash
ffmpeg -i input.mp4 -b:a 128k /path/to/output/output.mp3
```

### 转换并删除原文件
```bash
ffmpeg -i input.mp4 -b:a 128k output.mp3 && rm input.mp4
```

## 推荐设置

对于大多数用途，推荐使用以下命令：
```bash
ffmpeg -i input.mp4 -b:a 128k -ar 44100 output.mp3
```

这个设置提供：
- 128kbps比特率（平衡文件大小和音质）
- 44.1kHz采样率（标准音频质量）

## 注意事项

1. 确保已安装FFmpeg：`ffmpeg -version`
2. 输出文件会自动覆盖同名文件
3. 转换过程可能需要一些时间，取决于文件大小
4. 建议在转换前备份重要文件
