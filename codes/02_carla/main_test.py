# rsu_communication.py

import socket

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

    def send_data(self, data, destination_vehicle_ids=None, sender_rsu_id=None):
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
                    print("Error: Specify either destination_vehicle_ids or destination_rsu_id.")
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


############################

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

###############3
import time

# Example usage
if __name__ == "__main__":
    # Create DSRC communication module instances for each vehicle
    vehicle1_dsrc = DSRCCommunicationModule("localhost", 12345, vehicle_id=1)
    vehicle2_dsrc = DSRCCommunicationModule("localhost", 12346, vehicle_id=2)
    vehicle3_dsrc = DSRCCommunicationModule("localhost", 12347, vehicle_id=3)
    vehicle4_dsrc = DSRCCommunicationModule("localhost", 12348, vehicle_id=4)

    # Create RSU communication module instances for each RSU
    rsu1 = RSUCommunicationModule("localhost", 12349, rsu_id=1)
    rsu2 = RSUCommunicationModule("localhost", 12350, rsu_id=2)

    # Connect DSRC modules for each vehicle
    vehicle1_dsrc.connect()
    vehicle2_dsrc.connect()
    vehicle3_dsrc.connect()
    vehicle4_dsrc.connect()


    vehicle1_dsrc.send_data("EMERGENCYY")

    # # receive messages for each vehicle
    # vehicle2_dsrc.receive_data()
    # vehicle3_dsrc.receive_data()
    # vehicle4_dsrc.receive_data()

    ##DEVAM ETMİYOR BURADAN SONRA ???

    # Connect RSU modules
    rsu1.connect()
    rsu2.connect()

    # # Assign vehicles to RSUs
    rsu1.connected_vehicles = [vehicle1_dsrc, vehicle2_dsrc, vehicle3_dsrc, vehicle4_dsrc]
    rsu2.connected_vehicles = [vehicle1_dsrc, vehicle2_dsrc]

    # # Print connected vehicles for each RSU
    # for rsu in RSUCommunicationModule.connected_rsus:
    #     print(f"Connected vehicles for RSU {rsu.rsu_id}: {[vehicle.vehicle_id for vehicle in rsu.connected_vehicles]}")

    # Example data sending from RSUs to connected vehicles
    rsu1.send_data("Selam", destination_vehicle_ids = rsu1.connected_vehicles, sender_rsu_id=1)
    rsu2.send_data("Sanane", destination_vehicle_ids=[1, 2], sender_rsu_id=2)

    # Example data receiving in vehicles
    time.sleep(0.5)  # Wait for messages to be processed

    for rsu in RSUCommunicationModule.connected_rsus:
        for vehicle in rsu.connected_vehicles:
            vehicle.receive_data()

    # Disconnect DSRC modules and RSU modules
    vehicle1_dsrc.disconnect()
    vehicle2_dsrc.disconnect()
    vehicle3_dsrc.disconnect()
    vehicle4_dsrc.disconnect()

    rsu1.disconnect()
    rsu2.disconnect()

    print("\n\n\n Completed")

