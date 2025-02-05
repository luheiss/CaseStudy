import os
from tinydb import TinyDB, Query
from serializer import serializer

def find_devices() -> list:
    """Find all devices in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')
    # Search the database for all devices that are active
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [x["device_name"] for x in result if "device_name" in x]
    return result

def find_users() -> list:
    """Find all users in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('users')
    # Search the database for all devices that are active
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [y["id"] for y in result if "id" in y]
    return result



if __name__ == "__main__":
    print(find_users())