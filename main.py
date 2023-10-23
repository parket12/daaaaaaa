import random
import json
import csv
import os

SAVE_FILE = "save_file.json"
CSV_FILE = "game_data.csv"

enemies = ['Математический монстр', 'Грамматический дракон', 'Исторический злодей']

items = {
    'Карандаш': 'Позволяет решать математические головоломки.',
    'Книга': 'Дает знания о грамматике и литературе.',
    'Словарь': 'Помогает разгадать исторические загадки.'
}


def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    else:
        player_name = input("Введите имя игрока: ")
        player_health = 100
        player_items = []
        tasks_completed = 0
        return {
            'player_name': player_name,
            'player_health': player_health,
            'player_items': player_items,
            'tasks_completed': tasks_completed
        }


def save_game(game_state):
    with open(SAVE_FILE, 'w') as f:
        json.dump(game_state, f)


def describe_player(player_name, player_health, player_items):
    print(f"{player_name} (Здоровье: {player_health})")
    print("Имеет следующие предметы:")
    for item in player_items:
        print(f"- {item}: {items[item]}")


def battle_enemy(game_state):
    enemy = random.choice(enemies)
    print(f"Вы встретили {enemy}!")
    enemy_health = random.randint(20, 50)

    while game_state['player_health'] > 0 and enemy_health > 0:
        print(
            f"{game_state['player_name']} (Здоровье: {game_state['player_health']}) против {enemy} (Здоровье: {enemy_health})")
        choice = input("Выберите действие: 1 - Атаковать, 2 - Сбежать: ")
        if choice == '1':
            player_damage = random.randint(10, 20)
            enemy_damage = random.randint(5, 15)
            print(f"Вы нанесли {player_damage} урона {enemy}!")
            print(f"{enemy} нанес {enemy_damage} урона вам!")
            game_state['player_health'] -= enemy_damage
            enemy_health -= player_damage
        elif choice == '2':
            print(f"Вы сбежали от {enemy}!")
            return game_state
    if game_state['player_health'] <= 0:
        print("Вы проиграли в битве. Игра окончена.")
        game_state['game_over'] = True
    else:
        print(f"Вы победили {enemy}!")
        game_state['tasks_completed'] += 1
    return game_state


def collect_item(game_state):
    item = random.choice(list(items.keys()))
    print(f"Вы нашли {item}! {items[item]}")
    game_state['player_items'].append(item)
    return game_state


def end_game(player_name):
    print(f"Поздравляем, {player_name}! Вы успешно завершили задачи в школе и закончили игру.")
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)


def write_to_csv(game_state):
    fieldnames = ["player_name", "player_health", "player_items", "tasks_completed"]
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode='w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
    with open(CSV_FILE, mode='a') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(game_state)


def main():
    game_state = load_game()
    game_over = False

    while not game_over:
        describe_player(game_state['player_name'], game_state['player_health'], game_state['player_items'])
        print("1 - Идти дальше")
        print("2 - Собрать предмет")
        print("3 - Удалить сохраненную игру")
        choice = input("Выберите действие: ")   

        if choice == '1':
            game_state = battle_enemy(game_state)
        elif choice == '2':
            game_state = collect_item(game_state)
        elif choice == '3':
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
                print("Сохраненная игра удалена.")
                return
        write_to_csv(game_state)
        save_game(game_state)


if __name__ == "__main__":
    main()