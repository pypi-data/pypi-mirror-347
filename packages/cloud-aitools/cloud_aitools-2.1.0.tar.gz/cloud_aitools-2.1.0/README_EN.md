# cloud-aitools - AI Model Management Tool

cloud-aitools is a CLI tool for managing AI models on Tencent Cloud, providing high-performance upload, download and model management capabilities.

## Key Features

- 🚀 **High Performance Transfer**: Supports coroutine/multi-process concurrent operations for accelerated large model transfers (Internal network download speeds up to 90Gb/s, tested DeepSeek-R1 671B model (641GB) downloaded to local memory in just 1 minute 20 seconds)
- 🔍 **Model Management**: Supports model listing, uploading, downloading and other operations
- 🌐 **Smart Region Detection**: Automatically detects COS internal network region based on current network environment
- 🔒 **Data Verification**: Uses Blake3 algorithm to ensure file integrity
- 📊 **Progress Display**: Real-time transfer progress and speed monitoring
- 🔧 **Flexible Configuration**: Supports private deployment, custom bucket naming, region selection, etc.

## Installation Guide

### Prerequisites

- Python 3.12+
- pip
- uv (optional)

### Installation Methods

#### uv (Recommended)

```bash
# install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh

# or use pip to install uv
pip3 install uv --index-url https://mirrors.tencentyun.com/pypi/simple/

# Optional, for those who cannot access github.com
export UV_PYTHON_INSTALL_MIRROR="https://gh-proxy.com/github.com/indygreg/python-build-standalone/releases/download"

# install cloud-aitools
uv tool install cloud-aitools@latest --index-url https://mirrors.tencentyun.com/pypi/simple/
```

#### pip

```bash
pip3 install cloud-aitools --index-url https://mirrors.tencentyun.com/pypi/simple/ --trusted-host mirrors.tencentyun.com
```

## Usage

### Basic Command

```bash
aitools [OPTIONS] COMMAND [ARGS]...
```

### Upload Model

```bash
aitools model upload \
  --secret-id YOUR_SECRET_ID \
  --secret-key YOUR_SECRET_KEY \
  --local-path /path/to/model \
  --model-name model_name \
  --bucket-pattern bucket-appid \
  --region ap-shanghai
```

### Download Model

```bash
aitools model download model_name \
  --output /path/to/save \
  --region ap-shanghai
  -o /dev/shm
```

### List Models

```bash
aitools model list
```

### Detect Current Region

```bash
aitools get-region
```

## Configuration Options

### Common Parameters

- `--verbose/-v`: Enable verbose logging
- `--region`: Specify COS region
- `--bucket-pattern`: Bucket naming pattern (bucket-appid)
- `--process-num/-p`: Number of download processes (default 64)

## Development Guide

### Project Structure

```
cloud_aitools/
├── handler/          # Handlers
│   └── cos_handler.py # COS operations implementation
├── model/            # Data models and business logic
├── utils/            # Utility classes
│   ├── async_downloader.py # Async downloader
│   ├── dns.py        # DNS and region detection
│   └── progress.py   # Progress display
└── main.py           # Main entry
```

### Dependency Management

Project uses `uv` for dependency management, main dependencies include:

- `qcloud_cos`: Tencent Cloud COS SDK
- `minio`: MinIO client
- `aiohttp`: Async HTTP client
- `blake3`: Fast hashing algorithm

## License

MIT License

Copyright (c) 2025 cloud-aitools

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
