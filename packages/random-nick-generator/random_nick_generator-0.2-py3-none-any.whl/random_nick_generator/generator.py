import random

class NicknameGenerator:
    def __init__(self):
        self.adjectives = [
            "Swift", "Clever", "Brave", "Mighty", "Sly",
            "Fierce", "Gentle", "Bold", "Wise", "Noble",
            "Cunning", "Loyal", "Fearless", "Playful", "Daring"
        ]
        self.animals = [
            "Tiger", "Eagle", "Wolf", "Dragon", "Shark",
            "Phoenix", "Panther", "Falcon", "Bear", "Leopard",
            "Hawk", "Rhino", "Cheetah", "Fox", "Otter"
        ]
        self.numbers = [str(i) for i in range(1, 100)]

    def generate_nickname(self):
        adjective = random.choice(self.adjectives)
        animal = random.choice(self.animals)
        number = random.choice(self.numbers)
        return f"{adjective}{animal}{number}"

# Функция для генерации ника
def generate():
    generator = NicknameGenerator()
    return generator.generate_nickname()