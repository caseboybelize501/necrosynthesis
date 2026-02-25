"""
Relationship Mapper

Maps social graph dynamics, interaction styles per person, and relationship patterns.
"""

import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime
import json
from collections import defaultdict


class RelationshipMapper:
    def __init__(self):
        self.social_graph = {}
        self.interaction_patterns = []
        self.relationship_strengths = []

    def map_relationships(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Map social relationships from communication data
        """
        relationship_data = []
        
        # Find relationship files
        relationship_files = self._find_relationship_files(data_path)
        
        for file_path in relationship_files:
            try:
                data = self._process_relationship_file(file_path)
                if data:
                    relationship_data.append(data)
            except Exception as e:
                print(f"Error processing relationship file {file_path}: {str(e)}")
                
        return relationship_data

    def _find_relationship_files(self, data_path: str) -> List[str]:
        """
        Find all relationship files in the data path
        """
        relationship_extensions = ['.csv', '.json', '.xlsx', '.xls']
        files = []
        
        for root, dirs, files_list in os.walk(data_path):
            for file in files_list:
                if any(file.lower().endswith(ext) for ext in relationship_extensions):
                    files.append(os.path.join(root, file))
                    
        return files

    def _process_relationship_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a relationship file
        """
        try:
            # Determine file type and parse accordingly
            _, ext = os.path.splitext(file_path)
            
            if ext.lower() == '.csv':
                df = pd.read_csv(file_path)
            elif ext.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif ext.lower() == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
            else:
                return None
            
            # Analyze relationships
            analysis = self._analyze_relationships(df)
            
            # Extract metadata
            metadata = self._extract_relationship_metadata(file_path)
            
            return {
                'type': 'relationship_data',
                'path': file_path,
                'analysis': analysis,
                'metadata': metadata,
                'timestamp': metadata.get('timestamp', datetime.now())
            }
        except Exception as e:
            print(f"Error processing relationship file {file_path}: {str(e)}")
            return None

    def _analyze_relationships(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze social relationships
        """
        analysis = {}
        
        # Social graph analysis
        analysis['social_graph'] = self._build_social_graph(df)
        
        # Interaction patterns
        analysis['interaction_patterns'] = self._analyze_interaction_patterns(df)
        
        # Relationship strengths
        analysis['relationship_strengths'] = self._analyze_relationship_strengths(df)
        
        # Communication frequency
        analysis['communication_frequency'] = self._analyze_communication_frequency(df)
        
        return analysis

    def _build_social_graph(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Build social graph from relationship data
        """
        graph = defaultdict(list)
        
        # Simple approach - in practice, you'd use more sophisticated graph analysis
        if 'person1' in df.columns and 'person2' in df.columns:
            for _, row in df.iterrows():
                person1 = row['person1']
                person2 = row['person2']
                
                if person1 and person2:
                    graph[person1].append(person2)
                    graph[person2].append(person1)
                    
        return dict(graph)

    def _analyze_interaction_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze interaction patterns
        """
        patterns = {}
        
        # Simple pattern analysis
        if 'person1' in df.columns and 'person2' in df.columns:
            # Count interactions per person
            interaction_counts = df.groupby('person1').size()
            patterns['most_active_person'] = interaction_counts.idxmax()
            patterns['total_interactions'] = interaction_counts.sum()
            
        return patterns

    def _analyze_relationship_strengths(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze relationship strengths
        """
        strengths = {}
        
        # Simple strength analysis
        if 'person1' in df.columns and 'person2' in df.columns:
            # In practice, you'd use more sophisticated metrics
            # For now, we'll use interaction count as a proxy
            strength_metrics = df.groupby(['person1', 'person2']).size().to_dict()
            strengths['strength_metrics'] = strength_metrics
            
        return strengths

    def _analyze_communication_frequency(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze communication frequency
        """
        frequency = {}
        
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Group by date and count communications
            df['date'] = df['timestamp'].dt.date
            daily_counts = df.groupby('date').size()
            
            frequency['average_daily_communications'] = daily_counts.mean()
            frequency['peak_communication_days'] = daily_counts.sort_values(ascending=False).head(5).to_dict()
            
        return frequency

    def _extract_relationship_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from relationship file
        """
        try:
            stat = os.stat(file_path)
            
            metadata = {
                'filename': os.path.basename(file_path),
                'size': stat.st_size,
                'timestamp': datetime.fromtimestamp(stat.st_mtime),
                'format': 'relationship'
            }
            return metadata
        except Exception as e:
            print(f"Error extracting metadata for {file_path}: {str(e)}")
            return {}

    def create_social_profile(self, relationship_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a social profile from relationship data
        """
        profile = {
            'social_graph': self._aggregate_social_graph(relationship_data),
            'interaction_patterns': self._aggregate_interaction_patterns(relationship_data),
            'relationship_strengths': self._aggregate_relationship_strengths(relationship_data),
            'timestamp': datetime.now()
        }
        
        return profile

    def _aggregate_social_graph(self, relationship_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate social graph
        """
        graph = defaultdict(list)
        
        for data in relationship_data:
            if 'analysis' in data and 'social_graph' in data['analysis']:
                for person, connections in data['analysis']['social_graph'].items():
                    for connection in connections:
                        if connection not in graph[person]:
                            graph[person].append(connection)
                            
        return dict(graph)

    def _aggregate_interaction_patterns(self, relationship_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate interaction patterns
        """
        patterns = {}
        
        # Simple aggregation - in practice, you'd use more sophisticated analysis
        total_interactions = 0
        
        for data in relationship_data:
            if 'analysis' in data and 'interaction_patterns' in data['analysis']:
                patterns.update(data['analysis']['interaction_patterns'])
                
        return patterns

    def _aggregate_relationship_strengths(self, relationship_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate relationship strengths
        """
        strengths = {}
        
        # Simple aggregation - in practice, you'd use more sophisticated analysis
        
        for data in relationship_data:
            if 'analysis' in data and 'relationship_strengths' in data['analysis']:
                strengths.update(data['analysis']['relationship_strengths'])
                
        return strengths


# Example usage
if __name__ == "__main__":
    mapper = RelationshipMapper()
    data = mapper.map_relationships("./data/behavioral")
    print(f"Mapped {len(data)} relationship data items")
    
    if data:
        profile = mapper.create_social_profile(data)
        print(f"Created social profile")