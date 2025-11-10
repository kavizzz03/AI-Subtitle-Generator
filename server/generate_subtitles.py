# generate_subtitles.py
import sys
import whisper
import srt
from datetime import timedelta
from pathlib import Path

def flush_print(text):
    print(text, flush=True)  # real-time output to Node.js

def main():
    video_path = sys.argv[1]
    srt_path = sys.argv[2]
    source_lang = sys.argv[3] if len(sys.argv) > 3 else "en"

    flush_print(f"Python: Step 2.1: Loading Whisper multilingual model for '{source_lang}'...")
    model = whisper.load_model("small")  # supports translation

    flush_print("Step 2.2: Transcribing and translating to English (please wait)...")

    # Transcribe + translate to English
    result = model.transcribe(
        video_path,
        task="translate",  # ensures English subtitles
        language=source_lang
    )

    flush_print("Step 2.3: Writing subtitles to SRT file (UTF-8)...")

    subtitles = []
    for i, seg in enumerate(result["segments"], start=1):
        start_td = timedelta(seconds=float(seg["start"]))
        end_td = timedelta(seconds=float(seg["end"]))
        text = seg["text"].strip()

        subtitles.append(srt.Subtitle(index=i, start=start_td, end=end_td, content=text))
        if i % 5 == 0:
            flush_print(f"Writing segment {i}: {text[:100]}")

    Path(srt_path).parent.mkdir(parents=True, exist_ok=True)
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subtitles))

    flush_print(f"[✅ SUCCESS] Subtitle saved to {srt_path}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
