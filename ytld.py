import argparse
import os
import shutil
import signal
import sys

import yt_dlp


VIDEO_DIR = os.path.expanduser("~/Videos")
AUDIO_DIR = os.path.expanduser("~/Music")

EXIT_WORDS = {"q", "quit", "exit"}
VIDEO_WORDS = {"v", "video", "mp4"}
AUDIO_WORDS = {"a", "audio", "mp3"}


def _find_deno():
    """Locate a deno binary so yt-dlp's JS-based YouTube extractor works.
    Returns a path string, or None if deno can't be found."""
    try:
        import deno  # the pip-installed deno package
        return deno.find_deno_bin()
    except Exception:
        return shutil.which("deno")


def _sigint_handler(signum, frame):
    """Clean exit on Ctrl+C instead of a traceback."""
    print("\n  YTLD - Interrupted by user. Goodbye!")
    sys.exit(0)


signal.signal(signal.SIGINT, _sigint_handler)


def progress_hook(d):
    if d.get("status") == "downloading":
        pct = d.get("_percent_str", "N/A")
        speed = d.get("_speed_str", "N/A")
        eta = d.get("_eta_str", "N/A")
        print(f"\r  {pct} at {speed} ETA {eta}   ", end="", flush=True)
    elif d.get("status") == "finished":
        print("\n  Download complete.\n")


def build_opts(audio_only):
    common = {
        "progress_hooks": [progress_hook],
        "concurrent_fragment_downloads": True,
        "fragment_retries": 10,
        "retries": 10,
        "noprogress": False,
        "quiet": False,
        "no_warnings": False,
    }
    deno_path = _find_deno()
    if deno_path:
        common["js_runtimes"] = {"deno": {"path": deno_path}}
        common["remote_components"] = ["ejs:github", "ejs:npm"]
    if audio_only:
        os.makedirs(AUDIO_DIR, exist_ok=True)
        return {
            **common,
            "format": "bestaudio/best",
            "outtmpl": os.path.join(AUDIO_DIR, "%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    os.makedirs(VIDEO_DIR, exist_ok=True)
    return {
        **common,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": os.path.join(VIDEO_DIR, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
    }


def download(url, audio_only):
    opts = build_opts(audio_only)
    kind = "audio (MP3)" if audio_only else "video (MP4)"
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "Unknown")
        print(f"\n  [{kind}] Title: {title}")
        print("  Starting download...\n")
        if info.get("_type") == "playlist":
            # process_info() only handles single videos; let download()
            # re-extract and walk the playlist entries.
            ydl.download([url])
        else:
            # Reuse the already-extracted info so we don't download twice.
            ydl.process_info(info)
    print("  Done!\n")


def parse_urls(line):
    """Split a line into URLs, accepting spaces and/or commas."""
    return [chunk for chunk in line.replace(",", " ").split() if chunk]


def choose_mode():
    """Prompt for the default format. Returns True for audio/MP3."""
    print("  Format:")
    print("    [1] Video (MP4)")
    print("    [2] Audio (MP3)")
    while True:
        try:
            choice = input("  Choose [1]: ").strip().lower()
        except EOFError:
            return False
        if choice in ("", "1") or choice in VIDEO_WORDS:
            return False
        if choice == "2" or choice in AUDIO_WORDS:
            return True
        print("  Please enter 1 or 2.")


def interactive():
    audio_only = choose_mode()
    print("\n  Paste one or more URLs (space/comma separated).")
    print("  Commands:  v = video | a = audio/mp3 | q = quit\n")
    while True:
        try:
            line = input("  URL: ").strip()
        except EOFError:
            break
        if not line:
            continue
        lowered = line.lower()
        if lowered in EXIT_WORDS:
            break
        if lowered in VIDEO_WORDS:
            audio_only = False
            print("  -> Video mode (MP4)\n")
            continue
        if lowered in AUDIO_WORDS:
            audio_only = True
            print("  -> Audio mode (MP3)\n")
            continue
        for url in parse_urls(line):
            try:
                download(url, audio_only)
            except Exception as e:
                print(f"  Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(description="YTLD - YouTube Downloader")
    parser.add_argument("urls", nargs="*", help="one or more video URLs")
    parser.add_argument(
        "-a", "--audio", "--mp3", dest="audio", action="store_true",
        help="download as MP3 audio instead of MP4 video",
    )
    args = parser.parse_args()

    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)

    print("  YTLD - YouTube Downloader\n")

    # Non-interactive: URLs passed on the command line.
    if args.urls:
        for url in args.urls:
            try:
                download(url, args.audio)
            except Exception as e:
                print(f"  Error: {e}\n")
        return

    interactive()


if __name__ == "__main__":
    main()
