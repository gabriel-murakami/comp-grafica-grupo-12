from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import json
import os

class Comp(BoxLayout):
    # Collect data from each TextInput
    def save_data(self):
        data = {
            'name': self.ids.name.text,
            'sex': self.ids.sex.text,
            'age': self.ids.age.text,
            'ethnicity': self.ids.ethnicity.text,
            'height': self.ids.height.text,
            'weight': self.ids.weight.text
        }

        # Define the file path for saving data
        file_path = "user_data.json"

        # Load existing data if the file already exists
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Append the new data to the existing data
        existing_data.append(data)

        # Save the data back to the JSON file
        with open(file_path, "w") as file:
            json.dump(existing_data, file, indent=4)

        # Clear the text fields after saving
        for key in self.ids:
            self.ids[key].text = ""

        print("Data saved successfully!")



class Comparador(App):
    def build(self):
        return Comp()
    
    def submit_data(self):
        self.root.save_data()
    
if __name__ == "__main__":
    Comparador().run()
