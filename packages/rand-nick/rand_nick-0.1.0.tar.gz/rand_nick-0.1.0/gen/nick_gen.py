import random

adjectives = [
    "Funny", "Smart", "Swift", "Wise", "Strong",
    "Lunar", "Starry", "Secret", "Bright", "Wild",
    "Brave", "Night", "Sunny", "Creative", "Fierce",
    "Mighty", "Cunning", "Noble", "Fearless", "Charming",
    "Epic", "Legendary", "Mystic", "Savage", "Gentle",
    "Bold", "Daring", "Radiant", "Vibrant", "Eternal",
    "Clever", "Sly", "Playful", "Majestic", 
    'Dazzling', 'Fearsome', 'Gallant', 'Gracious', 
    'Heroic', 'Intrepid', 'Jovial', 'Keen', 
    'Lively', 'Nimble', 'Obsidian', 'Radiant',
            'Serene', 'Tenacious', 'Valiant', 'Zealous'
        ]
nouns = [
    "Lion", "Tiger", "Wolf", "Hawk", "Dragon",
    "Phoenix", "Cat", "Elephant", "Panda", 
    'Crab', 'Lynx', 'Eagle', 'Hare', 'Bear',
    'Kangaroo', 'Shark', 'Falcon', 'Viper',
    'Rhino', 'Gorilla', 'Leopard', 'Cheetah',
    'Owl', 'Whale', 'Turtle', 'Fox',
    'Bison', 'Otter', 'Raven', 
    'Jaguar', 'Griffin', 'Storm', 
    'Knight','Wizard','Sorcerer','Ninja','Samurai',
        ]
numbers = [str(i) for i in range(1, 100)]
special_chars = ["_", "-", "#"]

def generate_nickname():
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    number = random.choice(numbers)
    special_char = random.choice(special_chars)

    format_choice = random.choice([
        f"{adjective}{noun}{number}",
        f"{adjective}{special_char}{noun}{number}",
        f"{noun}{special_char}{adjective}{number}",
        f"{number}{special_char}{adjective}{noun}",
    ])
    
    return format_choice