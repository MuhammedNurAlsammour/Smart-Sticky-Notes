#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Settings - Yapılandırma
Uygulama yapılandırma ayarları ve yükleme fonksiyonları
"""

import os
import json
from pathlib import Path

def load_config():
    """
    Uygulama yapılandırmasını yükle
    
    Returns:
        dict: Yapılandırma ayarları
    """
    try:
        # Varsayılan yapılandırma
        default_config = {
            'logging': {
                'log_dir': 'logs',
                'level': 'INFO'
            },
            'file_sync': {
                'sync_interval': 60,  # saniye
                'watch_dirs': ['notes']
            },
            'notifications': {
                'enabled': True,
                'sound': True
            }
        }
        
        # Yapılandırma dosyası yolu
        config_path = Path('config.json')
        
        # Eğer yapılandırma dosyası varsa, oku
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # Varsayılan yapılandırmayı kullanıcı yapılandırması ile birleştir
                default_config.update(user_config)
        
        print("Yapılandırma başarıyla yüklendi")
        
        return default_config
        
    except Exception as e:
        print(f"Yapılandırma yükleme hatası: {str(e)}")
        raise
