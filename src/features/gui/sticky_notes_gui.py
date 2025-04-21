#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sticky Notes GUI - Yapışkan Notlar Arayüzü
Ana uygulama arayüzü
"""

import sys
import os
from pathlib import Path

# Proje kök dizinini Python yoluna ekle
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

import uuid
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QPushButton, QTextEdit, QSystemTrayIcon, QMenu,
                           QTabWidget, QToolBar, QFileDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QShortcut, QFont

from features.storage.notes_storage import NotesStorage
from features.gui.theme_settings import ThemeSettings
from features.gui.settings_window import SettingsWindow

class NoteWidget(QWidget):
    """Tek bir not widget'ı"""
    
    def __init__(self, parent=None, note_id=None):
        super().__init__(parent)
        self.note_id = note_id or str(uuid.uuid4())
        self.init_ui()
        
    def init_ui(self):
        """Arayüzü başlat"""
        layout = QVBoxLayout(self)
        
        # Araç çubuğu
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        
        # Kalın yazı butonu
        self.bold_action = QAction("B", self)
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(self.toggle_bold)
        self.toolbar.addAction(self.bold_action)
        
        # Altı çizili butonu
        self.underline_action = QAction("U", self)
        self.underline_action.setCheckable(True)
        self.underline_action.triggered.connect(self.toggle_underline)
        self.toolbar.addAction(self.underline_action)
        
        # Üstü çizili butonu
        self.strike_action = QAction("S", self)
        self.strike_action.setCheckable(True)
        self.strike_action.triggered.connect(self.toggle_strike)
        self.toolbar.addAction(self.strike_action)
        
        # Liste butonu
        self.list_action = QAction("•", self)
        self.list_action.setCheckable(True)
        self.list_action.triggered.connect(self.toggle_list)
        self.toolbar.addAction(self.list_action)
        
        # Resim ekle butonu
        self.image_action = QAction("🖼️", self)
        self.image_action.triggered.connect(self.insert_image)
        self.toolbar.addAction(self.image_action)
        
        layout.addWidget(self.toolbar)
        
        # Not alanı
        self.note_text = QTextEdit()
        self.note_text.setPlaceholderText("Notunuzu buraya yazın...")
        layout.addWidget(self.note_text)
        
        # Kaydet butonu
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(self.save_note)
        layout.addWidget(save_button)
        
    def toggle_bold(self):
        """Kalın yazı durumunu değiştir"""
        cursor = self.note_text.textCursor()
        if cursor.hasSelection():
            # Seçili metni kalın yap
            format = cursor.charFormat()
            format.setFontWeight(QFont.Weight.Bold if not format.fontWeight() == QFont.Weight.Bold else QFont.Weight.Normal)
            cursor.mergeCharFormat(format)
            self.note_text.setCurrentCharFormat(format)
        else:
            # Kalın yazı modunu değiştir
            format = self.note_text.currentCharFormat()
            format.setFontWeight(QFont.Weight.Bold if not format.fontWeight() == QFont.Weight.Bold else QFont.Weight.Normal)
            self.note_text.setCurrentCharFormat(format)
        
    def toggle_underline(self):
        """Altı çizili yazı durumunu değiştir"""
        cursor = self.note_text.textCursor()
        if cursor.hasSelection():
            # Seçili metni altı çizili yap
            format = cursor.charFormat()
            format.setFontUnderline(not format.fontUnderline())
            cursor.mergeCharFormat(format)
            self.note_text.setCurrentCharFormat(format)
        else:
            # Altı çizili yazı modunu değiştir
            format = self.note_text.currentCharFormat()
            format.setFontUnderline(not format.fontUnderline())
            self.note_text.setCurrentCharFormat(format)
        
    def toggle_strike(self):
        """Üstü çizili yazı durumunu değiştir"""
        cursor = self.note_text.textCursor()
        if cursor.hasSelection():
            # Seçili metni üstü çizili yap
            format = cursor.charFormat()
            format.setFontStrikeOut(not format.fontStrikeOut())
            cursor.mergeCharFormat(format)
            self.note_text.setCurrentCharFormat(format)
        else:
            # Üstü çizili yazı modunu değiştir
            format = self.note_text.currentCharFormat()
            format.setFontStrikeOut(not format.fontStrikeOut())
            self.note_text.setCurrentCharFormat(format)
        
    def toggle_list(self):
        """Liste durumunu değiştir"""
        cursor = self.note_text.textCursor()
        block_format = cursor.blockFormat()
        
        # Mevcut girintiyi kontrol et
        current_indent = block_format.indent()
        
        if current_indent > 0:
            # Liste stilini kaldır
            block_format.setIndent(0)
            block_format.setLeftMargin(0)
        else:
            # Liste stilini ekle
            block_format.setIndent(1)
            block_format.setLeftMargin(20)  # Sol kenar boşluğu
            
            # Nokta ekle
            cursor.insertText("• ")
        
        cursor.setBlockFormat(block_format)
        self.note_text.setTextCursor(cursor)
        
        # Enter tuşuna basıldığında otomatik nokta ekle
        self.note_text.keyPressEvent = self.handle_key_press

    def handle_key_press(self, event):
        """Enter tuşuna basıldığında otomatik nokta ekle"""
        if event.key() == Qt.Key.Key_Return:
            cursor = self.note_text.textCursor()
            block_format = cursor.blockFormat()
            
            if block_format.indent() > 0:
                # Yeni satıra nokta ekle
                cursor.insertText("• ")
                return
            
        # Normal tuş işleme
        QTextEdit.keyPressEvent(self.note_text, event)
        
    def save_note(self):
        """Notu kaydet"""
        note_text = self.note_text.toHtml()  # HTML formatında kaydet
        if note_text:
            if hasattr(self.parent(), 'notes_storage'):
                if self.parent().notes_storage.save_note(self.note_id, note_text):
                    self.parent().notification_manager.send_notification(
                        "Not Kaydedildi",
                        "Notunuz başarıyla kaydedildi",
                        "info"
                    )

    def insert_image(self):
        """Resim ekle"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Resim Seç",
            "",
            "Resim Dosyaları (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        
        if file_name:
            # Resmi HTML olarak ekle
            cursor = self.note_text.textCursor()
            cursor.insertHtml(f'<img src="{file_name}" width="300">')

class NoteWindow(QMainWindow):
    """Not penceresi"""
    
    def __init__(self, parent=None, note_widget=None):
        super().__init__(parent)
        self.note_widget = note_widget
        self.setCentralWidget(note_widget)
        
    def closeEvent(self, event):
        """Pencere kapatıldığında"""
        try:
            # Notu kaydet
            if self.note_widget:
                self.note_widget.save_note()
            event.accept()
        except Exception as e:
            print(f"Pencere kapatılırken hata: {str(e)}")
            event.accept()

class StickyNotesGUI(QMainWindow):
    """Ana uygulama penceresi"""
    
    def __init__(self, config, notification_manager, file_sync_manager):
        super().__init__()
        self.config = config
        self.notification_manager = notification_manager
        self.file_sync_manager = file_sync_manager
        self.notes = []
        
        # Not depolama sistemini başlat
        self.notes_storage = NotesStorage(config)
        
        # Tema ayarlarını başlat
        self.theme_settings = ThemeSettings(QApplication.instance())
        
        # Varsayılan temayı uygula
        default_theme = config.get('theme', 'dark')
        self.theme_settings.apply_theme(default_theme)
        
        self.init_ui()
        self.init_tray_icon()
        self.init_shortcuts()
        self.load_saved_notes()
        
    def load_saved_notes(self):
        """Kayıtlı notları yükle"""
        saved_notes = self.notes_storage.list_notes()
        for note_data in saved_notes:
            note_widget = NoteWidget(self, note_data['id'])
            note_widget.note_text.setText(note_data['content'])
            self.notes.append(note_widget)
            self.tab_widget.addTab(note_widget, f"Not {len(self.notes)}")
        
        if not saved_notes:
            self.create_new_note()
            
    def init_ui(self):
        """Arayüzü başlat"""
        self.setWindowTitle('Smart Sticky Notes')
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Sekmeler
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tab_widget)
        
        # Araç çubuğu
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        
        # Kalın yazı butonu
        self.bold_action = QAction("B", self)
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(self.toggle_bold)
        self.toolbar.addAction(self.bold_action)
        
        # Altı çizili butonu
        self.underline_action = QAction("U", self)
        self.underline_action.setCheckable(True)
        self.underline_action.triggered.connect(self.toggle_underline)
        self.toolbar.addAction(self.underline_action)
        
        # Üstü çizili butonu
        self.strike_action = QAction("S", self)
        self.strike_action.setCheckable(True)
        self.strike_action.triggered.connect(self.toggle_strike)
        self.toolbar.addAction(self.strike_action)
        
        # Liste butonu
        self.list_action = QAction("•", self)
        self.list_action.setCheckable(True)
        self.list_action.triggered.connect(self.toggle_list)
        self.toolbar.addAction(self.list_action)
        
        # Ayarlar butonu
        self.settings_action = QAction("⚙️", self)
        self.settings_action.triggered.connect(self.show_settings)
        self.toolbar.addAction(self.settings_action)
        
        layout.addWidget(self.toolbar)
        
        # Yeni not butonu
        new_note_button = QPushButton("Yeni Not")
        new_note_button.clicked.connect(self.create_new_note)
        layout.addWidget(new_note_button)
        
        # Pencere boyutunu ayarla
        self.resize(400, 300)
        
        # İlk notu oluştur
        if not self.notes:
            self.create_new_note()
        
    def init_shortcuts(self):
        """Klavye kısayollarını başlat"""
        # Yeni not kısayolu (Ctrl+Win+T)
        new_note_shortcut = QShortcut(QKeySequence("Ctrl+Super+T"), self)
        new_note_shortcut.activated.connect(self.create_new_note)
        
        # Alternatif kısayol (Ctrl+Alt+T)
        alt_shortcut = QShortcut(QKeySequence("Ctrl+Alt+T"), self)
        alt_shortcut.activated.connect(self.create_new_note)
        
        # Ayarlar kısayolu (Ctrl+,)
        settings_shortcut = QShortcut(QKeySequence("Ctrl+,"), self)
        settings_shortcut.activated.connect(self.show_settings)
        
        # Altı çizili kısayolu (Ctrl+U)
        underline_shortcut = QShortcut(QKeySequence("Ctrl+U"), self)
        underline_shortcut.activated.connect(self.toggle_underline)
        
        # Liste kısayolu (Ctrl+L)
        list_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        list_shortcut.activated.connect(self.toggle_list)
        
        # Üstü çizili kısayolu (Ctrl+S)
        strike_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        strike_shortcut.activated.connect(self.toggle_strike)
        
    def create_new_note(self):
        """Yeni not oluştur"""
        try:
            # Görünüm tipini kontrol et
            view_type = self.theme_settings.get_config().get('new_note_view', 'tab')
            
            if view_type == 'window':
                # NoteWidget'ı oluştur
                note_widget = NoteWidget(self)
                self.notes.append(note_widget)
                
                # Ayrı pencere olarak göster
                note_window = NoteWindow(self, note_widget)
                note_window.setWindowTitle(f"Not {len(self.notes)}")
                note_window.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
                note_window.resize(400, 300)
                note_window.show()
                
            else:
                # Sekme olarak göster
                note_widget = NoteWidget(self)
                self.notes.append(note_widget)
                
                if hasattr(self, 'tab_widget'):
                    tab_index = self.tab_widget.addTab(note_widget, f"Not {len(self.notes)}")
                    self.tab_widget.setCurrentIndex(tab_index)
                else:
                    print("Hata: tab_widget bulunamadı")
                    return False
                
            # Bildirim gönder
            if self.notification_manager:
                self.notification_manager.send_notification(
                    "Yeni Not",
                    "Yeni bir not oluşturuldu",
                    "info"
                )
                
            return True
        except Exception as e:
            print(f"Yeni not oluşturulurken hata: {str(e)}")
            return False
        
    def close_tab(self, index):
        """Sekmeyi kapat"""
        widget = self.tab_widget.widget(index)
        if widget in self.notes:
            # Notu kaydet
            widget.save_note()
            # Notu listeden kaldır
            self.notes.remove(widget)
            # Sekmeyi kaldır
            self.tab_widget.removeTab(index)
            
        # Eğer son sekme kapatıldıysa, yeni bir not oluştur
        if self.tab_widget.count() == 0:
            self.create_new_note()
            
    def init_tray_icon(self):
        """Sistem tepsisi simgesini başlat"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.ico"))
        
        # Tepsi menüsü
        tray_menu = QMenu()
        
        # Tema menüsü
        theme_menu = QMenu("Tema", self)
        
        # Tema aksiyonları
        themes = {
            'Koyu Tema': 'dark',
            'Mavi Tema': 'blue',
            'Yeşil Tema': 'green',
            'Mor Tema': 'purple',
            'Kırmızı Tema': 'red',
            'Turuncu Tema': 'orange'
        }
        
        # Her tema için aksiyon oluştur
        for theme_name, theme_id in themes.items():
            action = QAction(theme_name, self)
            action.setCheckable(True)
            action.setChecked(theme_id == self.theme_settings.get_current_theme())
            action.triggered.connect(lambda checked, t=theme_id: self.change_theme(t))
            theme_menu.addAction(action)
        
        # Ana menü
        show_action = QAction("Göster", self)
        new_note_action = QAction("Yeni Not", self)
        settings_action = QAction("Ayarlar", self)
        quit_action = QAction("Çıkış", self)
        
        show_action.triggered.connect(self.show)
        new_note_action.triggered.connect(self.create_new_note)
        settings_action.triggered.connect(self.show_settings)
        quit_action.triggered.connect(QApplication.quit)
        
        # Menüleri ekle
        tray_menu.addMenu(theme_menu)
        tray_menu.addSeparator()
        tray_menu.addAction(show_action)
        tray_menu.addAction(new_note_action)
        tray_menu.addAction(settings_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def change_theme(self, theme_name):
        """Tema değiştir"""
        if self.theme_settings.apply_theme(theme_name):
            # Tema değişikliğini kaydet
            self.config['theme'] = theme_name
            self.notes_storage.save_config(self.config)
            
            # Tüm pencereleri güncelle
            for note in self.notes:
                note.setStyleSheet(f"""
                    QWidget {{
                        background-color: {self.theme_settings.get_theme_colors()['background']};
                        color: {self.theme_settings.get_theme_colors()['text']};
                    }}
                    QPushButton {{
                        background-color: {self.theme_settings.get_theme_colors()['primary']};
                        color: {self.theme_settings.get_theme_colors()['text']};
                        border: none;
                        padding: 5px;
                    }}
                    QPushButton:hover {{
                        background-color: {self.theme_settings.get_theme_colors()['secondary']};
                    }}
                """)
            
            # Bildirim gönder
            self.notification_manager.send_notification(
                "Tema Değiştirildi",
                f"{theme_name.capitalize()} tema uygulandı",
                "info"
            )
            
    def show_settings(self):
        """Ayarlar penceresini göster"""
        settings = SettingsWindow(self, self.theme_settings)
        settings.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        settings.show()
        settings.raise_()
        settings.activateWindow()
        
    def closeEvent(self, event):
        """Pencere kapatıldığında"""
        try:
            # Tüm notları kaydet
            for note in self.notes:
                note_text = note.note_text.toHtml()
                if note_text:  # Sadece boş olmayan notları kaydet
                    self.notes_storage.save_note(note.note_id, note_text)
            
            # Dosya senkronizasyonunu başlat
            if self.file_sync_manager:
                self.file_sync_manager.sync_files()
                
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Smart Sticky Notes",
                "Uygulama arka planda çalışıyor\nالتطبيق يعمل في الخلفية",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        except Exception as e:
            self.notification_manager.send_notification(
                "Hata / خطأ",
                f"Notlar kaydedilirken hata oluştu: {str(e)}",
                "error"
            ) 

    def toggle_bold(self):
        """Kalın yazı durumunu değiştir"""
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, 'toggle_bold'):
            current_widget.toggle_bold()

    def toggle_underline(self):
        """Altı çizili yazı durumunu değiştir"""
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, 'toggle_underline'):
            current_widget.toggle_underline()

    def toggle_strike(self):
        """Üstü çizili yazı durumunu değiştir"""
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, 'toggle_strike'):
            current_widget.toggle_strike()

    def toggle_list(self):
        """Liste durumunu değiştir"""
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, 'toggle_list'):
            current_widget.toggle_list()

if __name__ == "__main__":
    # Test için basit bir yapılandırma
    config = {
        'storage': {
            'notes_dir': 'notes'
        }
    }
    
    app = QApplication(sys.argv)
    gui = StickyNotesGUI(config, None, None)
    gui.show()
    sys.exit(app.exec()) 