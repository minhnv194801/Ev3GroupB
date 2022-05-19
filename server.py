import socket
import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from functools import partial


kivy.require("1.9.1")

HOST = '192.168.1.70'
PORT = 42422  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

robotNames = ["Alfred", "Jarvis", "Walter"]

class HomeScreen(Screen):
    scrollView = ScrollView(size_hint=(1, None), pos_hint={'center_x': .5, 'center_y': .5}, size=(Window.width, 0.7 * Window.height))
    scrollLayout = GridLayout(rows=10)
    connectBtn = Button(text='connect', pos_hint={'x': .0, 'center_y': .1}, size_hint=(.1, .1))
    layout = FloatLayout()
    label = Label(text='Every robot is missing! Please help me find my boys T_T',
                      pos_hint={'x': .45, 'center_y': .5},
                      size_hint=(.1, .1),
                      font_size=28)
    robotBtnMap = {}
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.connectBtn.bind(on_press=self.initialize_connection)

        self.scrollLayout.add_widget(self.label)
        self.scrollView.add_widget(self.scrollLayout)

        self.layout.add_widget(self.connectBtn)
        self.layout.add_widget(self.scrollView)
        self.add_widget(self.layout)

    def initialize_connection(self, event):
        print('initializeConnection')
        global connection, robotNames
        connection, addr = s.accept()
        data = connection.recv(1024)
        robotName = robotNames.pop(0)
        sm.add_widget(RobotScreen(name=robotName))
        print(robotName)
        self.scrollLayout.remove_widget(self.label)
        robotBtn = Button(text=robotName, size_hint=(.1, .1))
        buttoncallback = lambda robot_name:self.moveToRobotScreen(robotName)
        robotBtn.bind(on_press=buttoncallback)
        self.robotBtnMap[robotName] = robotBtn
        self.scrollLayout.add_widget(robotBtn)

    def moveToRobotScreen(self, robot_name):
        if (sm.has_screen(robot_name)):
            sm.current = robot_name
        else:
            self.scrollLayout.remove_widget(self.robotBtnMap[robot_name])
            self.robotBtnMap[robot_name] = None
            if (len(sm.screen_names) == 1):
                self.scrollLayout.add_widget(self.label)


class RobotScreen(Screen):
    layout = None
    label = None
    backBtn = None
    leftBtn = None
    rightBtn = None
    forwardBtn = None
    backwardBtn = None
    stopBtn = None
    autoBtn = None
    table_label = None
    table_text_field = None
    submitBtn = None
    conn = None

    def __init__(self, **kwargs):
        super(RobotScreen, self).__init__(**kwargs)
        global connection
        self.conn = connection

        self.layout = FloatLayout()
        self.label = Label(text=self.name + ' found!!! :D Let\'s go!!!',
                      pos_hint={'x': .45, 'center_y': .5},
                      size_hint=(.1, .1),
                      font_size=28)
        self.backBtn = Button(text='back', pos_hint={'x': 0, 'center_y': .9}, size_hint=(.1, .1))
        self.leftBtn = Button(text='goleft', pos_hint={'x': .1, 'center_y': .1}, size_hint=(.1, .1))
        self.rightBtn = Button(text='goright', pos_hint={'x': .3, 'center_y': .1}, size_hint=(.1, .1))
        self.forwardBtn = Button(text='goforward', pos_hint={'x': .2, 'center_y': .2}, size_hint=(.1, .1))
        self.backwardBtn = Button(text='gobackward', pos_hint={'x': .2, 'center_y': .1}, size_hint=(.1, .1))
        self.stopBtn = Button(text='stop', pos_hint={'x': .9, 'center_y': .1}, size_hint=(.1, .1))
        self.autoBtn = Button(text='auto', pos_hint={'x': .8, 'center_y': .1}, size_hint=(.1, .1))
        self.table_label = Label(text='Table: ',
                            pos_hint={'x': .1, 'center_y': .1},
                            size_hint=(.1, .1))
        self.table_text_field = TextInput(pos_hint={'x': .2, 'center_y': .1}, size_hint=(.1, .1))
        self.submitBtn = Button(text='submit', pos_hint={'x': .3, 'center_y': .1}, size_hint=(.1, .1))

        self.backBtn.bind(on_press=self.goBackToHomeScreen)
        self.leftBtn.bind(on_press=self.send_left_command)
        self.rightBtn.bind(on_press=self.send_right_command)
        self.forwardBtn.bind(on_press=self.send_forward_command)
        self.backwardBtn.bind(on_press=self.send_backward_command)
        self.stopBtn.bind(on_press=self.send_stop_command)
        self.autoBtn.bind(on_press=self.prepare_for_automode)
        self.submitBtn.bind(on_press=self.send_table_command)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.backBtn)
        self.layout.add_widget(self.leftBtn)
        self.layout.add_widget(self.rightBtn)
        self.layout.add_widget(self.forwardBtn)
        self.layout.add_widget(self.backwardBtn)
        self.layout.add_widget(self.stopBtn)
        self.layout.add_widget(self.autoBtn)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.add_widget(self.layout)
        print("Hello")

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

    def close_socket(self):
        global robotNames, sm
        robotNames.append(self.name)
        self.conn.close()
        sm.current = 'Home'
        sm.remove_widget(self)

    def send_left_command(self, event):
        try:
            self.conn.send(b"left")
        except:
            if self.conn.fileno() != -1:
                self.close_socket()

    def send_right_command(self, event):
        try:
            self.conn.send(b"right")
        except:
            if self.conn.fileno() != -1:
                self.close_socket()

    def send_forward_command(self, event):
        try:
            self.conn.send(b"forward")
        except:
            if self.conn.fileno() != -1:
                self.close_socket()

    def send_backward_command(self, event):
        try:
            self.conn.send(b"backward")
        except:
            if self.conn.fileno() != -1:
                self.close_socket()

    def send_stop_command(self, event):
        try:
            self.conn.send(b"stop")
        except:
            if self.conn.fileno() != -1:
                self.close_socket()

    def send_stop_auto_command(self, event):
        self.layout.clear_widgets()
        self.layout.add_widget(self.backBtn)
        self.layout.add_widget(self.leftBtn)
        self.layout.add_widget(self.rightBtn)
        self.layout.add_widget(self.forwardBtn)
        self.layout.add_widget(self.backwardBtn)
        self.layout.add_widget(self.stopBtn)
        self.layout.add_widget(self.autoBtn)
        self.layout.add_widget(self.label)
        self.send_stop_command(event=None)

    def send_auto_command(self, event):
        try:
            self.conn.send(b"auto")
        except:
            if self.conn.fileno() != -1:
                self.close_socket()

    def send_table_command(self, event):
        command = "table "
        command += self.table_text_field.text
        try:
            self.conn.send(command.encode("UTF-8"))
        except:
            if self.conn.fileno() != -1:
                self.close_socket()

    def prepare_for_automode(self, event):
        # Change the UI to match auto mode
        self.layout.clear_widgets()
        self.layout.add_widget(self.backBtn)
        self.layout.add_widget(self.table_label)
        self.layout.add_widget(self.table_text_field)
        self.layout.add_widget(self.submitBtn)
        self.layout.add_widget(self.stopBtn)
        self.stopBtn.bind(on_press=self.send_stop_auto_command)

        self.send_auto_command(event=None)

    def goBackToHomeScreen(self, event):
        sm.current = 'Home'

class Ev3App(App):
    def build(self):
        global sm
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='Home'))
        return sm

# creating the object root for ButtonApp() class
root = Ev3App()

# run function runs the whole program
# i.e run() method which calls the target
# function passed to the constructor.
root.run()

