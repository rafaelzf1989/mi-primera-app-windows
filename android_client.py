from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import socket
import threading

class PTTAndroid(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Variables de red
        self.client_socket = None
        self.is_connected = False

        # --- Interfaz Gráfica ---
        self.add_widget(Label(text="Configuración del Servidor (PC)", font_size='18sp', size_hint_y=None, height=40))

        self.ip_input = TextInput(text='192.168.1.100', multiline=False, size_hint_y=None, height=50)
        self.add_widget(Label(text="IP del PC:", size_hint_y=None, height=30))
        self.add_widget(self.ip_input)

        self.port_input = TextInput(text='12345', multiline=False, size_hint_y=None, height=50)
        self.add_widget(Label(text="Puerto:", size_hint_y=None, height=30))
        self.add_widget(self.port_input)

        self.btn_connect = Button(text="Conectar", size_hint_y=None, height=60, background_color=(0, 0.7, 1, 1))
        self.btn_connect.bind(on_press=self.conectar)
        self.add_widget(self.btn_connect)

        self.status_label = Label(text="Estado: Desconectado", color=(1, 0, 0, 1), size_hint_y=None, height=40)
        self.add_widget(self.status_label)

        # Indicador (similar a la app de Windows)
        self.indicador = Label(text="●", font_size='80sp', color=(0.3, 0.3, 0.3, 1), size_hint_y=None, height=100)
        self.add_widget(self.indicador)

        # Botón PTT (mantener presionado para hablar)
        self.btn_ptt = Button(text="PTT (Mantener para hablar)", size_hint_y=None, height=80,
                              background_color=(0.2, 0.6, 0.2, 1), disabled=True)
        self.btn_ptt.bind(on_press=self.ptt_press)
        self.btn_ptt.bind(on_release=self.ptt_release)
        self.add_widget(self.btn_ptt)

    def conectar(self, instance):
        if self.is_connected:
            self.desconectar()
            return
        ip = self.ip_input.text
        port = int(self.port_input.text)
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, port))
            self.is_connected = True
            self.status_label.text = "Estado: Conectado"
            self.status_label.color = (0, 1, 0, 1)
            self.btn_connect.text = "Desconectar"
            self.btn_connect.background_color = (1, 0, 0, 1)
            self.btn_ptt.disabled = False
            # Hilo para escuchar mensajes del servidor
            threading.Thread(target=self.escuchar_servidor, daemon=True).start()
        except Exception as e:
            self.status_label.text = f"Error: {e}"
            self.status_label.color = (1, 0, 0, 1)

    def desconectar(self):
        self.is_connected = False
        if self.client_socket:
            try: self.client_socket.close()
            except: pass
        self.status_label.text = "Estado: Desconectado"
        self.status_label.color = (1, 0, 0, 1)
        self.btn_connect.text = "Conectar"
        self.btn_connect.background_color = (0, 0.7, 1, 1)
        self.btn_ptt.disabled = True
        self.encender_indicador(False)

    def escuchar_servidor(self):
        while self.is_connected:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data: break
                if data == "WINDOWS_PTT_ON":
                    Clock.schedule_once(lambda dt: self.encender_indicador(True))
                elif data == "WINDOWS_PTT_OFF":
                    Clock.schedule_once(lambda dt: self.encender_indicador(False))
            except:
                break
        Clock.schedule_once(lambda dt: self.desconectar())

    def ptt_press(self, instance):
        if self.is_connected:
            try:
                self.client_socket.send("ANDROID_PTT_ON".encode('utf-8'))
            except:
                pass

    def ptt_release(self, instance):
        if self.is_connected:
            try:
                self.client_socket.send("ANDROID_PTT_OFF".encode('utf-8'))
            except:
                pass

    def encender_indicador(self, on):
        self.indicador.color = (0, 1, 0, 1) if on else (0.3, 0.3, 0.3, 1)

class PTTAndroidApp(App):
    def build(self):
        return PTTAndroid()

if __name__ == '__main__':
    PTTAndroidApp().run()
