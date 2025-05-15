import tkinter as tk
from tkinter import ttk, messagebox
import paramiko
import socket
import select
import threading
import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".ssh_port_forwarder.json"

class SSHForwardingApp:
    def __init__(self, root):
        self.root = root
        root.title("SSH Port Forwarding Wizard")
        self.forwarding_active = False
        self.transport = None
        self.client = None
        self.active_connections = []
        
        self.create_widgets()
        self.load_last_session()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # SSH Server Details
        ttk.Label(self.root, text="SSH Server:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.ssh_host_entry = ttk.Entry(self.root)
        self.ssh_host_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(self.root, text="SSH Port:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.ssh_port_entry = ttk.Entry(self.root)
        self.ssh_port_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(self.root, text="Username:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.ssh_user_entry = ttk.Entry(self.root)
        self.ssh_user_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(self.root, text="Password:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.ssh_password_entry = ttk.Entry(self.root, show="*")
        self.ssh_password_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=2)
        
        # Port Forwarding Details
        ttk.Label(self.root, text="Local Port:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.local_port_entry = ttk.Entry(self.root)
        self.local_port_entry.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(self.root, text="Remote Port:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        self.remote_port_entry = ttk.Entry(self.root)
        self.remote_port_entry.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=2)
        
        # Start/Stop Button
        self.start_button = ttk.Button(self.root, text="Start Forwarding", command=self.toggle_forwarding)
        self.start_button.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Status Area
        self.status_text = tk.Text(self.root, height=10, state=tk.DISABLED)
        self.status_text.grid(row=7, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        
        # Grid configuration
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(7, weight=1)

    def load_last_session(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.ssh_host_entry.insert(0, data.get('host', ''))
                    self.ssh_port_entry.insert(0, str(data.get('port', 22)))
                    self.ssh_user_entry.insert(0, data.get('user', ''))
                    self.local_port_entry.insert(0, str(data.get('local_port', '')))
                    self.remote_port_entry.insert(0, str(data.get('remote_port', '')))
            except Exception as e:
                print(f"Error loading last session: {e}")

    def save_current_session(self):
        session_data = {
            'host': self.ssh_host_entry.get().strip(),
            'port': int(self.ssh_port_entry.get().strip() or 22),
            'user': self.ssh_user_entry.get().strip(),
            'local_port': int(self.local_port_entry.get().strip() or 0),
            'remote_port': int(self.remote_port_entry.get().strip() or 0)
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(session_data, f, indent=2)

    def on_close(self):
        self.save_current_session()
        if self.forwarding_active:
            self.stop_forwarding()
        self.root.destroy()

    def update_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.config(state=tk.DISABLED)
        self.status_text.see(tk.END)

    def toggle_forwarding(self):
        if self.forwarding_active:
            self.stop_forwarding()
        else:
            self.start_forwarding()

    def start_forwarding(self):
        ssh_host = self.ssh_host_entry.get().strip()
        ssh_port = int(self.ssh_port_entry.get().strip() or 22)
        ssh_user = self.ssh_user_entry.get().strip()
        ssh_password = self.ssh_password_entry.get().strip()
        local_port = int(self.local_port_entry.get().strip())
        remote_port = int(self.remote_port_entry.get().strip())

        try:
            if not (1 <= local_port <= 65535) or not (1 <= remote_port <= 65535):
                raise ValueError("Ports must be between 1-65535")
        except ValueError as e:
            self.update_status(f"Error: {e}")
            return

        self.forwarding_active = True
        self.start_button.config(text="Stop Forwarding")
        
        self.ssh_thread = threading.Thread(
            target=self.run_ssh_connection,
            args=(ssh_host, ssh_port, ssh_user, ssh_password, local_port, remote_port),
            daemon=True
        )
        self.ssh_thread.start()

    def stop_forwarding(self):
        self.forwarding_active = False
        self.start_button.config(text="Start Forwarding", state=tk.NORMAL)
        
        for chan, sock in self.active_connections:
            try:
                chan.close()
                sock.close()
            except Exception as e:
                pass
        self.active_connections.clear()
        
        if self.client:
            self.client.close()
        if self.transport:
            self.transport.close()
        
        self.update_status("Forwarding stopped")

    def run_ssh_connection(self, host, port, user, password, local_port, remote_port):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.update_status(f"Connecting to {host}:{port}...")
            self.client.connect(host, port, user, password)
            self.transport = self.client.get_transport()
            
            self.transport.request_port_forward('', remote_port)
            self.update_status(f"Forwarding: localhost:{local_port} -> {host}:{remote_port}")
            
            while self.forwarding_active:
                chan = self.transport.accept(1000)
                if chan:
                    threading.Thread(target=self.handle_tunnel, args=(chan, local_port), daemon=True).start()
                    
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            self.stop_forwarding()

    def handle_tunnel(self, chan, local_port):
        sock = socket.socket()
        try:
            sock.connect(('127.0.0.1', local_port))
            self.active_connections.append((chan, sock))
            
            while self.forwarding_active:
                r, _, _ = select.select([sock, chan], [], [], 1)
                if sock in r:
                    data = sock.recv(4096)
                    if data:
                        chan.send(data)
                if chan in r:
                    data = chan.recv(4096)
                    if data:
                        sock.send(data)
        except Exception as e:
            self.update_status(f"Connection error: {e}")
        finally:
            sock.close()
            chan.close()
            self.update_status("Connection closed")

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHForwardingApp(root)
    root.mainloop()
def main():
    root = tk.Tk()
    app = SSHForwardingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
