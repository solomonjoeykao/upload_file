# from pyannote.audio import Pipeline

# offline_vad = Pipeline.from_pretrained("config.yaml")
# dia = offline_vad("246178__ceen__street-interview.wav")


# for speech_turn, track, speaker in dia.itertracks(yield_label=True):
#     print(f"{speech_turn.start:4.1f} {speech_turn.end:4.1f} {speaker}")

from huggingface_hub import HfApi
available_pipelines = [p.modelId for p in HfApi().list_models(filter="pyannote-audio-pipeline")]
list(filter(lambda p: p.startswith("pyannote/"), available_pipelines))

from huggingface_hub import notebook_login
notebook_login()

from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@develop", use_auth_token="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")

dia = pipeline("an4_diarize_test.wav")

from pyannote.core import Annotation
assert isinstance(dia, Annotation)

for speech_turn, track, speaker in dia.itertracks(yield_label=True):
    print(f"{speech_turn.start:4.4f} {speech_turn.end:4.4f} {speaker}")
     