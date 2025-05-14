from pydub import AudioSegment
from typing import Union, Optional
import os

class EzPyDub:
    """A simplified interface for pydub audio manipulation."""
    
    def __init__(self, file_path: Optional[str] = None):
        """Initialize with an optional audio file."""
        self.audio = None
        if file_path:
            self.load(file_path)
    
    def load(self, file_path: str) -> None:
        """Load an audio file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        self.audio = AudioSegment.from_file(file_path)
    
    def trim(self, start_ms: int, end_ms: Optional[int] = None) -> None:
        """Trim audio from start_ms to end_ms (in milliseconds)."""
        if self.audio is None:
            raise ValueError("No audio loaded")
        if end_ms is None:
            self.audio = self.audio[start_ms:]
        else:
            self.audio = self.audio[start_ms:end_ms]
    
    def concatenate(self, other: 'EzPyDub') -> None:
        """Concatenate another EzPyDub audio to this one."""
        if self.audio is None or other.audio is None:
            raise ValueError("One or both audio files not loaded")
        self.audio = self.audio + other.audio
    
    def adjust_volume(self, gain_db: float) -> None:
        """Adjust volume by gain_db (positive to increase, negative to decrease)."""
        if self.audio is None:
            raise ValueError("No audio loaded")
        self.audio = self.audio + gain_db
    
    def export(self, file_path: str, format: Optional[str] = None) -> None:
        """Export audio to file_path with optional format (e.g., 'mp3', 'wav')."""
        if self.audio is None:
            raise ValueError("No audio loaded")
        if format is None:
            format = os.path.splitext(file_path)[1].lstrip(".").lower()
        self.audio.export(file_path, format=format)
    
    def get_duration(self) -> float:
        """Get audio duration in seconds."""
        if self.audio is None:
            raise ValueError("No audio loaded")
        return len(self.audio) / 1000.0
