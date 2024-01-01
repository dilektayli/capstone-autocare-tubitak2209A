import socket
import time
import logging

class Vehicle:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.socket = None
        self.host = "localhost"
        self.port = 0
        self.rsu_id = None
        self.connected_v2n_modules = []  # List to store connected V2N modules

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.socket.bind((self.host, self.port))
            print(f"Vehicle {self.vehicle_id} connected to RSU {self.rsu_id} on {self.host}:{self.port}")
        except OSError as e:
            print(f"Error: Unable to bind socket for Vehicle {self.vehicle_id}. {e}")
            self.disconnect()

    def connect_to_v2n_module(self, v2n_module):
        self.connected_v2n_modules.append(v2n_module)
        print(f"Vehicle {self.vehicle_id} connected to V2N Module on {v2n_module.host}:{v2n_module.port}")

    def send_data_to_v2n(self, data):
        for v2n_module in self.connected_v2n_modules:
            try:
                message = f"V2N:{data}"
                v2n_module.socket.sendto(message.encode(), (v2n_module.host, v2n_module.port))
                print(f"Data sent from Vehicle {self.vehicle_id} to V2N Module: {data}")
            except socket.error as e:
                print(f"Error sending data to V2N Module. {e}")

    def receive_data(self):
        if self.socket:
            try:
                data, _ = self.socket.recvfrom(1024)
                sender_id, message = data.decode().split(":", 1)
                print(f"Received data from {sender_id} to Vehicle {self.vehicle_id}: {message}")
            except (socket.error, ValueError) as e:
                print(f"Error receiving data for Vehicle {self.vehicle_id}. {e}")
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
        try:
            self.socket.bind((self.host, self.port))
            RSUCommunicationModule.connected_rsus.append(self)
            print(f"RSU Communication Module connected on {self.host}:{self.port} for RSU {self.rsu_id}")
        except OSError as e:
            print(f"Error: Unable to bind socket for RSU {self.rsu_id}. {e}")
            self.disconnect()

    def send_data(self, data, destination_vehicle_ids=None):
        if self.socket:
            if destination_vehicle_ids is not None:
                for vehicle in self.connected_vehicles:
                    if vehicle.vehicle_id in destination_vehicle_ids:
                        try:
                            message = f"RSU{self.rsu_id}:{data}"
                            vehicle.socket.sendto(message.encode(), (vehicle.host, vehicle.port))
                            print(f"Data sent from RSU {self.rsu_id} to Vehicle {vehicle.vehicle_id}: {data}")
                        except socket.error as e:
                            print(f"Error sending data to Vehicle {vehicle.vehicle_id}. {e}")
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


class V2NCommunicationModule:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.connected_vehicles = []  # Initialize an empty list for connected vehicles

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.socket.bind((self.host, self.port))
            print(f"V2N Communication Module connected on {self.host}:{self.port}")
        except OSError as e:
            print(f"Error: Unable to bind socket for V2N Communication. {e}")
            self.disconnect()

    def send_data(self, data, destination_vehicle_ids=None):
        if self.socket:
            if destination_vehicle_ids is not None:
                for vehicle in self.connected_vehicles:
                    if vehicle.vehicle_id in destination_vehicle_ids:
                        try:
                            message = f"V2N:{data}"
                            vehicle.socket.sendto(message.encode(), (vehicle.host, vehicle.port))
                            print(f"Data sent from V2N to Vehicle {vehicle.vehicle_id}: {data}")
                        except socket.error as e:
                            print(f"Error sending data to Vehicle {vehicle.vehicle_id}. {e}")
                else:
                    print(f"Data sent to vehicles {destination_vehicle_ids} from V2N: {data}")
            else:
                print("Error: Specify destination_vehicle_ids.")
        else:
            print("Error: Connection not established.")

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            print("V2N Communication Module disconnected.")
        else:
            print("Error: Connection not established.")


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Create RSU communication module instances for each RSU
    rsu1 = RSUCommunicationModule("localhost", 12349, rsu_id=1)
    rsu2 = RSUCommunicationModule("localhost", 12350, rsu_id=2)

    # Create V2N communication module instances
    v2n_module1 = V2NCommunicationModule("localhost", 12351)
    v2n_module2 = V2NCommunicationModule("localhost", 12352)

    # Create Vehicle instances for each vehicle
    vehicle1 = Vehicle(vehicle_id=1)
    vehicle2 = Vehicle(vehicle_id=2)
    vehicle3 = Vehicle(vehicle_id=3)
    vehicle4 = Vehicle(vehicle_id=4)

    # Connect RSU modules
    rsu1.connect()
    rsu2.connect()

    # Connect V2N modules
    v2n_module1.connect()
    v2n_module2.connect()

    # Connect vehicles with the correct port and associate them with RSUs and V2N modules
    # (Vehicle 1 and 3 to RSU 1, Vehicle 2 and 4 to RSU 2)
    vehicle1.port = 12345
    vehicle1.rsu_id = 1
    vehicle1.connect_to_v2n_module(v2n_module1)  # Connect to V2N Module 1

    vehicle3.port = 12347
    vehicle3.rsu_id = 1
    vehicle3.connect_to_v2n_module(v2n_module1)  # Connect to V2N Module 1

    vehicle2.port = 12346
    vehicle2.rsu_id = 2
    vehicle2.connect_to_v2n_module(v2n_module2)  # Connect to V2N Module 2

    vehicle4.port = 12348
    vehicle4.rsu_id = 2
    vehicle4.connect_to_v2n_module(v2n_module2)  # Connect to V2N Module 2

    vehicle1.connect()
    vehicle2.connect()
    vehicle3.connect()
    vehicle4.connect()

    # Connect vehicles to RSUs
    rsu1.connected_vehicles = [vehicle1, vehicle3]
    rsu2.connected_vehicles = [vehicle2, vehicle4]

    # Connect vehicles to V2N modules
    v2n_module1.connected_vehicles = [vehicle1, vehicle3]
    v2n_module2.connected_vehicles = [vehicle2, vehicle4]

    # Example data sending from RSUs to connected vehicles
    rsu1.send_data("Message from RSU1", destination_vehicle_ids=[vehicle1.vehicle_id, vehicle3.vehicle_id])
    rsu2.send_data("Message from RSU2", destination_vehicle_ids=[vehicle2.vehicle_id, vehicle4.vehicle_id])

    # Example data sending from V2N modules to connected vehicles
    v2n_module1.send_data("Message from V2N1", destination_vehicle_ids=[vehicle1.vehicle_id, vehicle3.vehicle_id])
    v2n_module2.send_data("Message from V2N2", destination_vehicle_ids=[vehicle2.vehicle_id, vehicle4.vehicle_id])

    # Example data receiving in vehicles
    time.sleep(0.5)  # Wait for messages to be processed

    for rsu in RSUCommunicationModule.connected_rsus:
        for vehicle in rsu.connected_vehicles:
            vehicle.receive_data()

    for v2n_module in [v2n_module1, v2n_module2]:
        for vehicle in v2n_module.connected_vehicles:
            vehicle.receive_data()

    # Disconnect RSU modules, V2N modules, and vehicles
    rsu1.disconnect()
    rsu2.disconnect()
    v2n_module1.disconnect()
    v2n_module2.disconnect()
    vehicle1.disconnect()
    vehicle2.disconnect()
    vehicle3.disconnect()
    vehicle4.disconnect()

    print("\n\n\n Completed")
