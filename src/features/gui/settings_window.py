#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ayarlar Penceresi - Tema ve Diğer Ayarlar
Kullanıcı ayarları için arayüz
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                           QComboBox, QPushButton, QColorDialog, QGroupBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette

class SettingsWindow(QDialog):
    """Ayarlar penceresi"""
    
    def __init__(self, parent=None, theme_settings=None):
        super().__init__(parent)
        self.theme_settings = theme_settings
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.init_ui()
        self.center_window()
        
    def center_window(self):
        """Pencereyi ekranın ortasına yerleştir"""
        screen = self.screen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)
        
    def init_ui(self):
        """Arayüzü başlat"""
        self.setWindowTitle("Ayarlar")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        # Pencere stilini ayarla
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid gray;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QPushButton {
                padding: 5px 15px;
                border-radius: 3px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Tema ayarları grubu
        theme_group = QGroupBox("Tema Ayarları")
        theme_layout = QVBoxLayout()
        
        # Tema seçimi
        theme_label = QLabel("Tema:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Koyu Tema",
            "Mavi Tema",
            "Yeşil Tema",
            "Mor Tema",
            "Kırmızı Tema",
            "Turuncu Tema"
        ])
        
        # Mevcut temayı seç
        current_theme = self.theme_settings.get_current_theme()
        theme_names = {
            'dark': "Koyu Tema",
            'blue': "Mavi Tema",
            'green': "Yeşil Tema",
            'purple': "Mor Tema",
            'red': "Kırmızı Tema",
            'orange': "Turuncu Tema"
        }
        self.theme_combo.setCurrentText(theme_names[current_theme])
        
        # Özel renk ayarları
        colors_group = QGroupBox("Özel Renkler")
        colors_layout = QVBoxLayout()
        
        # Arka plan rengi
        bg_layout = QHBoxLayout()
        bg_label = QLabel("Arka Plan:")
        self.bg_button = QPushButton()
        self.bg_button.setFixedSize(50, 25)
        self.bg_button.clicked.connect(lambda: self.choose_color('background'))
        bg_layout.addWidget(bg_label)
        bg_layout.addWidget(self.bg_button)
        colors_layout.addLayout(bg_layout)
        
        # Metin rengi
        text_layout = QHBoxLayout()
        text_label = QLabel("Metin:")
        self.text_button = QPushButton()
        self.text_button.setFixedSize(50, 25)
        self.text_button.clicked.connect(lambda: self.choose_color('text'))
        text_layout.addWidget(text_label)
        text_layout.addWidget(self.text_button)
        colors_layout.addLayout(text_layout)
        
        # Vurgu rengi
        accent_layout = QHBoxLayout()
        accent_label = QLabel("Vurgu:")
        self.accent_button = QPushButton()
        self.accent_button.setFixedSize(50, 25)
        self.accent_button.clicked.connect(lambda: self.choose_color('highlight'))
        accent_layout.addWidget(accent_label)
        accent_layout.addWidget(self.accent_button)
        colors_layout.addLayout(accent_layout)
        
        colors_group.setLayout(colors_layout)
        
        # Yeni not ayarları grubu
        notes_group = QGroupBox("Not Ayarları")
        notes_layout = QVBoxLayout()
        
        # Yeni not görünümü seçimi
        view_label = QLabel("Yeni Not Görünümü:")
        self.view_combo = QComboBox()
        self.view_combo.addItems([
            "Sekme Olarak",
            "Ayrı Pencere Olarak"
        ])
        
        # Mevcut ayarı seç
        current_view = self.theme_settings.get_config().get('new_note_view', 'tab')
        self.view_combo.setCurrentText("Ayrı Pencere Olarak" if current_view == 'window' else "Sekme Olarak")
        
        notes_layout.addWidget(view_label)
        notes_layout.addWidget(self.view_combo)
        notes_group.setLayout(notes_layout)
        
        # Butonlar
        button_layout = QHBoxLayout()
        save_button = QPushButton("Kaydet")
        cancel_button = QPushButton("İptal")
        
        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        # Layout'ları ekle
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addWidget(colors_group)
        theme_group.setLayout(theme_layout)
        
        layout.addWidget(theme_group)
        layout.addWidget(notes_group)
        layout.addLayout(button_layout)
        
        # Renk butonlarını güncelle
        self.update_color_buttons()
        
    def update_color_buttons(self):
        """Renk butonlarını güncelle"""
        colors = self.theme_settings.get_theme_colors()
        
        self.bg_button.setStyleSheet(f"background-color: {colors['background']};")
        self.text_button.setStyleSheet(f"background-color: {colors['text']};")
        self.accent_button.setStyleSheet(f"background-color: {colors['highlight']};")
        
    def choose_color(self, color_type):
        """Renk seçici aç"""
        colors = self.theme_settings.get_theme_colors()
        current_color = QColor(colors[color_type])
        
        color = QColorDialog.getColor(current_color, self, f"{color_type.capitalize()} Rengi Seç")
        if color.isValid():
            if color_type == 'background':
                self.bg_button.setStyleSheet(f"background-color: {color.name()};")
            elif color_type == 'text':
                self.text_button.setStyleSheet(f"background-color: {color.name()};")
            elif color_type == 'highlight':
                self.accent_button.setStyleSheet(f"background-color: {color.name()};")
    
    def save_settings(self):
        """Ayarları kaydet"""
        # Tema seçimini kaydet
        theme_names = {
            "Koyu Tema": 'dark',
            "Mavi Tema": 'blue',
            "Yeşil Tema": 'green',
            "Mor Tema": 'purple',
            "Kırmızı Tema": 'red',
            "Turuncu Tema": 'orange'
        }
        
        selected_theme = theme_names[self.theme_combo.currentText()]
        self.theme_settings.apply_theme(selected_theme)
        
        # Yeni not görünümü ayarını kaydet
        view_type = 'window' if self.view_combo.currentText() == "Ayrı Pencere Olarak" else 'tab'
        self.theme_settings.get_config()['new_note_view'] = view_type
        
        self.accept() 