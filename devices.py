import os
from datetime import datetime, timedelta
from tinydb import TinyDB, Query
from serializer import serializer

class Device:
    # Class variable that is shared between all instances of the class
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')

    # Constructor
    def __init__(self, device_name: str, managed_by_user_id: str, first_maintenance: datetime = None, maintenance_interval: int = 0, maintenance_cost: float = 0.0, next_maintenance: datetime = None, creation_date: datetime = None, last_update: datetime = None) -> None:
        self.device_name = device_name
        self.managed_by_user_id = managed_by_user_id
        self.first_maintenance = first_maintenance
        self.maintenance_interval = maintenance_interval
        self.maintenance_cost = maintenance_cost
        self.next_maintenance = next_maintenance if next_maintenance else self.calculate_next_maintenance()
        self.is_active = True
        self.creation_date = creation_date if creation_date else datetime.now()
        self.last_update = last_update if last_update else datetime.now()
        
    # String representation of the class
    def __str__(self):
        return f'Device (Object) {self.device_name} ({self.managed_by_user_id})'

    # String representation of the class
    def __repr__(self):
        return self.__str__()

    def get_Info(self, info: str) -> str:
        if info == "device_name":
            return self.device_name
        elif info == "managed_by_user_id":
            return self.managed_by_user_id
        elif info == "is_active":
            return str(self.is_active)

    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        if result:
            # Update the existing record with the current instance's data
            self.db_connector.update(self.to_dict(), doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.to_dict())
            print("Data inserted.")

    def delete(self):
        print("Deleting data...")
        # Check if the device exists in the database
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        if result:
            # Delete the record from the database
            self.db_connector.remove(doc_ids=[result[0].doc_id])
            print("Data deleted.")
        else:
            print("Data not found.")

    def set_managed_by_user_id(self, managed_by_user_id: str):
        """Expects `managed_by_user_id` to be a valid user id that exists in the database."""
        self.managed_by_user_id = managed_by_user_id

    # Class method that can be called without an instance of the class to construct an instance of the class
    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1):
        # Load data from the database and create an instance of the Device class
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery[by_attribute] == attribute_value)

        if result:
            data = result[:num_to_return]
            device_results = [cls.instantiate_from_dict(d) for d in data]
            return device_results if num_to_return > 1 else device_results[0]
        else:
            return None

    @classmethod
    def find_all(cls) -> list:
        # Load all data from the database and create instances of the Device class
        devices = []
        for device_data in Device.db_connector.all():
            devices.append(cls.instantiate_from_dict(device_data))
        return devices

    def calculate_next_maintenance(self) -> datetime:
        if self.first_maintenance and self.maintenance_interval > 0:
            return self.first_maintenance + timedelta(days=self.maintenance_interval)
        return None

    def update_maintenance(self):
        if self.next_maintenance and self.maintenance_interval > 0:
            self.first_maintenance = self.next_maintenance
            self.next_maintenance = self.calculate_next_maintenance()
            self.last_update = datetime.now()
            self.store_data()

    @classmethod
    def instantiate_from_dict(cls, data: dict) -> 'Device':
        def parse_datetime(dt):
            return datetime.fromisoformat(dt) if isinstance(dt, str) else None
        
        return cls(
            data['device_name'], 
            data['managed_by_user_id'], 
            parse_datetime(data.get('first_maintenance')), 
            data.get('maintenance_interval', 0), 
            data.get('maintenance_cost', 0.0), 
            parse_datetime(data.get('next_maintenance')),
            parse_datetime(data.get('creation_date')), 
            parse_datetime(data.get('last_update'))
        )

    def to_dict(self) -> dict:
        return {
            'device_name': self.device_name,
            'managed_by_user_id': self.managed_by_user_id,
            'first_maintenance': self.first_maintenance.isoformat() if self.first_maintenance else None,
            'maintenance_interval': self.maintenance_interval,
            'maintenance_cost': self.maintenance_cost,
            'next_maintenance': self.next_maintenance.isoformat() if self.next_maintenance else None,
            'is_active': self.is_active,
            'creation_date': self.creation_date.isoformat(),
            'last_update': self.last_update.isoformat()
        }