import socket
import logging
import time
from threading import Event


class Vehicle:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.socket = None
        self.host = "localhost"
        self.port = 0
        #self.data_event = Event()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.socket.connect((self.host, self.port))
            print(f"Vehicle {self.vehicle_id} connected to V2N Server on {self.host}:{self.port}")
        except OSError as e:
            print(f"Error: Unable to connect socket for Vehicle {self.vehicle_id}. {e}")
            self.disconnect()

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

class V2NCommunicationModule:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.connected_vehicles = []

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

    v2n_module = V2NCommunicationModule("localhost", 12351)
    v2n_module.connect()

    vehicle1 = Vehicle(vehicle_id=1)
    vehicle1.port = 12345

    vehicle2 = Vehicle(vehicle_id=2)
    vehicle2.port = 12346

    vehicle3 = Vehicle(vehicle_id=3)
    vehicle3.port = 12347

    vehicle4 = Vehicle(vehicle_id=4)
    vehicle4.port = 12348

    vehicle1.connect()
    vehicle2.connect()
    vehicle3.connect()
    vehicle4.connect()

    # Connect vehicles to V2N module
    v2n_module.connected_vehicles = [vehicle1, vehicle2, vehicle3, vehicle4]


    v2n_module.send_data("Message from V2N", destination_vehicle_ids=[vehicle1.vehicle_id, vehicle2.vehicle_id, vehicle3.vehicle_id, vehicle4.vehicle_id])

    # Sleep to allow time for data to be received
    time.sleep(1)

    # Signal that data is ready to be received
    for vehicle in v2n_module.connected_vehicles:
        vehicle.receive_data()

    v2n_module.disconnect()
    vehicle1.disconnect()
    vehicle2.disconnect()
    vehicle3.disconnect()
    vehicle4.disconnect()

    print("\n\n\n Completed")