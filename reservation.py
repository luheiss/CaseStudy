from datetime import datetime
import os
from tinydb import Query, TinyDB
from serializer import serializer


class Reservation(serializer):
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('reservations')

    def __init__(self, user_id:str, device_id:str, start_date: datetime, end_date: datetime, creation_date= None, last_update= None):
        id = f"{user_id}_{device_id}_{end_date}"
        super().__init__(id, creation_date, last_update)
        #Todo
        self.user_id= user_id
        self.device_id= device_id
        self.start_date= start_date
        self.end_date= end_date

    def store_data(self)-> None:
       """Save the user to the database"""
       print("Storing User data...")
       # Check if the User already exists in the database
       UserQuery = Query()
       result = self.db_connector.search(UserQuery.id == self.id)
       if result:
           # Update the existing record with the current instance's data
           result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
           print("User Data updated.")
       else:
           # If the device doesn't exist, insert a new record
           self.db_connector.insert(self.__dict__)
           print("User Data inserted.")
           
    def __str__(self):
        return f"Reservation of {self.device_id} by {self.user_id} from {self.start_date} until {self.end_date}"
    
    @classmethod
    def instantiate_from_dict(cls,data:dict):
        return cls(data["user_id"], data["device_id"], data["start_date"],data["end_date"],data["id"])
    
if __name__ == "__main__":
    res1 = Reservation("one@mci.edu", "Device2", "2025-01-16 00:00:00", "2025-01-17 00:00:00")
    res1.start_data()