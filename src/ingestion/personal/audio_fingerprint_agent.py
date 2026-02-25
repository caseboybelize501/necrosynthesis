"""
Audio Fingerprint Agent

Processes voice recordings to create voice models and speech patterns.
"""

import os
import librosa
import numpy as np
from typing import List, Dict, Any
from datetime import datetime
import soundfile as sf
import json


class AudioFingerprintAgent:
    def __init__(self):
        self.voice_samples = []
        self.speech_patterns = []
        self.voice_models = []

    def process_audio_data(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Process audio data from voice recordings
        """
        audio_data = []
        
        # Find audio files
        audio_files = self._find_audio_files(data_path)
        
        for audio_path in audio_files:
            try:
                audio_info = self._process_audio_file(audio_path)
                if audio_info:
                    audio_data.append(audio_info)
            except Exception as e:
                print(f"Error processing audio file {audio_path}: {str(e)}")
                
        return audio_data

    def _find_audio_files(self, data_path: str) -> List[str]:
        """
        Find all audio files in the data path
        """
        audio_extensions = ['.mp3', '.wav', '.flac', '.m4a', '.aac']
        audio_files = []
        
        for root, dirs, files in os.walk(data_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in audio_extensions):
                    audio_files.append(os.path.join(root, file))
                    
        return audio_files

    def _process_audio_file(self, audio_path: str) -> Dict[str, Any]:
        """
        Process a single audio file
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=None)
            
            # Extract features
            features = self._extract_audio_features(y, sr)
            
            # Extract speech patterns
            speech_patterns = self._extract_speech_patterns(y, sr)
            
            # Extract metadata
            metadata = self._extract_audio_metadata(audio_path)
            
            return {
                'type': 'audio',
                'path': audio_path,
                'features': features,
                'speech_patterns': speech_patterns,
                'metadata': metadata,
                'timestamp': metadata.get('timestamp', datetime.now())
            }
        except Exception as e:
            print(f"Error processing audio file {audio_path}: {str(e)}")
            return None

    def _extract_audio_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """
        Extract audio features for voice modeling
        """
        features = {}
        
        # Basic audio features
        features['duration'] = librosa.get_duration(y=y, sr=sr)
        features['sample_rate'] = sr
        
        # Spectral features
        features['spectral_centroids'] = librosa.feature.spectral_centroid(y=y, sr=sr).tolist()
        features['spectral_rolloff'] = librosa.feature.spectral_rolloff(y=y, sr=sr).tolist()
        features['zero_crossing_rate'] = librosa.feature.zero_crossing_rate(y).tolist()
        
        # MFCC features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features['mfcc'] = mfccs.tolist()
        
        # Tempo and beat features
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        features['tempo'] = tempo
        
        return features

    def _extract_speech_patterns(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """
        Extract speech patterns and prosody
        """
        patterns = {}
        
        # Pitch extraction
        pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
        patterns['pitch'] = pitches.tolist()
        
        # Formants (simplified)
        # In practice, you'd use more sophisticated formant analysis
        
        # Speech rate
        patterns['speech_rate'] = len(y) / sr
        
        return patterns

    def _extract_audio_metadata(self, audio_path: str) -> Dict[str, Any]:
        """
        Extract metadata from audio file
        """
        try:
            # Get file info
            stat = os.stat(audio_path)
            
            metadata = {
                'filename': os.path.basename(audio_path),
                'size': stat.st_size,
                'timestamp': datetime.fromtimestamp(stat.st_mtime),
                'format': 'audio'
            }
            return metadata
        except Exception as e:
            print(f"Error extracting metadata for {audio_path}: {str(e)}")
            return {}

    def create_voice_model(self, audio_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a voice model from audio data
        """
        # This would be a more complex process involving neural networks
        # For now, we'll return a simplified model
        
        voice_model = {
            'model_type': 'voice_fingerprint',
            'data_samples': len(audio_data),
            'features': self._aggregate_features(audio_data),
            'timestamp': datetime.now()
        }
        
        return voice_model

    def _aggregate_features(self, audio_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate features from multiple audio samples
        """
        aggregated = {}
        
        # Simple averaging of features
        if audio_data:
            # Get all feature keys
            feature_keys = set()
            for item in audio_data:
                if 'features' in item:
                    feature_keys.update(item['features'].keys())
            
            # Aggregate features
            for key in feature_keys:
                values = []
                for item in audio_data:
                    if 'features' in item and key in item['features']:
                        values.append(item['features'][key])
                
                if values:
                    # For numerical features, take average
                    if isinstance(values[0], list):
                        # For arrays, take mean of each element
                        if len(values[0]) > 0:
                            aggregated[key] = [np.mean([v[i] for v in values if i < len(v)]) 
                                             for i in range(len(values[0]))]
                    else:
                        aggregated[key] = np.mean(values)
                
        return aggregated


# Example usage
if __name__ == "__main__":
    agent = AudioFingerprintAgent()
    data = agent.process_audio_data("./data/personal")
    print(f"Processed {len(data)} audio items")
    
    if data:
        model = agent.create_voice_model(data)
        print(f"Created voice model with {model['data_samples']} samples")