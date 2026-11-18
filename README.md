# YTLD — YouTube Downloader

A modern, cross-platform YouTube downloader with built-in **MP3 audio extraction** and **deno JS runtime** integration for reliable extraction. Built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## ✨ Features

- **🎬 Video (MP4)** — Best quality video + audio, merged to MP4
- **🎵 Audio (MP3)** — Extract audio directly to 192kbps MP3
- **🔗 Multi-URL support** — Download multiple URLs at once (CLI or interactive)
- **🧠 Smart extraction** — Auto-detects and uses **deno** JS runtime for reliable YouTube signature decryption
- **⚡ Fast & resilient** — Parallel fragment downloads, automatic retries, cached metadata
- **🖥 Cross-platform** — Works on Linux, macOS, and Windows
- **🎮 Interactive mode** — Paste URLs, switch formats on the fly
- **📦 Installable via pip** — `pipx install git+https://github.com/boegaru/ytld.git`

## 📋 Requirements

| Requirement | Linux/macOS | Windows |
|-------------|-------------|---------|
| **Python** | ≥ 3.7 | ≥ 3.7 |
| **ffmpeg** | `sudo apt install ffmpeg` / `brew install ffmpeg` | [Download ffmpeg](https://ffmpeg.org/download.html) and add to PATH |
| **deno** *(optional but recommended)* | Auto-installed via pip | Auto-installed via pip |

> **Why ffmpeg?** Required for merging video+audio and converting to MP3. yt-dlp will fail without it.
>
> **Why deno?** YouTube uses JavaScript challenges for signature decryption. The pip-installed `deno` package provides a zero-config JS runtime that yt-dlp uses automatically — no manual setup needed.

## 🚀 Installation

### Option 1: pipx (recommended — isolated environment)
```bash
pipx install git+https://github.com/boegaru/ytld.git
# Then run anywhere:
ytld https://youtu.be/dQw4w9WgXcQ
```

### Option 2: pip (into your user site-packages)
```bash
pip install git+https://github.com/boegaru/ytld.git
```

### Option 3: From source (editable / development)
```bash
git clone https://github.com/boegaru/ytld.git
cd ytld
pip install -e .
```

### Option 4: Run without installing
```bash
git clone https://github.com/boegaru/ytld.git
cd ytld
python -m ytld https://youtu.be/dQw4w9WgXcQ
```

## 🎯 Quick Start

```bash
# Download a video (MP4) — default
ytld https://youtu.be/dQw4w9WgXcQ

# Download multiple videos
ytld https://youtu.be/dQw4w9WgXcQ https://youtu.be/9bZkp7q19f0

# Download as MP3 audio
ytld -a https://youtu.be/dQw4w9WgXcQ
ytld --mp3 https://youtu.be/dQw4w9WgXcQ

# Download multiple as MP3
ytld -a https://youtu.be/dQw4w9WgXcQ https://youtu.be/9bZkp7q19f0

# Interactive mode (no arguments)
ytld
```

## 📖 Usage

### Command-line

```
ytld [options] [URLS...]

Positional arguments:
  URLS            one or more video URLs (space-separated)

Options:
  -a, --audio, --mp3   download as MP3 audio instead of MP4 video
  -h, --help           show this help message and exit
```

**Examples:**
```bash
# Single video
ytld "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Single audio
ytld -a "https://youtu.be/dQw4w9WgXcQ"

# Multiple videos
ytld "https://youtu.be/dQw4w9WgXcQ" "https://youtu.be/9bZkp7q19f0"

# Multiple audio
ytld --mp3 "https://youtu.be/dQw4w9WgXcQ" "https://youtu.be/9bZkp7q19f0"
```

### Interactive Mode

Run `ytld` with no arguments:
```
$ ytld
  YTLD - YouTube Downloader

  Format:
    [1] Video (MP4)
    [2] Audio (MP3)
  Choose [1]: 2

  Paste one or more URLs (space/comma separated).
  Commands:  v = video | a = audio/mp3 | q = quit

  URL: https://youtu.be/dQw4w9WgXcQ, https://youtu.be/9bZkp7q19f0
  URL: a
  -> Audio mode (MP3)

  URL: q
```

- **Type `v` / `video` / `mp4`** → switch to video mode
- **Type `a` / `audio` / `mp3`** → switch to audio mode
- **Type `q` / `quit` / `exit`** or press `Ctrl+D` / `Ctrl+C` → quit
- Paste **one or many URLs** (space or comma separated)

## 📁 Output Locations

| Mode | Default Directory |
|------|-------------------|
| Video (MP4) | `~/Videos/` |
| Audio (MP3) | `~/Music/` |

> These are standard user directories on Linux/macOS/Windows.

## 🔧 Advanced / Troubleshooting

### "No supported JavaScript runtime" warning
If you see this warning, yt-dlp fell back to extraction without a JS runtime (some formats may be missing). The pip-installed `deno` package should auto-provide it. If not:
```bash
pip install deno
```

### ffmpeg not found
```
ERROR: ffmpeg not found. Please install ffmpeg.
```
- **Linux**: `sudo apt install ffmpeg` / `sudo dnf install ffmpeg` / `sudo pacman -S ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from https://ffmpeg.org/download.html → extract → add `bin/` to PATH

### Permission errors on Linux
```bash
mkdir -p ~/Videos ~/Music
chmod u+rwx ~/Videos ~/Music
```

### Update ytld
```bash
pipx upgrade ytld          # if installed via pipx
pip install -U git+https://github.com/boegaru/ytld.git  # if via pip
```

## 🧪 Development

```bash
# Clone & install in editable mode
git clone https://github.com/boegaru/ytld.git
cd ytld
pip install -e .
```

### Project Structure
```
ytld/
├── pyproject.toml      # Package metadata, dependencies, entry points
├── ytld.py             # Main module (CLI entry point is ytld:main)
├── README.md           # This file
├── LICENSE             # MIT License
└── .gitignore          # Git ignore rules
```

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — the powerful downloader underneath
- [deno](https://deno.land/) — the JS runtime that makes extraction reliable
- [ffmpeg](https://ffmpeg.org/) — the multimedia processing backbone
