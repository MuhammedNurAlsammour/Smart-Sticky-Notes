#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tema Ayarları - Uygulama Temaları
Uygulama teması ve renk ayarları
"""

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

class ThemeSettings:
    """Tema ayarları sınıfı"""
    
    def __init__(self, app):
        self.app = app
        self.config = {
            'theme': 'dark',
            'new_note_view': 'tab'  # Varsayılan olarak sekme görünümü
        }
        self.themes = {
            'dark': {
                'background': '#2d2d2d',
                'text': '#ffffff',
                'highlight': '#3d3d3d'
            },
            'blue': {
                'background': '#1e3a8a',
                'text': '#ffffff',
                'highlight': '#2563eb'
            },
            'green': {
                'background': '#064e3b',
                'text': '#ffffff',
                'highlight': '#059669'
            },
            'purple': {
                'background': '#4c1d95',
                'text': '#ffffff',
                'highlight': '#7c3aed'
            },
            'red': {
                'background': '#7f1d1d',
                'text': '#ffffff',
                'highlight': '#dc2626'
            },
            'orange': {
                'background': '#7c2d12',
                'text': '#ffffff',
                'highlight': '#ea580c'
            }
        }
        
    def get_config(self):
        """Yapılandırma ayarlarını döndür"""
        return self.config
        
    def get_current_theme(self):
        """Mevcut temayı döndür"""
        return self.config['theme']
        
    def get_theme_colors(self):
        """Mevcut tema renklerini döndür"""
        return self.themes[self.config['theme']]
        
    def apply_theme(self, theme_name):
        """Tema uygula"""
        if theme_name in self.themes:
            self.config['theme'] = theme_name
            colors = self.themes[theme_name]
            
            # Uygulama stilini güncelle
            self.app.setStyleSheet(f"""
                QMainWindow, QDialog, QWidget {{
                    background-color: {colors['background']};
                    color: {colors['text']};
                }}
                QPushButton {{
                    background-color: {colors['highlight']};
                    color: {colors['text']};
                    border: none;
                    padding: 5px;
                }}
                QPushButton:hover {{
                    background-color: {colors['text']};
                    color: {colors['background']};
                }}
                QTabWidget::pane {{
                    border: 1px solid {colors['highlight']};
                }}
                QTabBar::tab {{
                    background-color: {colors['background']};
                    color: {colors['text']};
                    border: 1px solid {colors['highlight']};
                    padding: 5px;
                }}
                QTabBar::tab:selected {{
                    background-color: {colors['highlight']};
                }}
            """)
            return True
        return False 