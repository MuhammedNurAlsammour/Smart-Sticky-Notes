#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Notes Storage - Not Depolama
Notları kaydetme ve yükleme işlemleri
"""

import os
import json
from pathlib import Path
import logging
import time

class NotesStorage:
    """Not depolama yöneticisi"""
    
    def __init__(self, config):
        """Yapılandırma ile başlat"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.notes_dir = Path(config.get('storage', {}).get('notes_dir', 'notes'))
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        
    def save_note(self, note_id, content):
        """
        Notu kaydet
        
        Args:
            note_id (str): Not kimliği
            content (str): Not içeriği
        """
        try:
            note_file = self.notes_dir / f"{note_id}.json"
            note_data = {
                'id': note_id,
                'content': content,
                'timestamp': time.time()
            }
            
            with open(note_file, 'w', encoding='utf-8') as f:
                json.dump(note_data, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"Not kaydedildi: {note_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Not kaydetme hatası: {str(e)}")
            return False
            
    def load_note(self, note_id):
        """
        Notu yükle
        
        Args:
            note_id (str): Not kimliği
            
        Returns:
            dict: Not verisi veya None
        """
        try:
            note_file = self.notes_dir / f"{note_id}.json"
            if note_file.exists():
                with open(note_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
            
        except Exception as e:
            self.logger.error(f"Not yükleme hatası: {str(e)}")
            return None
            
    def list_notes(self):
        """
        Tüm notları listele
        
        Returns:
            list: Not listesi
        """
        try:
            notes = []
            for note_file in self.notes_dir.glob('*.json'):
                with open(note_file, 'r', encoding='utf-8') as f:
                    notes.append(json.load(f))
            return sorted(notes, key=lambda x: x['timestamp'], reverse=True)
            
        except Exception as e:
            self.logger.error(f"Not listeleme hatası: {str(e)}")
            return []
            
    def delete_note(self, note_id):
        """
        Notu sil
        
        Args:
            note_id (str): Not kimliği
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            note_file = self.notes_dir / f"{note_id}.json"
            if note_file.exists():
                note_file.unlink()
                self.logger.info(f"Not silindi: {note_id}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Not silme hatası: {str(e)}")
            return False 