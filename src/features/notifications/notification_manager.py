#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Notification Manager - Bildirim Yöneticisi
Bildirim işlemlerini yöneten sınıf
"""

import logging
from typing import Optional

class NotificationManager:
    """Bildirim yöneticisi sınıfı"""
    
    def __init__(self, config):
        """Yapılandırma ile başlat"""
        self.config = config
        self.is_running = False
        self.logger = logging.getLogger(__name__)
        
    def start(self):
        """Bildirim sistemini başlat"""
        self.is_running = True
        self.logger.info("Bildirim sistemi başlatıldı")
        print("Bildirim sistemi başlatıldı")
        
    def stop(self):
        """Bildirim sistemini durdur"""
        self.is_running = False
        self.logger.info("Bildirim sistemi durduruldu")
        print("Bildirim sistemi durduruldu")
        
    def send_notification(self, title: str, message: str, level: str = "info"):
        """
        Bildirim gönder
        
        Args:
            title (str): Bildirim başlığı
            message (str): Bildirim mesajı
            level (str): Bildirim seviyesi (info, warning, error)
        """
        if not self.is_running:
            return
            
        # Bildirim gönderme işlemleri burada gerçekleştirilecek
        self.logger.info(f"Bildirim gönderildi: {title} - {message}")
        print(f"Bildirim: {title} - {message}")
