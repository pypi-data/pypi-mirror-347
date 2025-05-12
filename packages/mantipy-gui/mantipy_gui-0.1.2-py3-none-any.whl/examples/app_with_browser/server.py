#!/usr/bin/env python3
"""
Simple HTTP server for serving local content for the EvrMail demo
"""

import http.server
import socketserver
import os
import threading
import time
import sys

# Define the port to serve on
PORT = 45465
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


class LocalServer:
    """Simple HTTP server that can be started and stopped"""
    
    def __init__(self, port=PORT, directory=DIRECTORY):
        self.port = port
        self.directory = directory
        self.server = None
        self.thread = None
        self.running = False
        
    def start(self):
        """Start the server in a separate thread"""
        if self.running:
            print(f"Server already running on port {self.port}")
            return
        
        os.chdir(self.directory)
        
        handler = http.server.SimpleHTTPRequestHandler
        self.server = socketserver.TCPServer(("", self.port), handler)
        
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        
        self.running = True
        print(f"Server started on port {self.port}, serving content from {self.directory}")
        
    def stop(self):
        """Stop the server"""
        if not self.running:
            print("Server not running")
            return
            
        self.server.shutdown()
        self.server.server_close()
        self.running = False
        print("Server stopped")


# Function to start the server from other modules
def start_server():
    """Start the local server and return the instance"""
    server = LocalServer()
    server.start()
    return server


if __name__ == "__main__":
    # If run directly, start the server and keep it running
    server = LocalServer()
    server.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()
        sys.exit(0) 