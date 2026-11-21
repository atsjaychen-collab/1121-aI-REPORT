import wave
from pathlib import Path
for p in sorted(Path("video/assets").glob("voice-*.wav")):
    with wave.open(str(p), "rb") as w:
        print(p.name, w.getnframes()/w.getframerate(), w.getframerate(), w.getnchannels())

