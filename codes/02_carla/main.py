import carla
import time
from dsrc_communication import DSRCCommunicationModule
from rsu_communication import RSUCommunicationModule

# Connect to Carla server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the Carla world and map
world = client.get_world()

# Create DSRC communication module instances for each vehicle
vehicle1_dsrc = DSRCCommunicationModule("localhost", 12345, vehicle_id=1)
vehicle2_dsrc = DSRCCommunicationModule("localhost", 12346, vehicle_id=2)
vehicle3_dsrc = DSRCCommunicationModule("localhost", 12347, vehicle_id=3)
vehicle4_dsrc = DSRCCommunicationModule("localhost", 12348, vehicle_id=4)

# Create RSU communication module instance
rsu = RSUCommunicationModule("localhost", 12349, rsu_id=1)

# Connect DSRC modules for each vehicle
vehicle1_dsrc.connect()
vehicle2_dsrc.connect()
vehicle3_dsrc.connect()
vehicle4_dsrc.connect()

# Connect RSU module
rsu.connect()

# Example: spawn vehicles in Carla
def spawn_vehicle(spawn_location):
    blueprint_library = world.get_blueprint_library()
    vehicle_blueprint = blueprint_library.filter('vehicle.*')[0]
    spawn_point = carla.Transform(carla.Location(**spawn_location))
    vehicle = world.spawn_actor(vehicle_blueprint, spawn_point)
    return vehicle

# Spawn four Carla vehicles
spawn_locations = [
    {"x": 10, "y": 10, "z": 2},
    {"x": 20, "y": 10, "z": 2},
    {"x": 30, "y": 10, "z": 2},
    {"x": 40, "y": 10, "z": 2}
]

carla_vehicles = [spawn_vehicle(location) for location in spawn_locations]

# Main loop
try:
    # Example: send data from one vehicle to other cars
    dsrc_data = "Carla message from Vehicle 1"
    vehicle1_dsrc.send_data(dsrc_data)

    # Example: Send data from RSU to each Carla vehicle
    rsu_data = "RSU message to Vehicles from RSU 1"
    rsu.send_data(rsu_data)

    # Example: Receive data in each Carla vehicle
    vehicle1_dsrc.receive_data()
    vehicle2_dsrc.receive_data()
    vehicle3_dsrc.receive_data()
    vehicle4_dsrc.receive_data()

    rsu.receive_data()

    # Other Carla-related logic can be added here

    time.sleep(2)  # Adjust as needed

finally:
    # Disconnect DSRC and RSU modules and destroy Carla actors on script exit
    vehicle1_dsrc.disconnect()
    vehicle2_dsrc.disconnect()
    vehicle3_dsrc.disconnect()
    vehicle4_dsrc.disconnect()

    rsu.disconnect()

    for vehicle in carla_vehicles:
        vehicle.destroy()

print("\n\n\n Completed")
