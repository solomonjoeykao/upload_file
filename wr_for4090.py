import json
import torch
import numpy as np
import wenetruntime as wenet
from scipy.io import wavfile
import sys

wenet.set_log_level(2)
decoder = wenet.Decoder('model_shichan')
test_wav = sys.argv[1]

def recognition(audio):
    sr, y = wavfile.read(audio)
    assert sr in [48000, 16000, 8000]
    if sr == 48000:  # Optional resample to 16000
        y = (y / max(np.max(y), 1) * 32767)[::3].astype("int16")
    if sr == 8000:
        print("Audio file must be 16k or 48k wav")
    ans = decoder.decode(y.tobytes(), True)
    print(ans)
    return json.loads(ans)

# text = "Speech Recognition in WeNet"
# gr.Interface(recognition, inputs="file", outputs="json",
#              description=text).launch()
recognition(test_wav)