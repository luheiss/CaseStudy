import os
from tinydb import TinyDB
from serializable import Serializable
from datetime import datetime, timedelta
from typing import Self
from serializer import serializer

class Maintenance(Serializable):

    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('maintenance')

    def __init__(self, device_id: str, first_maintenance: datetime, maintenance_interval: int, maintenance_cost: float, next_maintenance: datetime = None, creation_date: datetime = None, last_update: datetime = None, id: str = None) -> None:
        if not id:
            id = F"{device_id}_{first_maintenance}"

        super().__init__(id, creation_date, last_update)
        self.device_id = device_id
        self.first_maintenance = first_maintenance
        self.__maintenance_interval = maintenance_interval
        self.__maintenance_cost = maintenance_cost
        self.next_maintenance = next_maintenance if next_maintenance else self.calculate_next_maintenance()
        
    def calculate_next_maintenance(self) -> datetime:
        return self.first_maintenance + timedelta(days=self.__maintenance_interval)

    def update_maintenance(self):
        self.first_maintenance = self.next_maintenance
        self.next_maintenance = self.calculate_next_maintenance()
        self.last_update = datetime.now()
        self.store_data()

    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(
            data['device_id'], data['first_maintenance'], data['maintenance_interval'], 
            data['maintenance_cost'], data.get('next_maintenance'), 
            data.get('creation_date'), data.get('last_update'), data.get('id')
        )

    def __str__(self):
        return F"Maintenance: for {self.device_id}, Next: {self.next_maintenance}, Cost: {self.__maintenance_cost} EUR"

if __name__ == "__main__":
    # Create a device maintenance entry
    maintenance1 = Maintenance("Device1", datetime(2025, 1, 1), 30, 100.0)
    maintenance2 = Maintenance("Device2", datetime(2025, 2, 1), 60, 150.0)
    maintenance3 = Maintenance("Device2", datetime(2025, 3, 1), 90, 200.0)

    maintenance1.store_data()
    maintenance2.store_data()
    maintenance3.store_data()

    loaded_maintenance = Maintenance.find_by_attribute("device_id", "Device2", num_to_return=-1)
    if loaded_maintenance:
        for maintenance in loaded_maintenance:
            print(f"Loaded: {maintenance}")
    else:
        print("Maintenance not found.")
