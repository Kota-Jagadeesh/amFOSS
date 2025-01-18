from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication
from PySide6.QtGui import QPixmap
import requests
import os
import sys
import glob

class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokémon Search")
        self.setFixedSize(850, 500)
        self.captured_pokemon = []
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(50, 50, 280, 40)
        self.textbox.setPlaceholderText("Enter Pokémon name")

        self.info_label = QLabel(self)
        self.info_label.setGeometry(350, 50, 450, 200)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(350, 260, 300, 200)
        self.image_label.setScaledContents(True)

        QPushButton("Search", self, clicked=self.fetch_pokemon_data).setGeometry(50, 300, 160, 43)
        self.capture_button = QPushButton("Capture", self, clicked=self.capture_pokemon)
        self.capture_button.setGeometry(50, 350, 160, 43)
        self.capture_button.setEnabled(False)
        QPushButton("Display", self, clicked=self.display_captured_pokemon).setGeometry(50, 400, 160, 43)

    def fetch_pokemon_data(self):
        name = self.textbox.text().strip().lower()
        if name:
            url = f"https://pokeapi.co/api/v2/pokemon/{name}"
            response = requests.get(url)
            if response.status_code == 200:
                self.display_pokemon_data(response.json())
            else:
                QMessageBox.warning(self, "Error", "Pokémon not found.")
        else:
            QMessageBox.warning(self, "Error", "Please enter a Pokémon name.")

    def display_pokemon_data(self, data):
        name = data['name'].capitalize()
        abilities = ', '.join([a['ability']['name'] for a in data['abilities']])
        types = ', '.join([t['type']['name'] for t in data['types']])
        stats = '\n'.join([f"{s['stat']['name']}: {s['base_stat']}" for s in data['stats']])

        self.info_label.setText(f"Name: {name}\nAbilities: {abilities}\nTypes: {types}\nStats:\n{stats}")
        self.set_pokemon_image(data['sprites']['other']['official-artwork']['front_default'])
        self.current_pokemon = {"name": name, "image_url": data['sprites']['other']['official-artwork']['front_default']}
        self.capture_button.setEnabled(True)

    def set_pokemon_image(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.image_label.setPixmap(pixmap)

    def capture_pokemon(self):
        if self.current_pokemon:
            name, url = self.current_pokemon['name'], self.current_pokemon['image_url']
            response = requests.get(url)
            if response.status_code == 200:
                os.makedirs("captured_pokemon", exist_ok=True)
                path = f"captured_pokemon/{name}.png"
                with open(path, 'wb') as file:
                    file.write(response.content)
                self.captured_pokemon.append({"name": name, "file_path": path})
                self.show_success_popup(name)

    def show_success_popup(self, name):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"{name} captured successfully!")
        msg.setWindowTitle("Pokémon Captured")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("font-size: 16px;")
        msg.exec()

    def display_captured_pokemon(self):
        if self.captured_pokemon:
            self.captured_window = CapturedPokemonWindow(self.captured_pokemon)
            self.captured_window.show()
        else:
            QMessageBox.information(self, "No Pokémon", "No Pokémon captured yet.")


class CapturedPokemonWindow(QWidget):
    def __init__(self, captured_pokemon):
        super().__init__()
        self.setWindowTitle("Captured Pokémon")
        self.setFixedSize(850, 500)
        self.captured_pokemon = captured_pokemon

        # Load Pokémon images from the folder
        self.load_all_pokemon()

        self.current_index = 0
        self.image_label = QLabel(self)
        self.image_label.setGeometry(50, 50, 300, 300)
        self.image_label.setScaledContents(True)
        self.info_label = QLabel(self)
        self.info_label.setGeometry(400, 50, 400, 300)
        QPushButton("Previous", self, clicked=self.previous_pokemon).setGeometry(200, 400, 100, 40)
        QPushButton("Next", self, clicked=self.next_pokemon).setGeometry(550, 400, 100, 40)

        # Show the first Pokémon
        if self.captured_pokemon:
            self.show_pokemon(self.current_index)

    def load_all_pokemon(self):
        folder_path = "captured_pokemon"
        if os.path.exists(folder_path):
            # Load all PNG files in the folder
            for file_path in glob.glob(os.path.join(folder_path, "*.png")):
                name = os.path.splitext(os.path.basename(file_path))[0]
                self.captured_pokemon.append({"name": name, "file_path": file_path})

    def show_pokemon(self, index):
        pokemon = self.captured_pokemon[index]
        pixmap = QPixmap(pokemon['file_path'])
        self.image_label.setPixmap(pixmap)
        self.info_label.setText(f"Name: {pokemon['name']}")

    def previous_pokemon(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_pokemon(self.current_index)

    def next_pokemon(self):
        if self.current_index < len(self.captured_pokemon) - 1:
            self.current_index += 1
            self.show_pokemon(self.current_index)

if __name__ == "__main__":
    app = QApplication([])
    window = SearchWindow()
    window.show()
    sys.exit(app.exec())
