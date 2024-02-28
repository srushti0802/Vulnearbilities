import sys
import os
import importlib
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QGridLayout

def get_scan_function(vulnerability_number):
    vulnerability_file = f'vulnerabilities.vulnerability_{vulnerability_number}'
    print(f'Using the import {vulnerability_file}')
    try:
        module = importlib.import_module(vulnerability_file)
        return getattr(module, 'scan')
    except ImportError as e:
        print(f'Error importing {vulnerability_file}: {e}')
        return None

class AutomaticPentestingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        cwd = os.getcwd()
        if cwd not in sys.path:
            sys.path.append(cwd)
        self.setWindowTitle('Automatic Pentesting Application')
        self.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('Enter Website URL Or Domain Name')
        layout.addWidget(self.url_input)

        self.scan_all_button = QPushButton('Scan All')
        self.scan_all_button.clicked.connect(self.scan_all)
        layout.addWidget(self.scan_all_button)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        layout.addLayout(self.grid)

        self.setLayout(layout)

        self.create_buttons()

    def create_buttons(self):
        for i in range(52):
            row = i // 4
            col = i % 4

            vulnerability_name = f'Vulnerability {i+1}'
            button = QPushButton(vulnerability_name)
            button.clicked.connect(lambda ch, i=i: self.on_button_clicked(i))
            self.grid.addWidget(button, row, col)

    def scan_all(self):
        url = self.url_input.text()
        if not url:
            return

        for i in range(1, 53):
            vulnerability_function = get_scan_function(i)
            status = vulnerability_function(url)

            # Display the status in a message box
            QMessageBox.information(self, 'Scan Result', status)

    def on_button_clicked(self, index):
        url = self.url_input.text()
        if not url:
            return

        vulnerability_function = get_scan_function(index + 1)
        status = vulnerability_function(url)

        # Display the status in a message box
        QMessageBox.information(self, 'Scan Result', status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutomaticPentestingApp()
    ex.show()
    sys.exit(app.exec_())