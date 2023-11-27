import socket

# Dedicated Short Range Communication (DSRC)

class DSRCCommunicationModule:
    # Class variable to keep track of connected vehicles
    connected_vehicles = []

    def __init__(self, host, port, vehicle_id):
        """Initialize DSRCCommunicationModule with the specified host, port, and vehicle ID."""
        self.host = host
        self.port = port
        self.vehicle_id = vehicle_id
        self.socket = None

    def connect(self):
        """Establish a connection to the specified host and port."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        DSRCCommunicationModule.connected_vehicles.append(self)
        print(f"DSRC Communication Module connected on {self.host}:{self.port} for Vehicle {self.vehicle_id}")

    def send_data(self, data, destination_vehicle_id=None):
        """Send data over the established connection."""
        if self.socket:
            for vehicle in DSRCCommunicationModule.connected_vehicles:
                # Send to all connected vehicles except the sender
                if vehicle != self and (destination_vehicle_id is None or vehicle.vehicle_id == destination_vehicle_id):
                    message = f"{self.vehicle_id}:{data}"
                    vehicle.socket.sendto(message.encode(), (self.host, self.port))
                    print(f"Data sent from Vehicle {self.vehicle_id} to Vehicle {vehicle.vehicle_id}: {data}")
        else:
            print("Error: Connection not established.")

    def receive_data(self):
        """Receive data from the established connection."""
        if self.socket:
            data, _ = self.socket.recvfrom(1024)
            sender_vehicle_id, message = data.decode().split(":", 1)
            print(f"Received data from Vehicle {sender_vehicle_id}: {message}")
        else:
            print("Error: Connection not established.")

    def disconnect(self):
        """Close the connection."""
        if self.socket:
            self.socket.close()
            DSRCCommunicationModule.connected_vehicles.remove(self)
            self.socket = None
            print(f"DSRC Communication Module for Vehicle {self.vehicle_id} disconnected.")
        else:
            print("Error: Connection not established.")
# Example usage
if __name__ == "__main__":
    # Create instances for four vehicles with unique vehicle IDs
    vehicle1 = DSRCCommunicationModule("localhost", 12345, vehicle_id=1)
    vehicle2 = DSRCCommunicationModule("localhost", 12346, vehicle_id=2)
    vehicle3 = DSRCCommunicationModule("localhost", 12347, vehicle_id=3)
    vehicle4 = DSRCCommunicationModule("localhost", 12348, vehicle_id=4)

    # Connect vehicles to the network
    vehicle1.connect()
    vehicle2.connect()
    vehicle3.connect()
    vehicle4.connect()

    # Example data sending from vehicle1 to all connected vehicles
    vehicle1.send_data("Emergency message to all vehicles")

    # Example data receiving in all vehicles
    vehicle1.receive_data()
    vehicle2.receive_data()
    vehicle3.receive_data()
    vehicle4.receive_data()

    # Disconnect vehicles from the network
    vehicle1.disconnect()
    vehicle2.disconnect()
    vehicle3.disconnect()
    vehicle4.disconnect()
