"""
Transaction Analyzer

Analyzes spending patterns, financial decision logic, and financial behavior.
"""

import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime
import json


class TransactionAnalyzer:
    def __init__(self):
        self.spending_patterns = []
        self.decision_logic = []
        self.financial_traits = []

    def analyze_transactions(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Analyze financial transaction data
        """
        transaction_data = []
        
        # Find transaction files
        transaction_files = self._find_transaction_files(data_path)
        
        for file_path in transaction_files:
            try:
                data = self._process_transaction_file(file_path)
                if data:
                    transaction_data.append(data)
            except Exception as e:
                print(f"Error processing transaction file {file_path}: {str(e)}")
                
        return transaction_data

    def _find_transaction_files(self, data_path: str) -> List[str]:
        """
        Find all transaction files in the data path
        """
        transaction_extensions = ['.csv', '.xlsx', '.xls', '.json']
        files = []
        
        for root, dirs, files_list in os.walk(data_path):
            for file in files_list:
                if any(file.lower().endswith(ext) for ext in transaction_extensions):
                    files.append(os.path.join(root, file))
                    
        return files

    def _process_transaction_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a transaction file
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
            
            # Analyze transactions
            analysis = self._analyze_transactions(df)
            
            # Extract metadata
            metadata = self._extract_transaction_metadata(file_path)
            
            return {
                'type': 'transaction_data',
                'path': file_path,
                'analysis': analysis,
                'metadata': metadata,
                'timestamp': metadata.get('timestamp', datetime.now())
            }
        except Exception as e:
            print(f"Error processing transaction file {file_path}: {str(e)}")
            return None

    def _analyze_transactions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze transaction data
        """
        analysis = {}
        
        # Basic statistics
        if 'amount' in df.columns:
            analysis['total_spent'] = df['amount'].sum()
            analysis['average_transaction'] = df['amount'].mean()
            analysis['transaction_count'] = len(df)
            analysis['spending_categories'] = self._categorize_spending(df)
            
        # Time-based analysis
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            analysis['spending_over_time'] = self._analyze_spending_over_time(df)
            analysis['peak_spending_periods'] = self._identify_peak_periods(df)
            
        # Behavioral patterns
        analysis['spending_style'] = self._identify_spending_style(df)
        analysis['financial_risk_profile'] = self._analyze_risk_profile(df)
        
        return analysis

    def _categorize_spending(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Categorize spending patterns
        """
        categories = {}
        
        if 'category' in df.columns:
            category_counts = df['category'].value_counts()
            categories = category_counts.to_dict()
        
        return categories

    def _analyze_spending_over_time(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze spending over time
        """
        if 'date' in df.columns and 'amount' in df.columns:
            df['month'] = df['date'].dt.to_period('M')
            monthly_spending = df.groupby('month')['amount'].sum()
            return monthly_spending.to_dict()
        
        return {}

    def _identify_peak_periods(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Identify peak spending periods
        """
        peak_periods = {}
        
        if 'date' in df.columns and 'amount' in df.columns:
            df['day_of_week'] = df['date'].dt.day_name()
            df['hour'] = df['date'].dt.hour
            
            # Peak days
            peak_days = df['day_of_week'].value_counts()
            peak_periods['peak_days'] = peak_days.to_dict()
            
            # Peak hours
            peak_hours = df['hour'].value_counts()
            peak_periods['peak_hours'] = peak_hours.to_dict()
            
        return peak_periods

    def _identify_spending_style(self, df: pd.DataFrame) -> str:
        """
        Identify spending style
        """
        if 'amount' in df.columns:
            avg = df['amount'].mean()
            std = df['amount'].std()
            
            # Simple categorization
            if std / avg < 0.3:
                return 'consistent'
            elif std / avg < 0.7:
                return 'moderate'
            else:
                return 'variable'
        
        return 'unknown'

    def _analyze_risk_profile(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze financial risk profile
        """
        risk_profile = {
            'risk_tolerance': 'medium',  # Placeholder
            'investment_style': 'balanced',  # Placeholder
            'savings_behavior': 'moderate'  # Placeholder
        }
        
        return risk_profile

    def _extract_transaction_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from transaction file
        """
        try:
            stat = os.stat(file_path)
            
            metadata = {
                'filename': os.path.basename(file_path),
                'size': stat.st_size,
                'timestamp': datetime.fromtimestamp(stat.st_mtime),
                'format': 'transaction'
            }
            return metadata
        except Exception as e:
            print(f"Error extracting metadata for {file_path}: {str(e)}")
            return {}

    def create_financial_profile(self, transaction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a financial profile from transaction data
        """
        profile = {
            'spending_patterns': self._aggregate_spending_patterns(transaction_data),
            'decision_logic': self._aggregate_decision_logic(transaction_data),
            'financial_traits': self._aggregate_financial_traits(transaction_data),
            'timestamp': datetime.now()
        }
        
        return profile

    def _aggregate_spending_patterns(self, transaction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate spending patterns
        """
        patterns = {}
        
        # Simple aggregation - in practice, you'd use more sophisticated analysis
        total_spent = 0
        transaction_count = 0
        
        for data in transaction_data:
            if 'analysis' in data and 'total_spent' in data['analysis']:
                total_spent += data['analysis']['total_spent']
                transaction_count += data['analysis']['transaction_count']
                
        patterns['total_spent'] = total_spent
        patterns['average_transaction'] = total_spent / transaction_count if transaction_count > 0 else 0
        
        return patterns

    def _aggregate_decision_logic(self, transaction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate decision logic
        """
        logic = {}
        
        # Placeholder for more sophisticated logic analysis
        
        return logic

    def _aggregate_financial_traits(self, transaction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate financial traits
        """
        traits = {}
        
        # Placeholder for financial traits
        
        return traits


# Example usage
if __name__ == "__main__":
    analyzer = TransactionAnalyzer()
    data = analyzer.analyze_transactions("./data/behavioral")
    print(f"Analyzed {len(data)} transaction data items")
    
    if data:
        profile = analyzer.create_financial_profile(data)
        print(f"Created financial profile")