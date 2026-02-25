"""
Location Memory Agent

Processes GPS history, place associations, and travel patterns.
"""

import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime
import json
from geopy.distance import geodesic


class LocationMemoryAgent:
    def __init__(self):
        self.gps_history = []
        self.place_associations = []
        self.travel_patterns = []

    def process_location_data(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Process location data from GPS history
        """
        location_data = []
        
        # Find location files
        location_files = self._find_location_files(data_path)
        
        for file_path in location_files:
            try:
                data = self._process_location_file(file_path)
                if data:
                    location_data.append(data)
            except Exception as e:
                print(f"Error processing location file {file_path}: {str(e)}")
                
        return location_data

    def _find_location_files(self, data_path: str) -> List[str]:
        """
        Find all location files in the data path
        """
        location_extensions = ['.csv', '.json', '.gpx', '.kml']
        files = []
        
        for root, dirs, files_list in os.walk(data_path):
            for file in files_list:
                if any(file.lower().endswith(ext) for ext in location_extensions):
                    files.append(os.path.join(root, file))
                    
        return files

    def _process_location_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a location file
        """
        try:
            # Determine file type and parse accordingly
            _, ext = os.path.splitext(file_path)
            
            if ext.lower() == '.csv':
                df = pd.read_csv(file_path)
            elif ext.lower() == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
            elif ext.lower() == '.gpx':
                # Handle GPX files (simplified)
                df = self._parse_gpx(file_path)
            else:
                return None
            
            # Analyze location data
            analysis = self._analyze_location_data(df)
            
            # Extract metadata
            metadata = self._extract_location_metadata(file_path)
            
            return {
                'type': 'location_data',
                'path': file_path,
                'analysis': analysis,
                'metadata': metadata,
                'timestamp': metadata.get('timestamp', datetime.now())
            }
        except Exception as e:
            print(f"Error processing location file {file_path}: {str(e)}")
            return None

    def _parse_gpx(self, file_path: str) -> pd.DataFrame:
        """
        Parse GPX file (simplified)
        """
        # In practice, you'd use a proper GPX parser like gpxpy
        # For now, return empty DataFrame
        return pd.DataFrame()

    def _analyze_location_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze location data
        """
        analysis = {}
        
        # Basic location statistics
        if 'latitude' in df.columns and 'longitude' in df.columns:
            analysis['total_locations'] = len(df)
            analysis['location_range'] = self._calculate_location_range(df)
            analysis['most_visited_places'] = self._identify_most_visited_places(df)
            analysis['travel_patterns'] = self._analyze_travel_patterns(df)
            
        # Time-based analysis
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            analysis['visit_frequency'] = self._analyze_visit_frequency(df)
            analysis['daily_routine'] = self._identify_daily_routine(df)
            
        return analysis

    def _calculate_location_range(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate location range
        """
        if 'latitude' in df.columns and 'longitude' in df.columns:
            latitudes = df['latitude'].dropna()
            longitudes = df['longitude'].dropna()
            
            if len(latitudes) > 0 and len(longitudes) > 0:
                return {
                    'min_latitude': latitudes.min(),
                    'max_latitude': latitudes.max(),
                    'min_longitude': longitudes.min(),
                    'max_longitude': longitudes.max()
                }
        
        return {}

    def _identify_most_visited_places(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Identify most visited places
        """
        places = []
        
        if 'latitude' in df.columns and 'longitude' in df.columns:
            # Group by location and count visits
            location_counts = df.groupby(['latitude', 'longitude']).size().sort_values(ascending=False)
            
            # Get top 10 most visited places
            for (lat, lon), count in location_counts.head(10).items():
                places.append({
                    'latitude': lat,
                    'longitude': lon,
                    'visit_count': count
                })
                
        return places

    def _analyze_travel_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze travel patterns
        """
        patterns = {}
        
        if 'latitude' in df.columns and 'longitude' in df.columns:
            # Calculate distances between consecutive locations
            distances = []
            
            for i in range(len(df) - 1):
                lat1, lon1 = df.iloc[i]['latitude'], df.iloc[i]['longitude']
                lat2, lon2 = df.iloc[i+1]['latitude'], df.iloc[i+1]['longitude']
                
                if not pd.isna(lat1) and not pd.isna(lon1) and not pd.isna(lat2) and not pd.isna(lon2):
                    distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
                    distances.append(distance)
                    
            if distances:
                patterns['average_distance_traveled'] = np.mean(distances)
                patterns['max_distance_traveled'] = np.max(distances)
                patterns['total_distance_traveled'] = sum(distances)
                
        return patterns

    def _analyze_visit_frequency(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze visit frequency
        """
        frequency = {}
        
        if 'timestamp' in df.columns:
            # Group by day and count visits
            df['date'] = df['timestamp'].dt.date
            daily_visits = df.groupby('date').size()
            
            frequency['average_daily_visits'] = daily_visits.mean()
            frequency['max_daily_visits'] = daily_visits.max()
            frequency['visit_days'] = len(daily_visits)
            
        return frequency

    def _identify_daily_routine(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Identify daily routine
        """
        routine = {}
        
        if 'timestamp' in df.columns:
            # Group by hour and count visits
            df['hour'] = df['timestamp'].dt.hour
            hourly_visits = df.groupby('hour').size()
            
            routine['peak_hours'] = hourly_visits.sort_values(ascending=False).head(3).to_dict()
            routine['average_hourly_visits'] = hourly_visits.mean()
            
        return routine

    def _extract_location_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from location file
        """
        try:
            stat = os.stat(file_path)
            
            metadata = {
                'filename': os.path.basename(file_path),
                'size': stat.st_size,
                'timestamp': datetime.fromtimestamp(stat.st_mtime),
                'format': 'location'
            }
            return metadata
        except Exception as e:
            print(f"Error extracting metadata for {file_path}: {str(e)}")
            return {}

    def create_place_profile(self, location_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a place profile from location data
        """
        profile = {
            'place_associations': self._aggregate_place_associations(location_data),
            'travel_patterns': self._aggregate_travel_patterns(location_data),
            'location_preferences': self._analyze_location_preferences(location_data),
            'timestamp': datetime.now()
        }
        
        return profile

    def _aggregate_place_associations(self, location_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aggregate place associations
        """
        associations = []
        
        for data in location_data:
            if 'analysis' in data and 'most_visited_places' in data['analysis']:
                associations.extend(data['analysis']['most_visited_places'])
                
        return associations

    def _aggregate_travel_patterns(self, location_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate travel patterns
        """
        patterns = {}
        
        # Simple aggregation - in practice, you'd use more sophisticated analysis
        total_distance = 0
        
        for data in location_data:
            if 'analysis' in data and 'travel_patterns' in data['analysis']:
                travel = data['analysis']['travel_patterns']
                if 'total_distance_traveled' in travel:
                    total_distance += travel['total_distance_traveled']
                    
        patterns['total_distance_traveled'] = total_distance
        
        return patterns

    def _analyze_location_preferences(self, location_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze location preferences
        """
        preferences = {}
        
        # Placeholder for location preference analysis
        
        return preferences


# Example usage
if __name__ == "__main__":
    agent = LocationMemoryAgent()
    data = agent.process_location_data("./data/behavioral")
    print(f"Processed {len(data)} location data items")
    
    if data:
        profile = agent.create_place_profile(data)
        print(f"Created place profile")