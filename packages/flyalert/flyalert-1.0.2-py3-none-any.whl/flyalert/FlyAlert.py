from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer

import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog,
    QGraphicsDropShadowEffect, QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer

import sys


class FlyAlert(QDialog):
    ICONS = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'question': '❓'
    }

    class FlyAlert(QDialog):
        """
        A highly customizable animated alert dialog for PyQt5 applications.

        This class provides a flexible notification system with smooth animations, configurable
        buttons, and positional settings. Ideal for displaying success, error, warning, and
        informational alerts in a clean and visually appealing manner.

        Attributes:
            ICONS (dict): A dictionary mapping alert types to their corresponding emoji icons.
            config (dict): A dictionary containing alert properties such as title, message,
                           icon type, and button configurations.
            position (str): Defines the alert position on the screen. Can be 'top-left',
                            'top-right', 'bottom-left', 'bottom-right', or 'center'.
            opacity_anim (QPropertyAnimation): Handles the fade-in animation.
            close_anim (QPropertyAnimation): Handles the fade-out animation.

        Methods:
            init_ui(): Sets up the graphical elements of the alert window.
            add_button(layout, button_key, default_color, default_action): Creates and
                adds buttons based on the configuration.
            start_animation(): Starts the fade-in effect upon opening the dialog.
            close_animation(): Starts the fade-out effect and closes the alert.
            show(): Displays the alert at the specified position.
        """

        ICONS = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️',
            'question': '❓'
        }

        def __init__(self, config: dict):
            """
            Initializes a FlyAlert dialog with custom settings.

            Args:
                config (dict): A dictionary defining alert properties such as message text,
                               title, button visibility, colors, and actions.
            """
            super().__init__()
            self.config = config
            self.position = config.get("position", "center")
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setFixedSize(400, 300)

            self.opacity_anim = None
            self.close_anim = None  # Will be initialized when closing
            self.init_ui()
            self.start_animation()

        def init_ui(self):
            """
            Configures the alert's user interface, including layout structure, styling,
            icon, title, message, and action buttons.
            """
            self.container = QWidget(self)
            self.container.setGeometry(10, 10, 380, 280)

            # Apply drop shadow effect for a modern UI appearance
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(24)
            shadow.setColor(QColor(0, 0, 0, 80))
            shadow.setOffset(0, 4)
            self.container.setGraphicsEffect(shadow)
            self.container.setStyleSheet("background-color: white; border-radius: 15px;")

            layout = QVBoxLayout(self.container)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(15)

            # Add icon
            icon_label = QLabel(self.ICONS.get(self.config.get("icon", "info"), 'ℹ️'))
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setFont(QFont("Arial", 50))
            layout.addWidget(icon_label)

            # Add title
            title_label = QLabel(self.config.get("title", "Default Title"))
            title_label.setFont(QFont("Arial", 14, QFont.Bold))
            title_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(title_label)

            # Add message text
            message_label = QLabel(self.config.get("message", "Default Message"))
            message_label.setFont(QFont("Arial", 12))
            message_label.setAlignment(Qt.AlignCenter)
            message_label.setWordWrap(True)
            layout.addWidget(message_label)

            # Create button layout
            button_layout = QHBoxLayout()
            button_layout.setSpacing(10)

            # Add buttons dynamically based on configuration
            self.add_button(button_layout, "ConfirmButton", "#4CAF50", self.accept)
            self.add_button(button_layout, "CancelButton", "#F44336", self.reject)
            self.add_button(button_layout, "InfoButton", "#2196F3", self.accept)

            layout.addLayout(button_layout)

        def add_button(self, layout: QHBoxLayout, button_key: str, default_color: str, default_action):
            """
            Dynamically adds a button to the alert based on the provided configuration.

            Args:
                layout (QHBoxLayout): The layout to which the button will be added.
                button_key (str): The configuration key representing the button settings.
                default_color (str): The default color of the button.
                default_action (function): The function to be executed when the button is clicked.
            """
            if self.config.get(button_key, False):
                btn = QPushButton(self.config.get(f"{button_key}Text", f"{button_key.replace('Button', '')}"))
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.config.get(f"{button_key}Color", default_color)};
                        color: white;
                        padding: 8px 16px;
                        border: none;
                        border-radius: 8px;
                    }}
                    QPushButton:hover {{
                        background-color: {default_color};
                    }}
                """)
                btn.clicked.connect(self.config.get(f"{button_key}Clicked", default_action))
                layout.addWidget(btn)

        def start_animation(self):
            """
            Initiates the fade-in animation when the alert is displayed.
            """
            self.setWindowOpacity(0.0)
            self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
            self.opacity_anim.setDuration(300)
            self.opacity_anim.setStartValue(0.0)
            self.opacity_anim.setEndValue(1.0)
            self.opacity_anim.setEasingCurve(QEasingCurve.OutQuad)
            self.opacity_anim.start()

        def close_animation(self):
            """
            Initiates the fade-out animation and closes the alert after the animation completes.
            """
            self.close_anim = QPropertyAnimation(self, b"windowOpacity")
            self.close_anim.setDuration(300)
            self.close_anim.setStartValue(1.0)
            self.close_anim.setEndValue(0.0)
            self.close_anim.setEasingCurve(QEasingCurve.InQuad)
            self.close_anim.start()
            QTimer.singleShot(300, self.close)

        def show(self, parent_window=None):
            """
            Displays the alert at the predefined position on the screen.
            """
            if parent_window:
                # محاسبه موقعیت نسبت به پنجره والد
                parent_geometry = parent_window.geometry()

                positions = {
                    "top-right": (parent_geometry.right() - self.width() - 20,
                                  parent_geometry.top() + 20),
                    "top-left": (parent_geometry.left() + 20,
                                 parent_geometry.top() + 20),
                    "bottom-right": (parent_geometry.right() - self.width() - 20,
                                     parent_geometry.bottom() - self.height() - 20),
                    "bottom-left": (parent_geometry.left() + 20,
                                    parent_geometry.bottom() - self.height() - 20),
                    "center": (parent_geometry.center().x() - self.width() // 2,
                               parent_geometry.center().y() - self.height() // 2)
                }
            else:
                screen = QApplication.primaryScreen()
                available_geometry = screen.availableGeometry()

                positions = {
                    "top-right": (available_geometry.width() - self.width() - 20, 20),
                    "top-left": (20, 20),
                    "bottom-right": (available_geometry.width() - self.width() - 20,
                                     available_geometry.height() - self.height() - 20),
                    "bottom-left": (20, available_geometry.height() - self.height() - 20),
                    "center": (available_geometry.center().x() - self.width() // 2,
                               available_geometry.center().y() - self.height() // 2)
                }

            pos_x, pos_y = positions.get(self.position, positions["center"])
            self.move(pos_x, pos_y)

            super().exec_()


class MinimalFlyAlert(FlyAlert):
    """
    A lightweight variant of FlyAlert with automatic closing.

    This class provides a minimal popup alert designed for brief notifications.
    Unlike the standard FlyAlert, it has a **smaller size** and can automatically
    disappear after a set duration.

    Attributes:
        position (str): Defines where the alert appears ('top-left', 'top-right',
                        'bottom-left', 'bottom-right', or 'center'). Default: "center".
        auto_close_time (int): The time in milliseconds before the alert automatically closes.
                               Default: 5000ms (5 seconds).

    Methods:
        init_ui(): Sets up the graphical elements of the minimal alert.
        start_auto_close_timer(): Starts a timer that automatically closes the alert.
    """

    def __init__(self, config: dict):
        """
        Initializes a MinimalFlyAlert with custom settings.

        Args:
            config (dict): A dictionary defining alert properties such as message text,
                           title, icon type, and auto-close time.
        """
        super().__init__(config)
        self.position = config.get("position", "center")
        self.auto_close_time = config.get("auto_close_time", 5000)  # Default to 5 seconds
        self.setFixedSize(400, 80)

        self.init_ui()
        self.start_auto_close_timer()

    def init_ui(self):
        """
        Configures the user interface for the minimal alert.

        The UI consists of:
        - An **icon** representing the alert type (success, error, warning, etc.).
        - A **message label** displaying the alert text.
        - A **close button** allowing manual dismissal.
        """
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 400, 80)
        self.container.setStyleSheet("background-color: white; border-radius: 10px;")

        # Define layout structure
        layout = QGridLayout(self.container)
        layout.setContentsMargins(10, 10, 10, 10)

        # Icon for alert type
        icon_label = QLabel(self.ICONS.get(self.config.get("icon", "info"), 'ℹ️'))
        icon_label.setFont(QFont("Arial", 32))

        # Message label
        message_label = QLabel(self.config.get("message", "Default Message"))
        message_label.setFont(QFont("Arial", 14))

        # Close button
        close_button = QPushButton("✖")
        close_button.setFont(QFont("Arial", 24))
        close_button.setStyleSheet("""
            QPushButton {
                background: transparent; font-size: 24px; border: none;
                color: black;
            }
            QPushButton:hover {
                color: red;
                font-size: 26px;
            }
        """)
        close_button.clicked.connect(self.close_animation)

        # Add widgets to layout
        layout.addWidget(icon_label, 0, 0)
        layout.addWidget(message_label, 0, 1)
        layout.addWidget(close_button, 0, 2)

    def start_auto_close_timer(self):
        """
        Starts a countdown timer to close the alert automatically.

        If `auto_close_time` is set, the alert will fade out and close after
        the specified time in milliseconds.
        """
        if self.auto_close_time:
            QTimer.singleShot(self.auto_close_time, self.close_animation)
