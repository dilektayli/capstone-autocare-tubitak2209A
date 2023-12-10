# rsu_communication.py

import socket
import time

class Vehicle:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.socket = None
        self.host = "localhost"  # You can adjust the host/port as needed
        self.port = 0  # You can adjust the port as needed
        self.rsu_id = None  # Added rsu_id attribute

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        print(f"Vehicle {self.vehicle_id} connected to RSU {self.rsu_id} on {self.host}:{self.port}")

    def receive_data(self):
        if self.socket:
            data, _ = self.socket.recvfrom(1024)
            sender_id, message = data.decode().split(":", 1)
            print(f"Received data from {sender_id} to Vehicle {self.vehicle_id}: {message}")
        else:
            print("Error: Connection not established.")

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            print(f"Vehicle {self.vehicle_id} disconnected.")
        else:
            print("Error: Connection not established.")


class RSUCommunicationModule:
    connected_rsus = []

    def __init__(self, host, port, rsu_id):
        self.host = host
        self.port = port
        self.rsu_id = rsu_id
        self.socket = None
        self.connected_vehicles = []  # Initialize an empty list for connected vehicles

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        RSUCommunicationModule.connected_rsus.append(self)
        print(f"RSU Communication Module connected on {self.host}:{self.port} for RSU {self.rsu_id}")

    def send_data(self, data, destination_vehicle_ids=None):
        if self.socket:
            if destination_vehicle_ids is not None:
                for vehicle in self.connected_vehicles:
                    if vehicle.vehicle_id in destination_vehicle_ids:
                        message = f"RSU{self.rsu_id}:{data}"
                        vehicle.socket.sendto(message.encode(), (vehicle.host, vehicle.port))
                        print(f"Data sent from RSU {self.rsu_id} to Vehicle {vehicle.vehicle_id}: {data}")
                else:
                    print(f"Data sent to vehicles {destination_vehicle_ids} from RSU {self.rsu_id}: {data}")
            else:
                print("Error: Specify destination_vehicle_ids.")
        else:
            print("Error: Connection not established.")

    def disconnect(self):
        if self.socket:
            self.socket.close()
            RSUCommunicationModule.connected_rsus.remove(self)
            self.socket = None
            print(f"RSU Communication Module for RSU {self.rsu_id} disconnected.")
        else:
            print("Error: Connection not established.")

# Example usage
if __name__ == "__main__":
    # Create RSU communication module instances for each RSU
    rsu1 = RSUCommunicationModule("localhost", 12349, rsu_id=1)
    rsu2 = RSUCommunicationModule("localhost", 12350, rsu_id=2)

    # Create Vehicle instances for each vehicle
    vehicle1 = Vehicle(vehicle_id=1)
    vehicle2 = Vehicle(vehicle_id=2)
    vehicle3 = Vehicle(vehicle_id=3)
    vehicle4 = Vehicle(vehicle_id=4)

    # Connect RSU modules
    rsu1.connect()
    rsu2.connect()

    # Connect vehicles with the correct port and associate them with RSUs
    vehicle1.port = 12345
    vehicle1.rsu_id = 1

    vehicle3.port = 12347
    vehicle3.rsu_id = 1

    vehicle2.port = 12346
    vehicle2.rsu_id = 2
   
    vehicle4.port = 12348
    vehicle4.rsu_id = 2

    vehicle1.connect()
    vehicle2.connect()
    vehicle3.connect()
    vehicle4.connect()

    # Assign vehicles to RSUs
    rsu1.connected_vehicles = [vehicle1, vehicle3]
    rsu2.connected_vehicles = [vehicle2, vehicle4]

    # Example data sending from RSUs to connected vehicles
    rsu1.send_data("Message from RSU1", destination_vehicle_ids=[vehicle1.vehicle_id, vehicle3.vehicle_id])
    rsu2.send_data("Message from RSU2", destination_vehicle_ids=[vehicle2.vehicle_id, vehicle4.vehicle_id])

    # Example data receiving in vehicles
    time.sleep(0.5)  # Wait for messages to be processed

    for rsu in RSUCommunicationModule.connected_rsus:
        for vehicle in rsu.connected_vehicles:
            vehicle.receive_data()

    # Disconnect RSU modules and vehicles
    rsu1.disconnect()
    rsu2.disconnect()

    vehicle1.disconnect()
    vehicle2.disconnect()
    vehicle3.disconnect()
    vehicle4.disconnect()

    print("\n\n\n Completed")
