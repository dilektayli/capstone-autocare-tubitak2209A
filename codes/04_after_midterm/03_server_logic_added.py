import socket
import threading
import time
import select
from threading import Event


class Vehicle:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.socket = None
        self.host = "localhost"
        self.port = 12351
        self.data_event = Event()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            print(f"Vehicle {self.vehicle_id} connected to V2N Server on {self.host}:{self.port}")
        except OSError as e:
            print(f"Error: Unable to connect socket for Vehicle {self.vehicle_id}. {e}")
            self.disconnect()

    def receive_data(self):
        if self.socket:
            print(f"Vehicle {self.vehicle_id} waiting for data...")
            self.data_event.wait()  # Wait for the data event to be set
            try:
                data = self.socket.recv(1024)
                print("Received data:", data.decode())
            except (socket.error, ValueError) as e:
                print(f"Error receiving data for Vehicle {self.vehicle_id}. {e}")
            finally:
                self.data_event.clear()  # Reset the data event for the next data transfer
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
        self.accept_connections_thread = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen()
            print(f"V2N Server started on {self.host}:{self.port}")
        except OSError as e:
            print(f"Error: Unable to bind socket for V2N Communication. {e}")
            self.disconnect()

    def accept_connections(self):
        while True:
            try:
                client_socket, addr = self.socket.accept()
                print(f"Accepted connection from {addr}")
                vehicle_id = client_socket.recv(1024).decode()
                vehicle = Vehicle(vehicle_id)
                vehicle.socket = client_socket
                print(f"Vehicle {vehicle_id} connected to V2N Server.")
                self.connected_vehicles.append(vehicle)
            except (socket.error, ConnectionError) as e:
                print(f"Error accepting connection. {e}")
                break  # Break the loop if there is an error accepting connections

    def start_accepting_connections(self):
        self.accept_connections_thread = threading.Thread(target=self.accept_connections)
        self.accept_connections_thread.start()
    
    def send_data(self, data, destination_vehicle_ids=None):
        if destination_vehicle_ids is not None:
            for vehicle in self.connected_vehicles:
                if vehicle.vehicle_id in destination_vehicle_ids:
                    try:
                        message = f"V2N:{data}"
                        vehicle.socket.send(message.encode())
                        print(f"Data sent from V2N to Vehicle {vehicle.vehicle_id}: {data}")
                    except (socket.error, ConnectionError) as e:
                        print(f"Error sending data to Vehicle {vehicle.vehicle_id}. {e}")
                        self.remove_vehicle(vehicle)
        else:
            print("Error: Specify destination_vehicle_ids.")
            # Correct indentation here
            print(f"Data sent to vehicles {destination_vehicle_ids} from V2N: {data}")
    
    def remove_vehicle(self, vehicle):
        if vehicle in self.connected_vehicles:
            vehicle.disconnect()
            self.connected_vehicles.remove(vehicle)

    def disconnect(self):
        if self.accept_connections_thread:
            self.accept_connections_thread.join()  # Wait for the accept_connections thread to finish
        if self.socket:
            self.socket.close()
            self.socket = None
            print("V2N Communication Module disconnected.")
            for vehicle in self.connected_vehicles:
                vehicle.disconnect()
            self.connected_vehicles = []
        else:
            print("Error: Connection not established.")


# Example usage
if __name__ == "__main__":
    v2n_module = V2NCommunicationModule("localhost", 12351)
    v2n_module.connect()
    v2n_module.start_accepting_connections()

    vehicle1 = Vehicle(vehicle_id=1)
    vehicle2 = Vehicle(vehicle_id=2)
    vehicle3 = Vehicle(vehicle_id=3)
    vehicle4 = Vehicle(vehicle_id=4)

    vehicle1.connect()
    vehicle2.connect()
    vehicle3.connect()
    vehicle4.connect()

    v2n_module.send_data("Message from V2N", destination_vehicle_ids=[vehicle1.vehicle_id, vehicle2.vehicle_id, vehicle3.vehicle_id, vehicle4.vehicle_id])

    # Sleep to allow time for data to be received
    time.sleep(1)

    # Signal that data is ready to be received
    for vehicle in [vehicle1, vehicle2, vehicle3, vehicle4]:
        vehicle.data_event.set()

    # Example data receiving in vehicles
    print("Data received:")
    vehicle1.receive_data()
    vehicle2.receive_data()
    vehicle3.receive_data()
    vehicle4.receive_data()

    v2n_module.disconnect()
    print("\n\n\n Completed")