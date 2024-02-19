import sys
import os
import shutil
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog

class SetupWizard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Setup Wizard')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        label = QLabel('Welcome to The Goose ++ Setup Wizard!')
        layout.addWidget(label)

        install_button = QPushButton('Install')
        install_button.clicked.connect(self.install)
        layout.addWidget(install_button)

        self.setLayout(layout)

    def install(self):
        user_dir = os.path.join(os.path.expanduser('~'))
        install_dir = QFileDialog.getExistingDirectory(self, 'Select Installation Directory', user_dir)
        if install_dir:
            # Perform installation tasks
            print(f'Installing to: {install_dir}')
            # Copy goose_interpreter.py to the installation directory
            shutil.copy('goose_interpreter.py', install_dir)
            # Create goose.bat in the installation directory
            with open(os.path.join(install_dir, 'goose.bat'), 'w') as bat_file:
                bat_file.write(f'@echo off\npython "{os.path.join(install_dir, "goose_interpreter.py")}" %*')
            # Add the directory containing goose.bat to the system PATH
            self.add_to_path(install_dir)
            self.close()

    def add_to_path(self, install_dir):
        # Add the directory containing goose.bat to the system PATH
        try:
            import winreg as reg
        except ImportError:
            import winreg as reg

        key = reg.HKEY_CURRENT_USER
        path = 'Environment'
        try:
            with reg.OpenKey(key, path, 0, reg.KEY_ALL_ACCESS) as environment_key:
                old_path = reg.QueryValueEx(environment_key, 'Path')[0]
                new_path = f'{install_dir};{old_path}'
                reg.SetValueEx(environment_key, 'Path', 0, reg.REG_EXPAND_SZ, new_path)
                print(f'Added {install_dir} to PATH')
        except Exception as e:
            print(f'Error adding to PATH: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wizard = SetupWizard()
    wizard.show()
    sys.exit(app.exec_())
