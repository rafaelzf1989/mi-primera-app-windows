import tkinter as tk
import socket
import threading

class PTTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PTT Windows - Servidor")
        self.root.geometry("380x320")
        self.root.resizable(False, False)

        # Variables de red
        self.server_socket = None
        self.client_socket = None
        self.is_listening = False
        self.client_ip = "No conectado"

        # --- Interfaz Gráfica ---
        # Marco de configuración
        frame_config = tk.LabelFrame(root, text="Configuración del Servidor", padx=10, pady=10)
        frame_config.pack(pady=10, padx=20, fill="x")

        tk.Label(frame_config, text="IP de escucha:").grid(row=0, column=0, sticky="w")
        self.entry_ip = tk.Entry(frame_config, width=18)
        self.entry_ip.insert(0, "0.0.0.0")  # Escucha en todas las interfaces
        self.entry_ip.grid(row=0, column=1, padx=5)

        tk.Label(frame_config, text="Puerto:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_port = tk.Entry(frame_config, width=18)
        self.entry_port.insert(0, "12345")
        self.entry_port.grid(row=1, column=1, padx=5)

        self.btn_start = tk.Button(frame_config, text="Iniciar Servidor", command=self.toggle_server, bg="#4CAF50", fg="white")
        self.btn_start.grid(row=2, column=0, columnspan=2, pady=10)

        self.lbl_status = tk.Label(frame_config, text="Estado: Detenido", fg="red")
        self.lbl_status.grid(row=3, column=0, columnspan=2)

        # Marco de PTT e indicador
        frame_ptt = tk.Frame(root)
        frame_ptt.pack(pady=20)

        self.indicador = tk.Canvas(frame_ptt, width=80, height=80, bg="#333")
        self.indicador.pack()
        self.circulo = self.indicador.create_oval(10, 10, 70, 70, fill="#555", outline="")

        self.btn_ptt = tk.Button(frame_ptt, text="PTT (Enviar a Android)", width=25, height=2,
                                 command=self.enviar_ptt, state="disabled", bg="#2196F3", fg="white")
        self.btn_ptt.pack(pady=10)

        self.lbl_cliente = tk.Label(root, text="Cliente: No conectado", fg="blue")
        self.lbl_cliente.pack(side="bottom", pady=10)

    def toggle_server(self):
        if not self.is_listening:
            self.start_server()
        else:
            self.stop_server()

    def start_server(self):
        ip = self.entry_ip.get()
        port = int(self.entry_port.get())
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((ip, port))
            self.server_socket.listen(1)
            self.is_listening = True
            self.lbl_status.config(text=f"Estado: Escuchando en {ip}:{port}", fg="green")
            self.btn_start.config(text="Detener Servidor", bg="#f44336")
            self.entry_ip.config(state="disabled")
            self.entry_port.config(state="disabled")
            # Hilo para aceptar conexiones
            threading.Thread(target=self.accept_clients, daemon=True).start()
        except Exception as e:
            self.lbl_status.config(text=f"Error: {e}", fg="red")

    def stop_server(self):
        self.is_listening = False
        if self.client_socket:
            try: self.client_socket.close()
            except: pass
            self.client_socket = None
        if self.server_socket:
            try: self.server_socket.close()
            except: pass
        self.lbl_status.config(text="Estado: Detenido", fg="red")
        self.btn_start.config(text="Iniciar Servidor", bg="#4CAF50")
        self.entry_ip.config(state="normal")
        self.entry_port.config(state="normal")
        self.btn_ptt.config(state="disabled")
        self.lbl_cliente.config(text="Cliente: No conectado")
        self.encender_indicador(False)

    def accept_clients(self):
        while self.is_listening:
            try:
                client, addr = self.server_socket.accept()
                self.client_socket = client
                self.client_ip = addr[0]
                self.lbl_cliente.config(text=f"Cliente: {self.client_ip}")
                self.btn_ptt.config(state="normal")
                # Hilo para escuchar mensajes del cliente
                threading.Thread(target=self.escuchar_cliente, args=(client,), daemon=True).start()
            except:
                break

    def escuchar_cliente(self, client):
        while True:
            try:
                data = client.recv(1024).decode('utf-8')
                if not data: break
                if data == "ANDROID_PTT_ON":
                    self.encender_indicador(True)
                elif data == "ANDROID_PTT_OFF":
                    self.encender_indicador(False)
            except:
                break
        # Si se desconecta
        self.client_socket = None
        self.btn_ptt.config(state="disabled")
        self.lbl_cliente.config(text="Cliente: Desconectado")
        self.encender_indicador(False)

    def enviar_ptt(self):
        if self.client_socket:
            try:
                self.client_socket.send("WINDOWS_PTT_ON".encode('utf-8'))
                # Simula que se mantiene presionado brevemente (puedes ajustarlo)
                self.root.after(500, lambda: self.client_socket.send("WINDOWS_PTT_OFF".encode('utf-8')))
            except:
                pass

    def encender_indicador(self, on):
        color = "#00FF00" if on else "#555"
        self.indicador.itemconfig(self.circulo, fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = PTTApp(root)
    root.mainloop()
