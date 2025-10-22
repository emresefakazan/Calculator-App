"""
Simple Calculator - PyQt5 OOP Design
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QGridLayout, QPushButton, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Calculator:
    """Calculator logic class - handles computation operations"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset the calculator"""
        self.current_value = 0
        self.previous_value = 0
        self.operation = None
        self.display_value = "0"
        self.should_reset_display = False
        self.expression = ""
    
    def set_number(self, number_str):
        """Enter a number"""
        if self.should_reset_display:
            self.display_value = number_str
            self.should_reset_display = False
        else:
            if self.display_value == "0":
                self.display_value = number_str
            else:
                self.display_value += number_str
        
        self.current_value = float(self.display_value)
        return self.display_value
    
    def add_decimal(self):
        """Add a decimal point"""
        if "." not in self.display_value:
            self.display_value += "."
        return self.display_value
    
    def set_operation(self, op):
        """Set an operation"""
        if self.operation and not self.should_reset_display:
            # Complete the previous operation first
            result = self.calculate()
            if result is None:
                return None, "Error: Invalid operation"
        
        self.previous_value = self.current_value
        self.operation = op
        self.expression = f"{self.display_value} {op}"
        self.display_value = "0"  # Clear main display
        self.should_reset_display = True
        
        return self.display_value, self.expression
    
    def calculate(self):
        """Perform calculation"""
        if self.operation is None or self.previous_value is None:
            return self.current_value
        
        try:
            if self.operation == '+':
                result = self.previous_value + self.current_value
            elif self.operation == '-':
                result = self.previous_value - self.current_value
            elif self.operation == '×':
                result = self.previous_value * self.current_value
            elif self.operation == '÷':
                if self.current_value == 0:
                    return None  # Division by zero error
                result = self.previous_value / self.current_value
            elif self.operation == '%':
                if self.current_value == 0:
                    return None  # Division by zero error
                result = self.previous_value % self.current_value
            else:
                return self.current_value
            
            # If result is an integer, display it as an integer
            if result == int(result):
                result = int(result)
            
            self.current_value = result
            self.display_value = str(result)
            self.expression = f"{self.previous_value} {self.operation} {self.current_value} ="
            self.operation = None
            self.previous_value = 0
            self.should_reset_display = True
            
            return result
        except:
            return None
    
    def toggle_sign(self):
        """Toggle sign (+/-)"""
        if self.display_value and self.display_value != '0':
            if self.display_value.startswith('-'):
                self.display_value = self.display_value[1:]
            else:
                self.display_value = '-' + self.display_value
            self.current_value = float(self.display_value)
        return self.display_value
    
    def backspace(self):
        """Delete last character"""
        if len(self.display_value) > 1:
            self.display_value = self.display_value[:-1]
        else:
            self.display_value = "0"
        
        self.current_value = float(self.display_value)
        return self.display_value


class CalculatorButton(QPushButton):
    """Custom calculator button"""
    
    def __init__(self, text, button_type="number"): # Method that runs when object is created
        super().__init__(text)
        self.setFixedSize(60, 50)
        self.setFont(QFont("Arial", 14))
        self.setup_style(button_type)
    
    def setup_style(self, button_type):
        """Set button style"""
        if button_type == "number":
            self.setStyleSheet("""
                QPushButton { 
                    background: #E0E0E0; 
                    color: black; 
                    border: 1px solid #999;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background: #D0D0D0;
                }
                QPushButton:pressed {
                    background: #C0C0C0;
                }
            """)
        elif button_type == "operator":
            self.setStyleSheet("""
                QPushButton { 
                    background: #FF9500; 
                    color: white; 
                    border: 1px solid #CC7700;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #FF8000;
                }
                QPushButton:pressed {
                    background: #E07000;
                }
            """)
        elif button_type == "function":
            self.setStyleSheet("""
                QPushButton { 
                    background: #A0A0A0; 
                    color: black;
                    border: 1px solid #777;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background: #909090;
                }
                QPushButton:pressed {
                    background: #808080;
                }
            """)
        elif button_type == "special":
            self.setStyleSheet("""
                QPushButton { 
                    background: #4CAF50; 
                    color: white;
                    border: 1px solid #388E3C;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #45A049;
                }
                QPushButton:pressed {
                    background: #3D8B40;
                }
            """)


