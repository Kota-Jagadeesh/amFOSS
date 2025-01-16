from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QScrollArea, QMessageBox
from PySide6.QtGui import QPixmap
import requests
import os

class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokémon Search")
        self.setFixedSize(850, 500)
        self.captured_pokemon = []

        # Layout setup
        layout = QVBoxLayout()
        self.textbox, self.info_label, self.image_label = QLineEdit(self), QLabel(self), QLabel(self)
        self.textbox.setPlaceholderText("Enter Pokémon name")
        self.image_label.setFixedSize(300, 300)

        layout.addWidget(self.textbox)
        layout.addWidget(QPushButton("Search", self, clicked=self.fetch_pokemon_data))
        self.capture_button = QPushButton("Capture", self, clicked=self.capture_pokemon, enabled=False)
        layout.addWidget(self.capture_button)
        layout.addWidget(QPushButton("Display Captured Pokémon", self, clicked=self.display_captured_pokemon))
        layout.addWidget(self.info_label)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def fetch_pokemon_data(self):
        pokemon_name = self.textbox.text().strip().lower()
        if pokemon_name:
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
            response = requests.get(url)
            if response.status_code == 200:
                self.display_pokemon_data(response.json())
            else:
                QMessageBox.warning(self, "Error", "Pokémon not found.")
        else:
            QMessageBox.warning(self, "Error", "Please enter a Pokémon name.")

    def display_pokemon_data(self, data):
        name, abilities = data['name'].capitalize(), ', '.join([ability['ability']['name'] for ability in data['abilities']])
        types, stats = ', '.join([ptype['type']['name'] for ptype in data['types']]), ', '.join([f"{stat['stat']['name']}: {stat['base_stat']}" for stat in data['stats']])
        self.info_label.setText(f"Name: {name}\nAbilities: {abilities}\nTypes: {types}\nStats: {stats}")

        image_url = data['sprites']['other']['official-artwork']['front_default']
        self.set_pokemon_image(image_url)
        self.capture_button.setEnabled(True)
        self.current_pokemon = {"name": name, "image_url": image_url}

    def set_pokemon_image(self, image_url):
        response = requests.get(image_url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

    def capture_pokemon(self):
        if hasattr(self, 'current_pokemon'):
            pokemon = self.current_pokemon
            name, image_url = pokemon['name'], pokemon['image_url']
            response = requests.get(image_url)
            if response.status_code == 200:
                os.makedirs("captured_pokemon", exist_ok=True)
                file_path = f"captured_pokemon/{name}.png"
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                self.captured_pokemon.append({"name": name, "file_path": file_path})
                QMessageBox.information(self, "Success", f"{name} captured!")

    def display_captured_pokemon(self):
        if self.captured_pokemon:
            display_window = QWidget()
            display_window.setWindowTitle("Captured Pokémon")
            layout = QVBoxLayout()
            scroll_area = QScrollArea()

            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout()

            for pokemon in self.captured_pokemon:
                name_label, image_label = QLabel(f"Name: {pokemon['name']}"), QLabel()
                pixmap = QPixmap(pokemon['file_path'])
                image_label.setPixmap(pixmap)
                image_label.setFixedSize(150, 150)
                image_label.setScaledContents(True)

                pokemon_layout = QVBoxLayout()
                pokemon_layout.addWidget(name_label)
                pokemon_layout.addWidget(image_label)
                scroll_layout.addLayout(pokemon_layout)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)
            layout.addWidget(scroll_area)
            display_window.setLayout(layout)
            display_window.show()
        else:
            QMessageBox.information(self, "No Pokémon", "No Pokémon captured yet.") 
