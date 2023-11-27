import socket
import time

# dedicated short range communication (DSRC)
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

# road side unit communication (RSU)
class RSUCommunicationModule:
    connected_vehicles = []
    connected_rsus = []

    def __init__(self, host, port, rsu_id):
        self.host = host
        self.port = port
        self.rsu_id = rsu_id
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        RSUCommunicationModule.connected_rsus.append(self)
        print(f"RSU Communication Module connected on {self.host}:{self.port} for RSU {self.rsu_id}")

    def send_data(self, data, destination_vehicle_id=None):
        if self.socket:
            for vehicle in RSUCommunicationModule.connected_vehicles:  # Change this line
                if destination_vehicle_id is None or vehicle.vehicle_id == destination_vehicle_id:
                    message = f"RSU{self.rsu_id}:{data}"
                    vehicle.socket.sendto(message.encode(), (vehicle.host, vehicle.port))
                    print(f"Data sent from RSU {self.rsu_id} to Vehicle {vehicle.vehicle_id}: {data}")
        else:
            print("Error: Connection not established.")

    def receive_data(self):
        if self.socket:
            data, _ = self.socket.recvfrom(1024)
            sender_id, message = data.decode().split(":", 1)
            if sender_id.startswith("RSU") and sender_id[3:] == str(self.rsu_id):
                print(f"Received data from RSU {self.rsu_id}: {message}")
            elif sender_id.startswith("RSU"):
                print(f"Received data from another RSU {sender_id[3:]}: {message}")
            else:
                for vehicle in DSRCCommunicationModule.connected_vehicles:
                    if vehicle.vehicle_id == int(sender_id):
                        print(f"Received data from Vehicle {sender_id} to Vehicle {self.vehicle_id}: {message}")
                        break
                else:
                    print(f"Received data from unknown sender {sender_id}: {message}")
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
    # Create instances for four vehicles with unique vehicle IDs
    vehicle1 = DSRCCommunicationModule("localhost", 12345, vehicle_id=1)
    vehicle2 = DSRCCommunicationModule("localhost", 12346, vehicle_id=2)
    vehicle3 = DSRCCommunicationModule("localhost", 12347, vehicle_id=3)
    vehicle4 = DSRCCommunicationModule("localhost", 12348, vehicle_id=4)

    # Create an RSU instance
    rsu1 = RSUCommunicationModule("localhost", 12349, rsu_id=1)

    # Connect vehicles and RSU to the network
    vehicle1.connect()
    vehicle2.connect()
    vehicle3.connect()
    vehicle4.connect()
    rsu1.connect()

    # Example data sending from vehicle1 to all connected vehicles
    vehicle1.send_data("Emergency message to all vehicles")

    # Example data receiving in all vehicles and RSU
    time.sleep(0.5)  # Wait for messages to be processed

    rsu1.send_data("Emergency message from Road Side Unit to all vehicles")

    time.sleep(0.5)  # Wait for messages to be processed

    vehicle1.receive_data()
    vehicle2.receive_data()
    vehicle3.receive_data()
    vehicle4.receive_data()
    rsu1.receive_data()  # RSU'dan gelen veriyi al

    # Disconnect vehicles and RSU from the network
    vehicle1.disconnect()
    vehicle2.disconnect()
    vehicle3.disconnect()
    vehicle4.disconnect()
    rsu1.disconnect()

    print("\n\n\n Completed")
