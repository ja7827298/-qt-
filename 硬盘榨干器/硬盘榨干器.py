import sys
import os
import random
import string
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt

class DiskFillerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('hard disk filler')
        self.setGeometry(100, 100, 400, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 创建目录输入框
        self.directory_input = QLineEdit()
        self.directory_input.setPlaceholderText("Enter directory path")
        layout.addWidget(self.directory_input)

        # 创建文件大小输入框
        self.file_size_input = QLineEdit()
        self.file_size_input.setPlaceholderText("Enter the size of a single file (MB)")
        layout.addWidget(self.file_size_input)

        # 创建磁盘使用上限输入框
        self.usage_limit_input = QLineEdit()
        self.usage_limit_input.setPlaceholderText("Enter the disk usage limit (GB)")
        layout.addWidget(self.usage_limit_input)

        # 创建按钮
        self.fill_button = QPushButton('Start Filling Disk')
        self.fill_button.clicked.connect(self.fill_disk)
        layout.addWidget(self.fill_button)

        # 设置布局
        self.setLayout(layout)

    def fill_disk(self):
        directory = self.directory_input.text()
        if not os.path.isdir(directory):
            QMessageBox.warning(self, "Warning", "The specified directory does not exist!")
            return

        try:
            file_size_mb = int(self.file_size_input.text())
            usage_limit_gb = int(self.usage_limit_input.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter a valid number!")
            return

        file_size_bytes = file_size_mb * 1024 * 1024
        usage_limit_bytes = usage_limit_gb * 1024 * 1024 * 1024

        current_usage = self.get_disk_usage(directory)

        if current_usage >= usage_limit_bytes:
            QMessageBox.warning(self, "Warning", "The current disk usage has reached or exceeded the limit!")
            return

        while current_usage < usage_limit_bytes:
            filename = self.generate_random_filename()
            file_path = os.path.join(directory, filename)
            with open(file_path, 'wb') as f:
                f.write(os.urandom(file_size_bytes))
            current_usage += file_size_bytes

        QMessageBox.information(self, "Information", "“Disk filling complete!")

    def get_disk_usage(self, directory):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    def generate_random_filename(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(10)) + '.dat'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DiskFillerApp()
    ex.show()
    sys.exit(app.exec_())
