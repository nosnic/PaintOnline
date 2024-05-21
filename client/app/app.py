from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QColorDialog, QSlider
from PyQt5 import QtGui

from .template.window import Ui_Main_Window
from .connect_dialog import ConnectDialog
from .surface import Surface
from .client import Client
from .listener import Listener


class MainWindow(QMainWindow, Ui_Main_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_pencil.clicked.connect(self.show_dialog_color)
        self.action_connect.triggered.connect(self.show_dialog_connect)
        self.button_clear.clicked.connect(self.clear_surface)
        self.color_red.clicked.connect(self.change_color_red)
        self.color_blue.clicked.connect(self.change_color_blue)
        self.color_yellow.clicked.connect(self.change_color_yellow)
        self.color_green.clicked.connect(self.change_color_green)
        self.button_eraser.clicked.connect(self.change_color_black)
        self.client = None
        self.surface = None
        self.listener = None

    def change_color_black(self):
        if self.surface:
            self.surface.set_pen(size=self.surface.size, color=QBrush(Qt.black))

    def change_color_red(self):
        if self.surface:
            self.surface.set_pen(size=self.surface.size, color=QBrush(Qt.red))

    def change_color_blue(self):
        if self.surface:
            self.surface.set_pen(size=self.surface.size, color=QBrush(Qt.blue))

    def change_color_yellow(self):
        if self.surface:
            self.surface.set_pen(size=self.surface.size, color=QBrush(Qt.yellow))

    def change_color_green(self):
        if self.surface:
            self.surface.set_pen(size=self.surface.size, color=QBrush(Qt.green))


    def show_dialog_color(self):
        dialog = QColorDialog()
        pen_size = QSlider(Qt.Horizontal)
        pen_size.setMinimum(1)
        pen_size.setMaximum(6)
        layout = dialog.layout()
        layout.addWidget(pen_size)
        dialog.setLayout(layout)
        if dialog.exec_() and self.surface:
            self.surface.set_pen(size=pen_size.value(), color=dialog.selectedColor().name())

    def clear_surface(self):
        if self.client:
            server_address = self.client.get_server()
            client_address = self.client.get_ip()
            self.client.sendto(bytes(str({"command": "clear"}), 'utf-8'), (server_address, client_address))

    def show_dialog_connect(self):
        dialog = ConnectDialog()
        if dialog.exec_():
            ip = Client.get_client_address(dialog.client_port)
            self.connect(dialog.server, ip)

    def connect(self, server_address, client_address):
        print(server_address, client_address)
        self.client = Client(client_address.to_tuple(), server_address.to_tuple())  # Передача кортежей адресов
        self.surface = Surface(self)
        self.listener = Listener(self)
        self.scrollArea.setWidget(self.surface)
        self.client.sendto(bytes(str({"command": "hello"}), 'utf-8'),
                           server_address.to_tuple())  # Использование server_address вместо get_server()
        self.listener.start()


    def closeEvent(self, event):
        if self.client:
            self.client.sendto(bytes(str({"command": "buy"}), 'utf-8'), self.client.get_server)
            self.client.sendto(bytes(str({"command": "buy"}), 'utf-8'), self.client.get_ip)
        if self.listener:
            self.listener.is_listen = False
        event.accept()
