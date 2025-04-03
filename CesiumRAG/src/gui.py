#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import markdown
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QPushButton, QLabel, 
                            QSplitter, QFrame, QStyleFactory, QProgressBar, QTextBrowser)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

# 导入flow模块
import flow

# 处理线程
class ProcessingThread(QThread):
    result_ready = pyqtSignal(str)
    status_update = pyqtSignal(str)
    progress_update = pyqtSignal(int)
    
    def __init__(self, query):
        super().__init__()
        self.query = query
        
    def run(self):
        try:
            # 使用flow.py中的process_query函数处理查询
            # 传入状态和进度回调函数
            result = flow.process_query(
                self.query, 
                status_callback=self.status_update.emit,
                progress_callback=self.progress_update.emit
            )
            
            # 发送结果信号
            self.result_ready.emit(result)
        except Exception as e:
            self.result_ready.emit(f"错误: {str(e)}")

class LoadingAnimation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.dots = 0
        self.active = False
        self.base_text = "处理中"
        self.setVisible(False)
        
        self.label = QLabel(self.base_text)
        self.label.setStyleSheet("color: #42a5f5; font-weight: bold;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                text-align: center;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #42a5f5;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
    
    def start(self):
        self.active = True
        self.setVisible(True)
        self.timer.start(500)
    
    def stop(self):
        self.active = False
        self.timer.stop()
        self.setVisible(False)
    
    def update_animation(self):
        if not self.active:
            return
        
        self.dots = (self.dots + 1) % 4
        self.label.setText(f"{self.base_text}{'.' * self.dots}")
    
    def set_progress(self, value):
        self.progress_bar.setValue(value)

class CesiumRagGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_style()
        self.initUI()
        
    def set_style(self):
        # 设置应用样式
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        
        # 自定义调色板
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(43, 43, 43))  # 稍微深一点的背景
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # 纯白色文字
        palette.setColor(QPalette.Base, QColor(18, 18, 18))  # 更深的输入框背景
        palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, QColor(255, 255, 255))  # 纯白色文字
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))  # 纯白色文字
        palette.setColor(QPalette.BrightText, QColor(255, 50, 50))  # 更鲜艳的强调色
        palette.setColor(QPalette.Link, QColor(66, 133, 244))  # 更鲜艳的链接颜色
        palette.setColor(QPalette.Highlight, QColor(66, 133, 244))  # 更鲜艳的高亮颜色
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))  # 纯白色高亮文字
        QApplication.setPalette(palette)
        
    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('Cesium RAG助手')
        self.setMinimumSize(800, 600)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标题标签
        title_label = QLabel('Cesium API 查询助手')
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # 创建分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        # 创建输入区域
        input_label = QLabel('请输入您的Cesium相关问题:')
        main_layout.addWidget(input_label)
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText('在这里输入您的问题...')
        self.input_text.setFixedHeight(100)
        self.input_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 10px;
                selection-background-color: #3e4451;
            }
            QTextEdit::placeholder {
                color: #aaaaaa;
            }
        """)
        main_layout.addWidget(self.input_text)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 添加提交按钮
        self.submit_button = QPushButton('提交问题')
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.submit_button.clicked.connect(self.process_query)
        button_layout.addWidget(self.submit_button)
        
        # 添加清除按钮
        self.clear_button = QPushButton('清除')
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            QPushButton:pressed {
                background-color: #d32f2f;
            }
        """)
        self.clear_button.clicked.connect(self.clear_input)
        button_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(button_layout)
        
        # 创建加载动画
        self.loading_animation = LoadingAnimation()
        main_layout.addWidget(self.loading_animation)
        
        # 创建分隔线
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line2)
        
        # 创建输出区域
        output_label = QLabel('系统回答:')
        main_layout.addWidget(output_label)
        
        # 使用QTextBrowser代替QTextEdit以支持HTML渲染
        self.output_text = QTextBrowser()
        self.output_text.setOpenExternalLinks(True)
        self.output_text.setPlaceholderText('回答将显示在这里...')
        self.output_text.setStyleSheet("""
            QTextBrowser {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 10px;
                selection-background-color: #3e4451;
            }
            QTextBrowser a {
                color: #61afef;
            }
            QTextBrowser code {
                background-color: #2d2d2d;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            QTextBrowser pre {
                background-color: #2d2d2d;
                padding: 10px;
                border-radius: 5px;
                overflow: auto;
            }
        """)
        main_layout.addWidget(self.output_text)
        
        # 添加状态指示
        self.status_label = QLabel('就绪')
        self.status_label.setStyleSheet("font-style: italic; color: #999999;")
        main_layout.addWidget(self.status_label)
        
        # 显示窗口
        self.show()
    
    def process_query(self):
        query = self.input_text.toPlainText().strip()
        if not query:
            self.status_label.setText('请输入问题')
            return
        
        # 更新状态
        self.status_label.setText('处理中...')
        self.submit_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.output_text.clear()
        
        # 显示加载动画
        self.loading_animation.start()
        
        # 创建处理线程
        self.processing_thread = ProcessingThread(query)
        self.processing_thread.result_ready.connect(self.update_result)
        self.processing_thread.status_update.connect(self.update_status)
        self.processing_thread.progress_update.connect(self.update_progress)
        self.processing_thread.start()
    
    def update_result(self, result):
        # 停止加载动画
        self.loading_animation.stop()
        
        try:
            # 将Markdown转换为HTML
            html_content = markdown.markdown(
                result,
                extensions=[
                    'markdown.extensions.tables',
                    'markdown.extensions.fenced_code',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.nl2br',
                    'markdown.extensions.sane_lists'
                ]
            )
            
            # 添加基本CSS样式
            css_style = """
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; }
                h1, h2, h3, h4, h5, h6 { color: #ffffff; margin-top: 24px; margin-bottom: 16px; font-weight: 600; }
                h1 { font-size: 2em; border-bottom: 1px solid #3e4451; padding-bottom: 0.3em; }
                h2 { font-size: 1.5em; border-bottom: 1px solid #3e4451; padding-bottom: 0.3em; }
                h3 { font-size: 1.25em; }
                h4 { font-size: 1em; }
                p, blockquote, ul, ol, dl, table, pre { margin: 0 0 16px; }
                a { color: #61afef; text-decoration: none; }
                a:hover { text-decoration: underline; }
                code { background-color: #2d2d2d; padding: 0.2em 0.4em; border-radius: 3px; font-family: 'Consolas', 'Courier New', monospace; }
                pre { background-color: #2d2d2d; padding: 16px; border-radius: 5px; overflow: auto; }
                pre code { background-color: transparent; padding: 0; }
                blockquote { padding: 0 1em; color: #d8d8d8; border-left: 0.25em solid #4b5363; }
                table { border-spacing: 0; border-collapse: collapse; width: 100%; overflow: auto; }
                table th, table td { padding: 6px 13px; border: 1px solid #4b5363; }
                table tr { background-color: #1e1e1e; }
                table tr:nth-child(2n) { background-color: #262626; }
                img { max-width: 100%; }
                ul, ol { padding-left: 2em; }
            </style>
            """
            
            # 设置HTML内容
            full_html = f"{css_style}<div>{html_content}</div>"
            self.output_text.setHtml(full_html)
        except Exception as e:
            # 如果转换失败，显示原始文本
            self.output_text.setPlainText(f"{result}\n\n(Markdown渲染失败: {str(e)})")
        
        self.status_label.setText('就绪')
        self.submit_button.setEnabled(True)
        self.clear_button.setEnabled(True)
    
    def update_status(self, status):
        self.status_label.setText(status)
        self.loading_animation.base_text = status
    
    def update_progress(self, value):
        self.loading_animation.set_progress(value)
    
    def clear_input(self):
        self.input_text.clear()
        self.input_text.setFocus()

def main():
    app = QApplication(sys.argv)
    ex = CesiumRagGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 