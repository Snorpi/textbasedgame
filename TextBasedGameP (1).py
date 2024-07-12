# SarahAnn Nagel
import random
import sys

rooms = {
    'Foyer': {'South': 'Bedroom', 'West': 'Kitchen', 'East': 'Garden', 'North': 'Library'},
    'Bedroom': {'North': 'Foyer', 'East': 'Bathroom'},
    'Bathroom': {'West': 'Bedroom'},
    'Kitchen': {'East': 'Foyer'},
    'Garden': {'West': 'Foyer', 'North': 'Crypt'},
    'Crypt': {'South': 'Garden', 'North': 'Library'},
    'Library': {'South': 'Crypt', 'East': 'Attic', 'North': 'Foyer'},
    'Attic': {'West': 'Library'}
}

items = {
    'Garlic': 'Crypt',
    'Silver Bullets': 'Bathroom',
    'Key': 'Bedroom',
    'Flashlight': 'Kitchen',
    'Map': 'Attic'
}

villains = {
    'Werewolf': random.choice(list(rooms.keys())),
    'Vampire': random.choice(list(rooms.keys()))
}


inventory = []


def add_item_to_inventory(found_item):
    inventory.append(found_item)
    print("You found", found_item)
    print("Current inventory:", inventory)

    # Check if player has collected all items and move the Vampire and Werewolf to the player's current room
    def get_current_room():
        global current_room
        return current_room

    if all(item in inventory for item in items.keys()):
        villains["Vampire"] = get_current_room
        villains["Werewolf"] = get_current_room
        print("The Vampire and Werewolf have entered the room!")
        print("The Vampire turns to dust and the Werewolf dies.")
        print("Congratulations! You have found all the items and beat the Supernaturals. You Win!")
        sys.exit()


def move_villains():
    for villain, current_location in villains.items():
        possible_directions = list(rooms[current_location].keys())
        random_direction = random.choice(possible_directions)
        villains[villain] = rooms[current_location][random_direction]


def check_villains():
    for villain, current_location in villains.items():
        print(villain, "is in", current_location)


# Set the initial room
current_room = 'Foyer'

# Gameplay loop
while current_room != 'exit':
    # Display the current room
    print("You are in the", current_room)

    # Prompt the player for a command
    command = input("Enter a command (North, South, East, West, or exit): ")

    # Handle the different commands
    if command == 'exit':
        # Set the current room to 'exit' to end the loop
        current_room = 'exit'

        # Check if player has killed the vampire and werewolf or collected all items
        if ("Garlic" in inventory and villains["Vampire"] not in rooms[current_room].values()) and \
                ("Silver Bullets" in inventory and villains["Werewolf"] not in rooms[current_room].values()) or \
                all(item in inventory for item in items.keys()):
            print("Congratulations! You have won the game.")
        else:
            print("You have lost the game.")
    elif command in ['North', 'South', 'East', 'West']:
        # Check if the direction is valid for the current room
        if command in rooms[current_room]:
            # Move to the new room
            current_room = rooms[current_room][command]
            move_villains()

            # Check if the player has the Map in inventory to see the Vampire and Werewolf locations
            if "Map" in inventory:
                check_villains()

            # Check if the player is trying to enter the Attic without a Flashlight
            if current_room == 'Attic' and 'Flashlight' not in inventory:
                # Check if the player has a Flashlight in their inventory
                if 'Flashlight' not in inventory:
                    print("It is too dark to see anything in the Attic. You need a Flashlight to search for the Map.")
                else:
                    print("You enter the Attic.")
        # Check if the player is trying to enter the Crypt without a Key
        elif current_room == 'Crypt' and 'Key' not in inventory:
            print("You are unable to enter the Crypt without a Key.")
        else:
            # Invalid direction, display an error message
            print("You can't move in that direction. Please try a different direction.")
                    # Check if there is an item in the new room
            if current_room in items.values():
                for item, location in items.items():
                    if location == current_room and item not in inventory:
                        print("Hint: There is a", item, "in the room. Search for it, to add it to your inventory.")
    elif command.startswith('Search for '):
        # Check if the player is searching for an item in the current room
        search_item = command.split('Search for ')[1]
        if search_item in items and items[search_item] == current_room:
            add_item_to_inventory(search_item)
        else:
            print("There is no", search_item, "in this room.")
    elif command == 'Encounter':
        # Check if the player encounters a Vampire or Werewolf in the current room
        if current_room == villains["Vampire"]:
            if "Garlic" in inventory:
                print("The Vampire turns to dust. You have defeated it!")
            else:
                print("The Vampire bites you. You have been turned into a Vampire. Game over.")
                current_room = 'exit'
        elif current_room == villains["Werewolf"]:
            if "Silver Bullets" in inventory:
                print("You shoot the Werewolf with a Silver Bullet. You have defeated it!")
            else:
                print("The Werewolf attacks and eats you. Game over.")
                current_room = 'exit'
        else:
            print("There is no Vampire or Werewolf in this room.")
    else:
        # Invalid command, display an error message
        print("Invalid command. Please try again. Also, hi cutie")
