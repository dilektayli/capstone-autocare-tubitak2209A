# dedicated short range communication (DSRC)

import socket

class DSRCCommunicationModule:
    connected_vehicles = []

    def __init__(self, host, port, vehicle_id):
        self.host = host
        self.port = port
        self.vehicle_id = vehicle_id
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        DSRCCommunicationModule.connected_vehicles.append(self)
        print(f"DSRC Communication Module connected on {self.host}:{self.port} for Vehicle {self.vehicle_id}")

    def send_data(self, data, destination_vehicle_id=None):
        if self.socket:
            for vehicle in DSRCCommunicationModule.connected_vehicles:
                if vehicle.vehicle_id != self.vehicle_id and (destination_vehicle_id is None or vehicle.vehicle_id == destination_vehicle_id):
                    message = f"{self.vehicle_id}:{data}"
                    vehicle.socket.sendto(message.encode(), (self.host, self.port))
                    print(f"Data sent from Vehicle {self.vehicle_id} to Vehicle {vehicle.vehicle_id}: {data}")
        else:
            print("Error: Connection not established.")
        
    def receive_data(self):
        if self.socket:
            data, _ = self.socket.recvfrom(1024)
            sender_vehicle_id, message = data.decode().split(":", 1)
            if sender_vehicle_id.startswith("RSU"):
                print(f"Received data from RSU {sender_vehicle_id[3:]}: {message}")
            else:
                print(f"Received data from Vehicle {sender_vehicle_id}: {message}")
        else:
            print("Error: Connection not established.")

    def disconnect(self):
        if self.socket:
            self.socket.close()
            DSRCCommunicationModule.connected_vehicles.remove(self)
            self.socket = None
            print(f"DSRC Communication Module for Vehicle {self.vehicle_id} disconnected.")
        else:
            print("Error: Connection not established.")
