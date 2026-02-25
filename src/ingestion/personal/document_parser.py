"""
Document Parser

Parses journals, letters, medical records, legal filings, and other documents.
"""

import os
import re
from typing import List, Dict, Any
from datetime import datetime
import docx
import pdfplumber
import json


class DocumentParser:
    def __init__(self):
        self.document_types = {
            '.txt': self._parse_text,
            '.md': self._parse_markdown,
            '.docx': self._parse_docx,
            '.pdf': self._parse_pdf,
            '.csv': self._parse_csv,
            '.json': self._parse_json
        }

    def parse_documents(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Parse all documents in the data path
        """
        documents = []
        
        for root, dirs, files in os.walk(data_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Get file extension
                _, ext = os.path.splitext(file)
                
                if ext.lower() in self.document_types:
                    try:
                        doc_data = self._parse_document(file_path, ext.lower())
                        if doc_data:
                            documents.append(doc_data)
                    except Exception as e:
                        print(f"Error parsing document {file_path}: {str(e)}")
                        
        return documents

    def _parse_document(self, file_path: str, ext: str) -> Dict[str, Any]:
        """
        Parse a single document
        """
        try:
            # Get parser function
            parser = self.document_types[ext]
            
            # Parse document
            content = parser(file_path)
            
            # Extract metadata
            metadata = self._extract_document_metadata(file_path)
            
            return {
                'type': 'document',
                'path': file_path,
                'content': content,
                'metadata': metadata,
                'timestamp': metadata.get('timestamp', datetime.now())
            }
        except Exception as e:
            print(f"Error parsing document {file_path}: {str(e)}")
            return None

    def _parse_text(self, file_path: str) -> str:
        """
        Parse plain text file
        """
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    def _parse_markdown(self, file_path: str) -> str:
        """
        Parse markdown file
        """
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    def _parse_docx(self, file_path: str) -> str:
        """
        Parse Word document
        """
        try:
            doc = docx.Document(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            print(f"Error parsing DOCX {file_path}: {str(e)}")
            return ""

    def _parse_pdf(self, file_path: str) -> str:
        """
        Parse PDF document
        """
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"Error parsing PDF {file_path}: {str(e)}")
            return ""

    def _parse_csv(self, file_path: str) -> str:
        """
        Parse CSV file
        """
        try:
            import csv
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                rows = list(reader)
                return '\n'.join([','.join(row) for row in rows])
        except Exception as e:
            print(f"Error parsing CSV {file_path}: {str(e)}")
            return ""

    def _parse_json(self, file_path: str) -> str:
        """
        Parse JSON file
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
                return json.dumps(data, indent=2)
        except Exception as e:
            print(f"Error parsing JSON {file_path}: {str(e)}")
            return ""

    def _extract_document_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from document file
        """
        try:
            stat = os.stat(file_path)
            
            metadata = {
                'filename': os.path.basename(file_path),
                'size': stat.st_size,
                'timestamp': datetime.fromtimestamp(stat.st_mtime),
                'format': 'document'
            }
            return metadata
        except Exception as e:
            print(f"Error extracting metadata for {file_path}: {str(e)}")
            return {}

    def extract_key_phrases(self, content: str, num_phrases: int = 10) -> List[str]:
        """
        Extract key phrases from document content
        """
        # Simple approach - in practice, you'd use NLP libraries like spaCy or NLTK
        words = re.findall(r'\w+', content.lower())
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'}
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            if word not in stop_words and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:num_phrases]]


# Example usage
if __name__ == "__main__":
    parser = DocumentParser()
    documents = parser.parse_documents("./data/personal")
    print(f"Parsed {len(documents)} documents")
    
    if documents:
        # Extract key phrases from first document
        first_doc = documents[0]
        key_phrases = parser.extract_key_phrases(first_doc['content'], 5)
        print(f"Key phrases: {key_phrases}")