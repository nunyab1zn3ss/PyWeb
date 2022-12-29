# File: PyWeb
# Author: Nunya

import tkinter as tk
import http.server
import socketserver
import threading
import os
import socket 

class ServerControl(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Create a frame to hold the server controls
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side="top", fill="both", expand=True)

        # Create a label to display the status of the server
        self.status_label = tk.Label(self.control_frame, text="Server is stopped")
        self.status_label.pack(side="top", fill="both", expand=True)

        # Create a button to start the server
        self.start_button = tk.Button(self.control_frame, text="Start Server", command=self.start_server)
        self.start_button.pack(side="left", fill="both", expand=True)

        # Create a button to stop the server
        self.stop_button = tk.Button(self.control_frame, text="Stop Server", command=self.stop_server)
        self.stop_button.pack(side="right", fill="both", expand=True)

        # Create a frame to hold the port and directory inputs
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side="bottom", fill="both", expand=True)

        # Create a label and entry field for the port number
        self.port_entry = tk.Entry(self.input_frame, width=4)
        self.port_entry.pack(side="right", fill="both", expand=True)
        self.port_label = tk.Label(self.input_frame, text="Port:")
        self.port_label.pack(side="right", fill="both", expand=True)

        # Create a label and scroll wheel for the directory
        self.dir_label = tk.Label(self.input_frame, text="Directory:")
        self.dir_label.pack(side="top", fill="both", expand=True)
        self.dir_scrollwheel = tk.Scrollbar(self.input_frame)
        self.dir_scrollwheel.pack(side="right", fill="y")

        # Create a listbox to display the directory options
        self.dir_listbox = tk.Listbox(self.input_frame, yscrollcommand=self.dir_scrollwheel.set)
        self.dir_listbox.pack(side="right", fill="both", expand=True)

        # Configure the scrollwheel to update the listbox
        self.dir_scrollwheel.config(command=self.dir_listbox.yview)

        for root, dirs, files in os.walk("/"):
            for directory in dirs:
                self.dir_listbox.insert("end", os.path.join(root, directory))

        self.dir_scrollwheel.config(command=self.dir_listbox.yview)
        self.port_entry.insert(0, "8000")
        self.dir_listbox.select_set(0)
        self.dir_listbox.event_generate("<<ListboxSelect>>")
        self.server_running = False
        self.server = None
        self.server_thread = None

    def start_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        if not self.server_running:
            port = int(self.port_entry.get())
            directory = self.dir_listbox.get(self.dir_listbox.curselection())
            os.chdir(directory)
            handler = http.server.SimpleHTTPRequestHandler
            self.server = socketserver.TCPServer(("", port), handler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.start()
            self.status_label.config(text="Server is running")
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(text=f"Server is running at http://{ip_address}:{port} in {directory}")
            self.server_running = True

    def stop_server(self):
        if self.server_running:
            self.server.shutdown()
            self.server.server_close()
            self.server_thread.join()
            self.status_label.config(text="Server is stopped")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.server_running = False
            self.server = None
            self.server_thread = None

if __name__ == "__main__":
    app = ServerControl()
    app.title("PyWeb")
    app.geometry("300x150")
    app.mainloop()

