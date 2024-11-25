import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class CommandRunnerThread(QThread):
    # Signal to update the output area with new text
    output_signal = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        # Run the command using subprocess.Popen for live output
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Read the output line by line and emit the signal to update the UI
        for line in process.stdout:
            self.output_signal.emit(line)

        # Also read stderr (errors) and emit it
        for line in process.stderr:
            self.output_signal.emit(f"Error: {line}")

        # Wait for the process to finish
        process.stdout.close()
        process.stderr.close()
        process.wait()


class BashRunner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bash Command Runner")

        # Set up the layout
        layout = QVBoxLayout()

        # Text field for entering the bash command
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter bash command here")
        layout.addWidget(self.command_input)

        # Button to run the command
        self.run_button = QPushButton("Run Command", self)
        self.run_button.clicked.connect(self.run_command)
        layout.addWidget(self.run_button)

        # Output area for displaying results
        self.output_area = QTextEdit(self)
        self.output_area.setPlaceholderText("Command output will appear here")
        self.output_area.setReadOnly(True)
        self.output_area.setVisible(False)  # Initially hidden
        layout.addWidget(self.output_area)

        # Set layout for the window
        self.setLayout(layout)

    def run_command(self):
        # Clear previous output
        self.output_area.clear()

        # Get the command from the text input
        command = self.command_input.text()

        # Make the output area visible
        self.output_area.setVisible(True)

        # Create a new thread to run the command
        self.runner_thread = CommandRunnerThread(command)

        # Connect the output_signal to update the output area
        self.runner_thread.output_signal.connect(self.update_output)

        # Start the thread
        self.runner_thread.start()

    def update_output(self, output):
        # Append new output to the QTextEdit widget
        self.output_area.append(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BashRunner()
    window.show()
    sys.exit(app.exec_())
