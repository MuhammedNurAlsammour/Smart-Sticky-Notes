#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Smart Sticky Notes - Ana Uygulama
Ana uygulama giriş noktası ve başlatma kodu
"""

import sys
import os
import time
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication

# Proje kök dizinini Python yoluna ekle
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Uygulama modüllerini içe aktar
from common.utils.file_utils import setup_logging
from core.config.settings import load_config
from features.notifications.notification_manager import NotificationManager
from features.file_sync.file_sync_manager import FileSyncManager
from features.gui.sticky_notes_gui import StickyNotesGUI

class SmartStickyNotes:
    """Ana uygulama sınıfı"""
    
    def __init__(self):
        """Uygulama başlatıcı"""
        self.config = None
        self.notification_manager = None
        self.file_sync_manager = None
        self.logger = None
        self.gui = None
        self.app = None
        
    def initialize(self):
        """Uygulamayı başlat"""
        try:
            # Yapılandırmayı yükle
            self.config = load_config()
            
            # Loglama sistemini başlat
            setup_logging(self.config)
            self.logger = logging.getLogger(__name__)
            
            # Bildirim yöneticisini başlat
            self.notification_manager = NotificationManager(self.config)
            self.notification_manager.start()
            
            # Dosya senkronizasyon yöneticisini başlat
            self.file_sync_manager = FileSyncManager(self.config)
            self.file_sync_manager.start()
            
            # GUI'yi başlat
            self.app = QApplication(sys.argv)
            self.gui = StickyNotesGUI(
                self.config,
                self.notification_manager,
                self.file_sync_manager
            )
            self.gui.show()
            
            self.logger.info("Uygulama başarıyla başlatıldı")
            print("Uygulama başarıyla başlatıldı!")
            
        except Exception as e:
            self.logger.error(f"Başlatma hatası: {str(e)}")
            print(f"Başlatma hatası: {str(e)}")
            sys.exit(1)
    
    def run(self):
        """Ana uygulama döngüsü"""
        try:
            sync_interval = self.config['file_sync']['sync_interval']
            last_sync = time.time()
            
            # Qt event loop'u başlat
            sys.exit(self.app.exec())
            
        except Exception as e:
            self.logger.error(f"Çalışma hatası: {str(e)}")
            print(f"Çalışma hatası: {str(e)}")
            self.shutdown()
    
    def shutdown(self):
        """Uygulamayı düzgün bir şekilde kapat"""
        try:
            if self.file_sync_manager:
                self.file_sync_manager.stop()
            if self.notification_manager:
                self.notification_manager.stop()
            self.logger.info("Uygulama başarıyla kapatıldı")
            print("Uygulama başarıyla kapatıldı!")
        except Exception as e:
            self.logger.error(f"Kapatma hatası: {str(e)}")
            print(f"Kapatma hatası: {str(e)}")

def main():
    """Ana fonksiyon"""
    app = SmartStickyNotes()
    app.initialize()
    app.run()

if __name__ == "__main__":
    main()