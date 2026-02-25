"""
Communication Harvester

Harvests personal communication data from emails, SMS, chat logs, social media, and voicemails.
"""

import os
import re
from typing import List, Dict, Any
from datetime import datetime
import email
import json


class CommunicationHarvester:
    def __init__(self):
        self.data_sources = {
            'email': self._harvest_email,
            'sms': self._harvest_sms,
            'chat': self._harvest_chat,
            'social_media': self._harvest_social_media,
            'voicemail': self._harvest_voicemail
        }

    def harvest(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Harvest communication data from various sources
        """
        all_data = []
        
        for source_type, harvest_func in self.data_sources.items():
            try:
                source_data = harvest_func(data_path)
                all_data.extend(source_data)
                print(f"Harvested {len(source_data)} records from {source_type}")
            except Exception as e:
                print(f"Error harvesting {source_type}: {str(e)}")
                
        return all_data

    def _harvest_email(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Harvest email data from .eml files
        """
        emails = []
        
        for root, dirs, files in os.walk(data_path):
            for file in files:
                if file.endswith('.eml'):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            msg = email.message_from_file(f)
                            
                            email_data = {
                                'type': 'email',
                                'sender': msg.get('From', ''),
                                'recipient': msg.get('To', ''),
                                'subject': msg.get('Subject', ''),
                                'date': msg.get('Date', ''),
                                'body': self._extract_email_body(msg),
                                'timestamp': self._parse_date(msg.get('Date', ''))
                            }
                            emails.append(email_data)
                    except Exception as e:
                        print(f"Error parsing email {file}: {str(e)}")
                        
        return emails

    def _extract_email_body(self, msg) -> str:
        """
        Extract body text from email message
        """
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
        return body

    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse email date string to datetime object
        """
        try:
            return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        except:
            try:
                return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S")
            except:
                return datetime.now()

    def _harvest_sms(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Harvest SMS data from various formats
        """
        sms_data = []
        
        # Placeholder for SMS parsing logic
        # This would typically parse .csv, .json, or database exports
        
        return sms_data

    def _harvest_chat(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Harvest chat logs from various platforms
        """
        chat_data = []
        
        # Placeholder for chat log parsing logic
        # This would parse WhatsApp, Telegram, Slack, etc. logs
        
        return chat_data

    def _harvest_social_media(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Harvest social media data
        """
        social_data = []
        
        # Placeholder for social media parsing logic
        # This would parse Facebook, Twitter, Instagram, LinkedIn data exports
        
        return social_data

    def _harvest_voicemail(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Harvest voicemail data
        """
        voicemail_data = []
        
        # Placeholder for voicemail parsing logic
        # This would parse audio files and transcribe them
        
        return voicemail_data


# Example usage
if __name__ == "__main__":
    harvester = CommunicationHarvester()
    data = harvester.harvest("./data/personal")
    print(f"Harvested {len(data)} communication records")