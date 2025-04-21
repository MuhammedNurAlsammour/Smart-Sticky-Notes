#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File Utilities - Dosya İşlemleri
Dosya işlemleri ve loglama için yardımcı fonksiyonlar
"""

import logging
import os
from pathlib import Path

def setup_logging(config):
    """
    Loglama sistemini yapılandır
    
    Args:
        config (dict): Uygulama yapılandırması
    """
    try:
        # Log dizinini oluştur
        log_dir = Path(config.get('logging', {}).get('log_dir', 'logs'))
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Log dosyası yolu
        log_file = log_dir / 'smart_sticky_notes.log'
        
        # Loglama formatını ayarla
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        print("Loglama sistemi başarıyla yapılandırıldı")
        
    except Exception as e:
        print(f"Loglama yapılandırma hatası: {str(e)}")
        raise
