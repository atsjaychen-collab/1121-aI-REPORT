import wave
p="video/assets/voice-test.wav"
with wave.open(p,"rb") as w: print(w.getnframes()/w.getframerate())

