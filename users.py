import os

from tinydb import TinyDB, Query
from serializer import serializer

class User:

    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('users')

    def __init__(self, id, name) -> None:
        """Create a new user based on the given name and id"""
        self.name = name
        self.id = id
        self.is_active = True

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
            
    def set_user_name(self, user_name: str):
        """Expects `managed_by_user_id` to be a valid user id that exists in the database."""
        self.name = user_name
    def delete(self) -> None:
        """Delete the user from the database"""
        print("Deleting data...")
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.id == self.id)
        if result:
            # Delete the record from the database
            self.db_connector.remove(doc_ids=[result[0].doc_id])
            print("Data deleted.")
        else:
            print("Data not found.")
    
    def __str__(self):
        return f"User {self.id} - {self.name}"
    
    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def find_all(cls) -> list:
        """Find all users in the database"""
        users = []
        for user_data in User.db_connector.all():
            users.append(User(user_data['name'], user_data['id']))
        return users

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1):
        # Load data from the database and create an instance of the user class
        UserQuery = Query()
        result = cls.db_connector.search(UserQuery[by_attribute] == attribute_value)

        if result:
            data = result[:num_to_return]
            user_results = [cls(d['id'], d['name']) for d in data]
            return user_results if num_to_return > 1 else user_results[0]
        else:
            return None

if __name__ == "__main__":
 print(User.find_all())
 print(User.find_by_attribute("id", "two@mci.edu"))