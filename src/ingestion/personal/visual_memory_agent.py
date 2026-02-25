"""
Visual Memory Agent

Processes photos, videos, and facial expression analysis to extract visual memories.
"""

import os
import cv2
import numpy as np
from typing import List, Dict, Any
from datetime import datetime
import face_recognition
import json


class VisualMemoryAgent:
    def __init__(self):
        self.face_encodings = []
        self.face_locations = []
        self.face_landmarks = []
        self.image_metadata = []

    def process_visual_data(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Process visual data from photos and videos
        """
        visual_data = []
        
        # Process images
        images = self._find_images(data_path)
        for image_path in images:
            try:
                image_data = self._process_image(image_path)
                if image_data:
                    visual_data.append(image_data)
            except Exception as e:
                print(f"Error processing image {image_path}: {str(e)}")
                
        # Process videos
        videos = self._find_videos(data_path)
        for video_path in videos:
            try:
                video_data = self._process_video(video_path)
                if video_data:
                    visual_data.extend(video_data)
            except Exception as e:
                print(f"Error processing video {video_path}: {str(e)}")
                
        return visual_data

    def _find_images(self, data_path: str) -> List[str]:
        """
        Find all image files in the data path
        """
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        images = []
        
        for root, dirs, files in os.walk(data_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    images.append(os.path.join(root, file))
                    
        return images

    def _find_videos(self, data_path: str) -> List[str]:
        """
        Find all video files in the data path
        """
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
        videos = []
        
        for root, dirs, files in os.walk(data_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    videos.append(os.path.join(root, file))
                    
        return videos

    def _process_image(self, image_path: str) -> Dict[str, Any]:
        """
        Process a single image file
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # Extract face encodings
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            # Extract facial landmarks
            face_landmarks_list = face_recognition.face_landmarks(image)
            
            # Extract metadata
            metadata = self._extract_image_metadata(image_path)
            
            return {
                'type': 'image',
                'path': image_path,
                'face_locations': face_locations,
                'face_encodings': face_encodings,
                'face_landmarks': face_landmarks_list,
                'metadata': metadata,
                'timestamp': metadata.get('timestamp', datetime.now())
            }
        except Exception as e:
            print(f"Error processing image {image_path}: {str(e)}")
            return None

    def _process_video(self, video_path: str) -> List[Dict[str, Any]]:
        """
        Process a video file to extract visual memories
        """
        try:
            cap = cv2.VideoCapture(video_path)
            frames = []
            
            # Extract frames at regular intervals
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            interval = max(1, int(fps / 2))  # Extract 2 frames per second
            
            frame_num = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_num % interval == 0:
                    # Extract face information
                    face_locations = face_recognition.face_locations(frame)
                    face_encodings = face_recognition.face_encodings(frame, face_locations)
                    
                    # Extract facial landmarks
                    face_landmarks_list = face_recognition.face_landmarks(frame)
                    
                    frames.append({
                        'type': 'video_frame',
                        'frame_number': frame_num,
                        'face_locations': face_locations,
                        'face_encodings': face_encodings,
                        'face_landmarks': face_landmarks_list,
                        'timestamp': datetime.now()
                    })
                
                frame_num += 1
                
            cap.release()
            return frames
        except Exception as e:
            print(f"Error processing video {video_path}: {str(e)}")
            return []

    def _extract_image_metadata(self, image_path: str) -> Dict[str, Any]:
        """
        Extract metadata from image file
        """
        try:
            # This is a simplified version - in practice, you'd use exifread or similar
            metadata = {
                'filename': os.path.basename(image_path),
                'size': os.path.getsize(image_path),
                'timestamp': datetime.now(),
                'format': 'image'
            }
            return metadata
        except Exception as e:
            print(f"Error extracting metadata for {image_path}: {str(e)}")
            return {}


# Example usage
if __name__ == "__main__":
    agent = VisualMemoryAgent()
    data = agent.process_visual_data("./data/personal")
    print(f"Processed {len(data)} visual data items")