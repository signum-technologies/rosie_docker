#!/usr/bin/env python3
"""
Terminal-based health monitor that prints measurements continuously.
Uses the same socketio service as the GUI version but outputs to terminal.
"""

import sys
import time
import signal
from datetime import datetime
import argparse

import socketio
import threading
import struct


def bytes_to_float(b):
    return struct.unpack('f', b)[0]


class TerminalSocketioService:
    def __init__(self, app, ip, port):
        self.socket = socketio.Client()
        self.app = app
        self.backend = ip
        self.publisher_url = f"http://{self.backend}:{port}"

    def setup_socket_connection(self):
        try:
            if self.socket.connected:
                self.socket.disconnect()
            self.socket.connect(self.publisher_url)
            self.socket.on('add_chip', self.handle_update_chip)
            self.socket.on('update_chip', self.handle_update_chip)
            self.socket.on('update_feed', self.update_feed)
            self.socket.on('frame_rate', self.frame_rate)
            self.socket.on('thermal_image', self.update_thermal)
            # Update the connection status in the main app - no wx.CallAfter needed
            self.app.update_connection_status(self.backend)
        except Exception as e:
            print(f"Error setting up socket connection: {e}")

    def handle_update_chip(self, data):
        try:
            chip_data = data.get('chip_data', {})
            temp = chip_data.get('temp', 'N/A')
            heartrate = chip_data.get('heartrate', 'N/A')
            resprate = chip_data.get('resprate', 'N/A')
            img = chip_data.get('chip_img', None)
            self.app.update_measurements(heartrate, resprate, temp, img)
        except Exception as e:
            print(f"Error handling update chip: {e}")

    def update_feed(self, data):
        pass

    def update_thermal(self, data):
        pass

    def frame_rate(self, data):
        try:
            fps = bytes_to_float(data)
            self.app.update_fps(fps)
        except Exception as e:
            print(f"Error updating frame rate: {e}")

    def start(self):
        try:
            self.thread = threading.Thread(target=self.setup_socket_connection)
            self.thread.daemon = True
            self.thread.start()
        except Exception as e:
            print(f"Error starting socket service: {e}")

    def get_connected_ip(self):
        return self.backend

    def disconnect(self):
        try:
            if self.socket:
                self.socket.disconnect()
        except Exception as e:
            print(f"Error disconnecting socket: {e}") 


class TerminalMonitor:
    def __init__(self, ip, port):
        self.running = True
        self.last_measurement_time = None
        self.last_fps_time = None
        self.fps_update_interval = 5  # Show FPS every 5 seconds
        print("🏥 Health Pod Terminal Monitor")
        print("=" * 50)
        print(f"Connecting to backend at {ip}:{port}...")
        
        # Initialize the socket service
        self.socket_service = TerminalSocketioService(self, ip, port)
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print("\n\n🛑 Shutting down terminal monitor...")
        self.running = False
        if hasattr(self, 'socket_service'):
            self.socket_service.disconnect()
        sys.exit(0)
    
    def start(self):
        """Start the terminal monitor"""
        try:
            self.socket_service.start()
            print("✅ Socket service started")
            print("📊 Waiting for measurements...")
            print("-" * 50)
            
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
                
        except Exception as e:
            print(f"❌ Error starting terminal monitor: {e}")
            self.running = False
    
    # Methods that SocketioService expects to exist on the app
    def update_measurements(self, heartrate, resprate, temp, img):
        """Called by SocketioService when new measurements arrive"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_measurement_time = timestamp
        
        print(f"\n📈 New Measurements [{timestamp}]")
        if heartrate != -1:
            print(f"   ❤️  Heart Rate: {round(heartrate)} BPM")
        if resprate != -1:
            print(f"   🫁 Respiratory Rate: {round(resprate)} breaths/min")
        print("-" * 50)
    
    def update_rgb_image(self, img_data):
        """Called by SocketioService - we ignore image data in terminal mode"""
        pass
    
    def update_thermal_image(self, img_data):
        """Called by SocketioService - we ignore thermal image data in terminal mode"""
        pass
    
    def update_fps(self, fps):
        """Called by SocketioService when FPS data arrives - only show occasionally"""
        import time
        current_time = time.time()
        
        # Only show FPS updates every few seconds to reduce noise
        if (self.last_fps_time is None or 
            current_time - self.last_fps_time >= self.fps_update_interval):
            print(f"📹 FPS: {fps:.1f}")
            self.last_fps_time = current_time
    
    def update_connection_status(self, ip):
        """Called by SocketioService when connection status changes"""
        print(f"🔗 Connected to backend: {ip}")
    
    def set_face_id(self, face_id):
        """Called when a face is detected - we can log this in terminal mode"""
        if face_id is None:
            print("👤 No person detected")
        else:
            print(f"👤 Person detected (ID: {face_id})")


def main():
    """Main function to run the terminal monitor"""
    parser = argparse.ArgumentParser(description="Rosie Receiver Terminal Monitor")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="IP address of the backend server.")
    parser.add_argument("--port", type=int, default=27182, help="Port of the backend server.")
    args = parser.parse_args()
    try:
        monitor = TerminalMonitor(args.ip, args.port)
        monitor.start()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        print("👋 Terminal monitor stopped")


if __name__ == "__main__":
    main() 