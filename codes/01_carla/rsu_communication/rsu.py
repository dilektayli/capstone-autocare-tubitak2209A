# road side unit communication (RSU)
class RSUCommunicationModule:
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
            for vehicle in DSRCCommunicationModule.connected_vehicles:
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
