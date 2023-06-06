import time
import base64
import binascii
import functions_framework
from pydub import AudioSegment
import magic


@functions_framework.http
def validate_input_format(request):
    request_input = request.get_json(silent=True)
    start = time.time()

    try:
        assert 'file' in request_input, "Missing 'file' key in the request input"
    except AssertionError:
        return {"info": "Fail! input payload must contain 'file' key"}

    try:
        assert is_base64(request_input['file']
                         ), "Input is not a valid Base64 string"
    except AssertionError:
        return {"info": "Fail! file must convert to base64"}

    request_input['file'] = base64.b64decode(request_input['file'])
    magic_output = magic.from_buffer(request_input['file'])
    print(f"Get file info {magic_output}")

    file_extension = determine_file_format(magic_output)
    if not file_extension:
        print(magic_output)
        return {"info": f"Fail! File type must be ['.m4a', '.mp4', '.mov', '.mp3', '.wav', '.flac'], I got {magic_output} from magic"}
    print(f"Get file extension {file_extension}")

    path = f"target{file_extension}"
    print(f"write path : {path}")
    with open(path, "wb") as f:
        f.write(request_input['file'])

    wav_path = "inference.wav"
    convert_to_wav(path, file_extension, wav_path)

    # fake output
    output_binary = base64.b64encode(
        convert_file_to_binary(wav_path)).decode('utf-8')
    response = {"wav": output_binary, "time": str(
        time.time() - start), "info": "convert success"}
    return response


def determine_file_format(magic_output):
    file_formats = {
        '.MOV': '.mov',
        'MP4': '.mp4',
        '.M4A': '.m4a',
        'ID3': '.mp3',
        'WAVE': '.wav',
        'FLAC': '.flac'
    }

    for pattern, file_type in file_formats.items():
        if pattern in magic_output:
            return file_type

    return None


def convert_to_wav(filepath, file_extension, wav_path):
    if file_extension in ['.m4a', '.mp4', '.mov', '.mp3', '.wav', '.flac']:
        print(f"change from {file_extension[1:]} to wav")
        audio = AudioSegment.from_file(
            filepath, format=file_extension[1:])  # Exclude the dot in format
        audio = audio.set_frame_rate(16000)  # Change frame rate to 16k
        # Change sample width to 16 bit (2 bytes)
        audio = audio.set_sample_width(2)
        audio = audio.set_channels(1)  # Change audio to mono
        audio.export(wav_path, format='wav')
        print(f'File has been converted to: {wav_path}')
    else:
        print('Invalid file format')


def convert_file_to_binary(file_path):
    try:
        with open(file_path, 'rb') as file:
            binary_string = file.read()
        return binary_string
    except IOError:
        print(f"Error: Unable to read the file at '{file_path}'")
        return None


def is_base64(input_str):
    try:
        base64.b64decode(input_str, validate=True)
        return True
    except (binascii.Error, TypeError):
        return False
