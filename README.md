# VideoToStringArt
Convert videos into captivating ASCII art animations effortlessly. This Python script utilizes PIL (Pillow) to process images, transforming them into a series of ASCII art frames. Customize fonts, symbols, and output settings for unique and visually appealing results.

## Installation

Run the following command in the project root to install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Use

### 1. Splitting the Original Video into Images

```bash
mkdir -p source && ffmpeg -i input.mp4 -vf fps=24 source/%07d.jpg
```

### 2. Run Python Script

```bash
python video_to_string_art.py
```

### 3. Compose the New Video

```bash
ffmpeg -i out/%07d.jpg -c:v libx264 -vf fps=24 -pix_fmt yuv420p output.mp4
```

### 4. Merge Audio from the Original Video

```bash
ffmpeg -i input.mp4 -i output.mp4 -c:v copy -c:a copy -strict experimental -shortest final.mp4
```

## Notes

- Ensure that [ffmpeg](https://github.com/FFmpeg/FFmpeg) is installed before running the script.
- Adjust ffmpeg command parameters based on your specific requirements.

## Demo 

Check out the output video demo on [Bilibili](https://www.bilibili.com/video/BV1cu4y1N7gJ/).

## License

This project is licensed under the [MIT License](LICENSE).

