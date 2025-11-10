import sys
import whisper
import datetime
import srt
import os

def to_srt(segments):
    subs = []
    for i, seg in enumerate(segments, start=1):
        start = seg['start']
        end = seg['end']
        text = seg['text'].strip()
        subs.append(srt.Subtitle(
            index=i,
            start=datetime.timedelta(seconds=start),
            end=datetime.timedelta(seconds=end),
            content=text
        ))
    return srt.compose(subs)

def to_vtt(srt_text):
    vtt = "WEBVTT\n\n"
    for line in srt_text.splitlines():
        vtt += line.replace(',', '.') + "\n"
    return vtt

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: transcribe.py input_audio.wav output_base")
        sys.exit(1)

    audio_path = sys.argv[1]
    output_base = sys.argv[2]

    print("🔊 Loading Whisper model (base)...")
    model = whisper.load_model("base")
    print("🎙️ Transcribing audio...")
    result = model.transcribe(audio_path, language="en")

    segments = result.get('segments', [])
    text_full = result.get('text', '').strip()
    srt_text = to_srt(segments)
    vtt_text = to_vtt(srt_text)

    with open(output_base + ".srt", "w", encoding="utf-8") as f:
        f.write(srt_text)
    with open(output_base + ".vtt", "w", encoding="utf-8") as f:
        f.write(vtt_text)
    with open(output_base + ".txt", "w", encoding="utf-8") as f:
        f.write(text_full)

    print("✅ Subtitles generated successfully!")
