import math, wave, struct
from pathlib import Path

sr = 44100
duration = 30.0
nframes = int(sr * duration)
out = Path("video/assets/music.wav")
progressions = [
    (0, 10, [130.81, 164.81, 196.00, 261.63]),
    (10, 20, [110.00, 146.83, 174.61, 220.00]),
    (20, 30, [98.00, 130.81, 164.81, 196.00]),
]
melody = [(2,392.00),(5,440.00),(8,523.25),(12,493.88),(15,440.00),
          (18,392.00),(22,440.00),(25,523.25),(28,392.00)]
with wave.open(str(out), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    block=[]
    for i in range(nframes):
        t=i/sr
        fade=min(1.0, t/1.2, (duration-t)/1.7)
        chord=progressions[min(int(t//10),2)][2]
        pad=0.0
        for j,f in enumerate(chord):
            phase=2*math.pi*f*t + 0.07*math.sin(2*math.pi*0.13*t+j)
            pad += (math.sin(phase)+0.22*math.sin(2*phase))/len(chord)
        lead=0.0
        for start,f in melody:
            age=t-start
            if 0 <= age < 1.55:
                env=math.sin(math.pi*age/1.55)**1.5
                lead += 0.18*env*math.sin(2*math.pi*f*age)
        swell=0.92+0.08*math.sin(2*math.pi*t/8)
        sample=(0.11*pad+lead)*fade*swell
        left=max(-0.85,min(0.85,sample*(0.98+0.02*math.sin(t*0.4))))
        right=max(-0.85,min(0.85,sample*(0.98+0.02*math.cos(t*0.37))))
        block.append(struct.pack("<hh", int(left*32767), int(right*32767)))
        if len(block) >= 4096:
            w.writeframesraw(b"".join(block)); block=[]
    if block: w.writeframesraw(b"".join(block))
print("Wrote original 30-second instrumental bed:", out)

