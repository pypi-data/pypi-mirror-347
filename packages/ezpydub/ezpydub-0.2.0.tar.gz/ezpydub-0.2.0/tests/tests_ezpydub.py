import pytest
import os
from ezpydub import EzPyDub

@pytest.fixture
def sample_audio(tmp_path):
    from pydub import AudioSegment
    audio = AudioSegment.silent(duration=5000)  # 5 seconds of silence
    file_path = tmp_path / "test.wav"
    audio.export(file_path, format="wav")
    return str(file_path)

def test_load(sample_audio):
    ez = EzPyDub(sample_audio)
    assert ez.audio is not None
    assert ez.get_duration() == 5.0

def test_trim(sample_audio):
    ez = EzPyDub(sample_audio)
    ez.trim(1000, 3000)
    assert ez.get_duration() == 2.0

def test_concatenate(sample_audio):
    ez1 = EzPyDub(sample_audio)
    ez2 = EzPyDub(sample_audio)
    ez1.concatenate(ez2)
    assert ez1.get_duration() == 10.0

def test_adjust_volume(sample_audio):
    ez = EzPyDub(sample_audio)
    original_dbfs = ez.audio.dBFS
    ez.adjust_volume(3.0)
    assert ez.audio.dBFS > original_dbfs

def test_export(sample_audio, tmp_path):
    ez = EzPyDub(sample_audio)
    output_path = tmp_path / "output.mp3"
    ez.export(str(output_path), format="mp3")
    assert os.path.exists(output_path)
