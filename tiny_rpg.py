import random
import json
from colorama import init, Fore, Style

init(autoreset=True)

# -------------------- Game Data -------------------- #
player = {
    'name': 'Hero',
    'level': 1,
    'xp': 0,
    'hp': 100,
    'max_hp': 100,
    'attack': 10,
    'gold': 50,
    'inventory': [],
    'skills': [],
    'potions': 1,
    'quests': [],
    'location': 'village'
}

monsters = [
    {'name': 'Slime', 'hp': 30, 'attack': 5, 'xp': 10, 'gold': 5},
    {'name': 'Goblin', 'hp': 50, 'attack': 8, 'xp': 20, 'gold': 10},
    {'name': 'Orc', 'hp': 80, 'attack': 12, 'xp': 30, 'gold': 15},
    {'name': 'Dark Knight', 'hp': 120, 'attack': 18, 'xp': 50, 'gold': 30},
    {'name': 'Dragon', 'hp': 200, 'attack': 25, 'xp': 100, 'gold': 50},
    {'name': 'Demon Lord', 'hp': 300, 'attack': 35, 'xp': 200, 'gold': 100}
]

shop_items = [
    {'name': 'Potion', 'price': 10, 'effect': 'heal'},
    {'name': 'Sword Upgrade', 'price': 30, 'effect': 'attack'},
    {'name': 'Armor Upgrade', 'price': 30, 'effect': 'hp'},
    {'name': 'Magic Scroll', 'price': 40, 'effect': 'fireball'},
    {'name': 'XP Boost', 'price': 50, 'effect': 'xp'},
    {'name': 'Revive Stone', 'price': 100, 'effect': 'revive'}
]

# -------------------- Game Functions -------------------- #
def battle(monster):
    print(Fore.RED + f"A wild {monster['name']} appears!")
    while monster['hp'] > 0 and player['hp'] > 0:
        action = input("(A)ttack or (R)un: ").lower()
        if action == 'a':
            dmg = random.randint(player['attack'] - 2, player['attack'] + 2)
            monster['hp'] -= dmg
            print(f"You dealt {dmg} damage to the {monster['name']}")
            if monster['hp'] <= 0:
                print(Fore.GREEN + f"You defeated the {monster['name']}!")
                player['xp'] += monster['xp']
                player['gold'] += monster['gold']
                level_up()
                loot_drop()
                break
            mdmg = random.randint(monster['attack'] - 2, monster['attack'] + 2)
            player['hp'] -= mdmg
            print(Fore.RED + f"The {monster['name']} hit you for {mdmg} damage.")
        elif action == 'r':
            print("You ran away!")
            break
        else:
            print("Invalid input.")
        if player['hp'] <= 0:
            print(Fore.RED + "You died...")
            if 'Revive Stone' in player['inventory']:
                print(Fore.YELLOW + "Your Revive Stone saved you!")
                player['inventory'].remove('Revive Stone')
                player['hp'] = player['max_hp'] // 2
            else:
                exit()

def loot_drop():
    chance = random.randint(1, 100)
    if chance > 75:
        item = random.choice(['Potion', 'Magic Scroll'])
        player['inventory'].append(item)
        print(Fore.MAGENTA + f"You found a {item}!")

def level_up():
    needed = player['level'] * 50
    if player['xp'] >= needed:
        player['level'] += 1
        player['xp'] -= needed
        player['max_hp'] += 20
        player['attack'] += 5
        print(Fore.CYAN + f"Level up! You are now level {player['level']}!")


def shop():
    print(Fore.YELLOW + "Welcome to the shop!")
    for i, item in enumerate(shop_items):
        print(f"{i+1}. {item['name']} - {item['price']} gold")
    choice = input("Buy item number or (E)xit: ").lower()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(shop_items):
            item = shop_items[idx]
            if player['gold'] >= item['price']:
                player['gold'] -= item['price']
                if item['effect'] == 'heal':
                    player['potions'] += 1
                elif item['effect'] == 'attack':
                    player['attack'] += 5
                elif item['effect'] == 'hp':
                    player['max_hp'] += 20
                elif item['effect'] == 'xp':
                    player['xp'] += 50
                    level_up()
                elif item['effect'] == 'revive':
                    player['inventory'].append('Revive Stone')
                elif item['effect'] == 'fireball':
                    player['skills'].append('Fireball')
                print(Fore.GREEN + f"Bought {item['name']}!")
            else:
                print("Not enough gold!")
    else:
        print("Leaving the shop.")


def dungeon():
    floor = 1
    print(Fore.BLUE + "You enter the dark dungeon...")
    while True:
        print(f"--- Floor {floor} ---")
        if floor % 5 == 0:
            print(Fore.MAGENTA + f"Boss Fight on Floor {floor}!")
            monster = monsters[min(floor // 5 + 2, len(monsters) - 1)].copy()
        else:
            monster = random.choice(monsters[:min(floor // 3 + 2, len(monsters))]).copy()
        monster['hp'] += floor * 5
        monster['attack'] += floor // 2
        battle(monster)
        if player['hp'] <= 0:
            break
        loot_drop()
        cont = input("Descend to next floor? (Y/N): ").lower()
        if cont != 'y':
            print(Fore.CYAN + f"You escaped the dungeon at Floor {floor} with {player['gold']} gold.")
            break
        floor += 1


def status():
    print(Fore.CYAN + f"Name: {player['name']} | Level: {player['level']} | HP: {player['hp']}/{player['max_hp']} | Attack: {player['attack']} | Gold: {player['gold']} | XP: {player['xp']}")
    print("Inventory:", player['inventory'])
    print("Skills:", player['skills'])

def main():
    print(Fore.YELLOW + "Welcome to Tiny RPG!")
    while True:
        print("\n(V)enture | (S)tatus | (Sh)op | (D)ungeon | (Q)uit")
        choice = input("Action: ").lower()
        if choice == 'v':
            battle(random.choice(monsters[:3]).copy())
        elif choice == 's':
            status()
        elif choice == 'sh':
            shop()
        elif choice == 'd':
            dungeon()
        elif choice == 'q':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
