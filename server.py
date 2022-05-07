import socket
import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window


kivy.require("1.9.1")

HOST = '192.168.194.1'
PORT = 42422  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()


class Ev3App(App):
    layout = FloatLayout()
    label = Label(text='Alfred is missing! Please help me find my boy T_T',
                  pos_hint={'x': .45, 'center_y': .5},
                  size_hint=(.1, .1),
                  font_size=28)
    connectBtn = Button(text='connect', pos_hint={'x': .0, 'center_y': .1}, size_hint=(.1, .1))
    leftBtn = Button(text='goleft', pos_hint={'x': .1, 'center_y': .1}, size_hint=(.1, .1))
    rightBtn = Button(text='goright', pos_hint={'x': .3, 'center_y': .1}, size_hint=(.1, .1))
    forwardBtn = Button(text='goforward', pos_hint={'x': .2, 'center_y': .2}, size_hint=(.1, .1))
    backwardBtn = Button(text='gobackward', pos_hint={'x': .2, 'center_y': .1}, size_hint=(.1, .1))
    stopBtn = Button(text='stop', pos_hint={'x': .9, 'center_y': .1}, size_hint=(.1, .1))
    autoBtn = Button(text='auto', pos_hint={'x': .8, 'center_y': .1}, size_hint=(.1, .1))


    def build(self):
        self.connectBtn.bind(on_press=self.initialize_connection)
        self.leftBtn.bind(on_press=self.send_left_command)
        self.rightBtn.bind(on_press=self.send_right_command)
        self.forwardBtn.bind(on_press=self.send_forward_command)
        self.backwardBtn.bind(on_press=self.send_backward_command)
        self.stopBtn.bind(on_press=self.send_stop_command)
        self.autoBtn.bind(on_press=self.prepare_for_automode)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.connectBtn)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        return self.layout


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.send_forward_command(event=None)
        elif keycode[1] == 'a':
            self.send_left_command(event=None)
        elif keycode[1] == 's':
            self.send_backward_command(event=None)
        elif keycode[1] == 'd':
            self.send_right_command(event=None)
        return True


    def initialize_connection(self, event):
        global conn, addr
        conn, addr = s.accept()
        data = conn.recv(1024)
        self.layout.add_widget(self.leftBtn)
        self.layout.add_widget(self.rightBtn)
        self.layout.add_widget(self.forwardBtn)
        self.layout.add_widget(self.backwardBtn)
        self.layout.add_widget(self.stopBtn)
        self.layout.add_widget(self.autoBtn)
        self.layout.remove_widget(self.connectBtn)
        self.label.text ='Alfred found!!! :D Let\'s go!!!'


    def close_socket(self):
        conn.close()
        self.layout.add_widget(self.connectBtn)
        self.layout.remove_widget(self.leftBtn)
        self.layout.remove_widget(self.rightBtn)
        self.layout.remove_widget(self.forwardBtn)
        self.layout.remove_widget(self.backwardBtn)
        self.layout.remove_widget(self.stopBtn)
        self.layout.remove_widget(self.autoBtn)
        self.label.text = 'Alfred is missing! Please help me find my boy T_T'


    def send_left_command(self, event):
        try:
            conn.send(b"left")
        except:
            if conn.fileno() != -1:
                self.close_socket()



    def send_right_command(self, event):
        try:
            conn.send(b"right")
        except:
            if conn.fileno() != -1:
                self.close_socket()


    def send_forward_command(self, event):
        try:
            conn.send(b"forward")
        except:
            if conn.fileno() != -1:
                self.close_socket()

    
    def send_backward_command(self, event):
        try:
            conn.send(b"backward")
        except:
            if conn.fileno() != -1:
                self.close_socket()


    def send_stop_command(self, event):
        try:
            conn.send(b"stop")
        except:
            if conn.fileno() != -1:
                self.close_socket()


    def send_auto_command(self, event):
        try:
            conn.send(b"auto")
        except:
            if conn.fileno() != -1:
                self.close_socket()


    def prepare_for_automode(self, event):
        # Change the UI to match auto mode
        self.send_auto_command(event=None)

# creating the object root for ButtonApp() class
root = Ev3App()

# run function runs the whole program
# i.e run() method which calls the target
# function passed to the constructor.
root.run()