class CalculatorGUI(QMainWindow):
    """Calculator GUI class - manages UI components"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧮 Simple Calculator")
        self.setFixedSize(300, 400)
        self.setup_ui()
    
    def setup_ui(self):
        """Create user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Expression display
        self.expression_display = self.create_expression_display()
        layout.addWidget(self.expression_display)
        
        # Main display
        self.main_display = self.create_main_display()
        layout.addWidget(self.main_display)
        
        # Buttons
        button_layout = self.create_button_layout()
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
    
    def create_expression_display(self):
        """Create expression display field"""
        display = QLineEdit("")
        display.setReadOnly(True)
        display.setFixedHeight(30)
        display.setFont(QFont("Arial", 12))
        display.setAlignment(Qt.AlignRight)
        display.setStyleSheet("""
            QLineEdit {
                background: #F8F8F8;
                border: 1px solid #CCC;
                border-radius: 3px;
                color: #666;
                padding: 5px;
            }
        """)
        return display
    
    def create_main_display(self):
        """Create main display field"""
        display = QLineEdit("0")
        display.setReadOnly(True)
        display.setAlignment(Qt.AlignRight)
        display.setFixedHeight(60)
        display.setFont(QFont("Arial", 20))
        display.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #333;
                border-radius: 5px;
                padding: 10px;
                color: black;
                font-weight: bold;
            }
        """)
        return display
    
    def create_button_layout(self):
        """Create button layout"""
        layout = QGridLayout()
        layout.setSpacing(5)
        
        # Button configuration: (text, button_type)
        button_config = [
            [('C', 'function'), ('⌫', 'function'), ('%', 'operator'), ('÷', 'operator')],
            [('7', 'number'), ('8', 'number'), ('9', 'number'), ('×', 'operator')],
            [('4', 'number'), ('5', 'number'), ('6', 'number'), ('-', 'operator')],
            [('1', 'number'), ('2', 'number'), ('3', 'number'), ('+', 'operator')],
            [('±', 'special'), ('0', 'number'), ('.', 'number'), ('=', 'operator')]
        ]
        
        self.buttons = {}
        
        for row, button_row in enumerate(button_config):
            for col, (text, button_type) in enumerate(button_row):
                button = CalculatorButton(text, button_type)
                self.buttons[text] = button
                layout.addWidget(button, row, col)
        
        return layout
    
    def update_display(self, value):
        """Update main display"""
        self.main_display.setText(str(value))
    
    def update_expression(self, expression):
        """Update expression display"""
        self.expression_display.setText(expression)
    
    def show_error(self, message):
        """Show error message"""
        self.main_display.setText("Error")
        self.expression_display.setText(message)
    
    def connect_buttons(self, callback):
        """Connect buttons to callback function"""
        for button in self.buttons.values():
            button.clicked.connect(lambda checked, btn=button: callback(btn.text()))


class CalculatorController:
    """Calculator controller class - bridge between GUI and logic"""
    
    def __init__(self):
        self.calculator = Calculator()
        self.gui = CalculatorGUI()
        self.gui.connect_buttons(self.handle_button_click)
    
    def handle_button_click(self, button_text):
        """Handle button clicks"""
        if button_text.isdigit():
            self.handle_number(button_text)
        elif button_text == '.':
            self.handle_decimal()
        elif button_text in ['+', '-', '×', '÷', '%']:
            self.handle_operator(button_text)
        elif button_text == '=':
            self.handle_equals()
        elif button_text == 'C':
            self.handle_clear()
        elif button_text == '⌫':
            self.handle_backspace()
        elif button_text == '±':
            self.handle_plus_minus()
    
    def handle_number(self, number):
        """Handle number input"""
        display_value = self.calculator.set_number(number)
        self.gui.update_display(display_value)
    
    def handle_decimal(self):
        """Handle decimal input"""
        display_value = self.calculator.add_decimal()
        self.gui.update_display(display_value)
    
    def handle_operator(self, operator):
        """Handle operator input"""
        result = self.calculator.set_operation(operator)
        if result[0] is None:
            self.gui.show_error(result[1])
        else:
            self.gui.update_display("")  # Clear main display
            self.gui.update_expression(result[1])
    
    def handle_equals(self):
        """Handle equals operation"""
        result = self.calculator.calculate()
        if result is None:
            self.gui.show_error("Error: Division by zero")
        else:
            self.gui.update_display(result)
            self.gui.update_expression(self.calculator.expression)
    
    def handle_clear(self):
        """Handle clear operation"""
        self.calculator.reset()
        self.gui.update_display("0")
        self.gui.update_expression("")
    
    def handle_backspace(self):
        """Handle backspace operation"""
        display_value = self.calculator.backspace()
        self.gui.update_display(display_value)
    
    def handle_plus_minus(self):
        """Handle sign toggle"""
        display_value = self.calculator.toggle_sign()
        self.gui.update_display(display_value)
    
    def show(self):
        """Show the GUI"""
        self.gui.show()


class CalculatorApp:
    """Main application class - initializes and manages the app"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.controller = CalculatorController()
    
    def run(self):
        """Run the application"""
        self.controller.show()
        return self.app.exec_()


def main():
    """Main function"""
    calculator_app = CalculatorApp()
    sys.exit(calculator_app.run())


if __name__ == "__main__":
    main()
