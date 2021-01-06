#  IMPORTS:
import time
import random

#  GLOBAL VARIABLES:
#  Dictionary of All Enemies and their Status in Battle:
enemies_status = {
    'Goblin': {'damage_range': (3, 7), 'health_range': (10, 20), 'reward': 5},
    'Pirate': {'damage_range': (6, 10), 'health_range': (20, 25), 'reward': 8},
    'Troll': {'damage_range': (4, 8), 'health_range': (15, 25), 'reward': 7},
    'Wolf': {'damage_range': (3, 6), 'health_range': (10, 15), 'reward': 3},
    'Malicious Wizard': {
        'damage_range': (6, 13),
        'health_range': (30, 40),
        'reward': 10
        },
    'Great Red Dragon': {
        'damage_range': (3, 18),
        'health_range': (40, 50),
        'reward': 20
        }
    }
# List of enemies to randomly pick in wider cave path:
enemies = ["Goblin", "Pirate", "Troll", "Wolf", "Malicious Wizard"]
# Dictionary with more detailed spell description so player understands usage:
spell_info = {
    'Magic Frost': ["Name: Magic Frost"
                    "\nAverage Damage: 4"
                    "\nIn-Combat: Strikes the enemy with"
                    " ice and causes it to move slower"
                    "\nOut-of-Combat: Cools stuff down.", 4],
    'Aerial Cut': ["Name: Aerial Cut"
                   "\nAverage Damage: 6"
                   "\nIn-Combat: Unleashes a powerful, air pressure strike."
                   "\nOut-of-Combat: Blows stuff out of the way.", 6],
    'Inferno': ["Name: Inferno"
                "\nAverage Damage: 9"
                "\nIn-Combat: Attacks foe with the full"
                " force of a hellish fiery inferno."
                "\nOut-of-Combat: Burns stuff.", 9]
    }


# FUNCTIONS:
# 1 Second Print Delay:
def print_delay(string=""):
    if string != "":
        print(string)
    time.sleep(1.7)


# BEGINNING & END:
# Game Intro:
def intro():
    print_delay("You are a young aspiring wizard on your way to"
                " your very first wizard mentor's house!")
    print_delay("Following your old, half torn map, you find your way"
                " to the mentor's village.")
    print_delay("To your disappointment, the markings on your map"
                " are no more specific than the street they indicate.")
    print_delay("You head towards that street, beginning your adventure.")
    print_delay("Since you have not received your Magic Staff yet,"
                " you are armed only with a small dagger that"
                " can deal between 1 and 3 damage points.")


# Game Over:
def game_over(status):
    if status == "loss":
        print_delay("Unfortunately, you have lost the game.\n")
    elif status == "victory":
        print_delay("\n\nCongratulations! You won the game!!! :)\n")
    response = input("Would you like to start a new game?\n(y/n): ")
    if response.lower() == "y":
        print_delay("\n\nNew Game!\n\n")
        main()
    elif response.lower() == "n":
        print_delay("\n\nGoodbye and thank you for playing!")
        quit()
    else:
        print_delay("\nPlease use either 'y' or 'n' as you response.\n")
        game_over(status)


# OWNED ITEMS:
# Show Inventory:
def get_inventory(variables):
    spells = variables['spells']
    inventory = variables["inventory"]
    player_health = variables['player_health']
    inv = '\n'.join(sorted([i for i in inventory]))
    spl = '\n'.join(sorted([i for i in spells]))
    print_delay()
    print(f"\n\nYour maximum health is: {player_health}\n"
          f"\nYour inventory contains the following items:\n{inv}\n")
    if len(spells) >= 1:
        print(f"\nThe magic spells you know are:\n{spl}\n")
        print("You can obtain detailed information about each of your"
              " spells at any moment by entering the letter 's'.\n")


# Show Spell Details:
def get_spells(variables):
    spells = variables['spells']
    if len(spells) >= 1:
        print_delay()
        print("Spell Information:\n")
        for i in spells:
            print(f"{spell_info[i][0]}\n")
    else:
        print_delay("Oops! It doesn't look like you know any"
                    " spells at the moment. Please try again "
                    "once you have learned some.")


# Get Inventory or Detailed Spell Info:
def item_info(variables, response):
    if response.lower() == "i":
        get_inventory(variables)  # Defined Line: 85
    elif response.lower() == "s":
        get_spells(variables)  # Defined Line: 101
    else:
        print_delay("\nSorry, I didn't quite catch that.\n")


# Checks if Player has a Magic Staff to Perform Spells:
def check_staff(variables, spell):
    inventory = variables['inventory']
    if "Magic Staff" not in inventory and spell == "obtained":
        print_delay("Even though you can memorize the spells, you can"
                    " unfortunately not cast them without a Magic Staff.")
        print_delay("You need to find one before you can use"
                    " your spells in battle or on objects!")
    elif "Magic Staff" in inventory and spell == "obtained":
        print_delay("Since you have a Magic Staff, you will now"
                    " be able to cast this spell.")


# Combat with Enemies:
def combat(enemy, variables):
    spells = variables['spells']
    unlocked = variables["unlocked"]
    # Player Attacks:
    player_health2 = variables['player_health']
    player_attacks = {}
    player_attacks[0] = "Dagger"
    if "Magic Staff" in variables['inventory']:
        player_attacks.update(
            {k + 1: spells[k] for k in range(len(spells))}
            )
    attack_choices = '\n'.join(
        [f'{k}. {v}' for k, v in player_attacks.items()]
        )
    # Enemy Status:
    enemy_health = random.randint(
        enemies_status[enemy]['health_range'][0],
        enemies_status[enemy]['health_range'][1])
    damage_range = enemies_status[enemy]['damage_range']
    reward = enemies_status[enemy]['reward']
    # Who Gets to Attack First:
    first_attack = random.choice(['player', 'enemy'])

    # Enemy Attack Routine:
    def enemy_attack(player_health2):
        print_delay(f"{enemy}'s turn!")
        enemy_damage = random.randint(damage_range[0], damage_range[1])
        player_health2 -= enemy_damage
        print_delay(f"{enemy} damaged your health by {enemy_damage} points.")
        return player_health2

    # Player Attack Routine:
    def player_attack(enemy_health):
        player_damage = 0
        response = input(f"\nYour turn! How do you want to attack?\n"
                         f"{attack_choices}\n")
        if response == "0":   # Dagger
            player_damage = random.randint(1, 3)
        elif response in [str(i) for i in player_attacks]:  # Spell
            player_damage = spell_info[player_attacks[int(response)]][1]
            player_damage = random.randint(player_damage-2, player_damage+3)
        else:  # Checks if input is valid:
            print_delay("Oops! The response you gave doesn't seem to"
                        " match any available option.\n"
                        "Please note that checking your inventory"
                        " or spells is unavailable during combat!")
            return player_attack(enemy_health)
        enemy_health -= player_damage
        print_delay(f"\nYou attacked {enemy} with your"
                    f" {player_attacks[int(response)]}!")
        print_delay(f"It did a total damage of {player_damage}.")
        return enemy_health

    # Loop Until Someone Loses:
    print_delay(f"{enemy}'s Health: {enemy_health}\n"
                f"Your Health: {player_health2}\n")
    for i in range(50):
        if i % 2 == 0:
            if first_attack == "player":
                enemy_health = player_attack(enemy_health)
            else:
                player_health2 = enemy_attack(player_health2)
        if i % 2 == 1:
            if first_attack == "player":
                player_health2 = enemy_attack(player_health2)
            else:
                enemy_health = player_attack(enemy_health)
        print_delay(f"{enemy}'s Health: {enemy_health}\n"
                    f"Your Health: {player_health2}\n")
        # Victory/Loss:
        if enemy_health <= 0:
            print_delay(f"Congratulations!"
                        f" You won the fight against the {enemy}!")
            unlocked.append(enemy)
            variables['player_health'] += reward
            print_delay(f"Your maxmum health has been upgraded"
                        f" to {variables['player_health']}.\n")
            break
        elif player_health2 <= 0:
            game_over("loss")  # Defined Line: 69


# MAIN LOCATIONS:
# Old Abandoned House (1):
def old_house(variables):
    spells = variables['spells']
    unlocked = variables["unlocked"]
    inventory = variables["inventory"]
    # Options:
    response = input("\nWhat would you like to do next?\n"
                     "1. Open the old chest.\n"
                     "2. Pet the black cat.\n"
                     "3. Investigate broken furniture.\n"
                     "4. Exit old house.\n"
                     "(Enter the number of your choice. Alternatively,"
                     " enter 'i' to view your health & inventory, or 's'"
                     " to view detailed info on your spells.)\n")
    if response == "1":  # 1. Open the old chest.
        print_delay("\nYou go to open the old chest.")
        print_delay("It appears that it is worn by time and"
                    " so you pry it open with ease.\n")
        if 'Magic Frost' in spells:
            print_delay("The chest appears to be empty at the moment.")
        else:
            print_delay("Upon opening the chest, you spot"
                        " a folded, half-torn scroll.\n")
            print_delay("You straighten it and read it;"
                        " It is a magic spell scroll!")
            print_delay("It appears to contain the instructions on"
                        " performing a magic spell called 'Magic Frost!'\n")
            spells.append("Magic Frost")
            check_staff(variables, "obtained")  # Defined Line: 125
    elif response == "2":  # 2. Pet the black cat.
        print_delay("\nYou approach the black cat, which is sitting"
                    " by the window, staring back at you.")
        print_delay("As you get closer, however, the cat gets scared"
                    " and backs off.")
        if "Raw Meat" in inventory:
            print_delay("You take the raw meat you found out of your bag"
                        " and show it to the cat.")
            print_delay("The cat immediately approaches to eat,"
                        " no longer fearful.")
            print_delay("You move closer to pet it, and"
                        " shortly enough it starts purring!")
            print_delay("Looks like you made a new friend.")
            inventory.remove("Raw Meat")
            unlocked.append("Black Cat")
        else:
            print_delay("Perhaps if you had some food to give it,"
                        " you could befriend it.")
    elif response == "3":  # 3. Investigate broken furniture.
        print_delay("\nYou take your time looking around"
                    " the abandoned house, investigating the"
                    " broken furniture and the old belongings.")
        print_delay("Your eyes stumble upon a dirty wizard"
                    " robe, and some books on wizardry.")
        print_delay("This must have been the house of a"
                    " wizard at some point in time.")
    elif response == "4":  # 4. Exit old house.
        print_delay("\nYou decide to leave the old house for now,"
                    " and exit through the door.\n")
        main_location(variables)
    else:  # i. Show inventory, s. Show detailed spell info.
        item_info(variables, response)  # Defined Line: 115
    old_house(variables)  # Defined Line: 609


# Two Floor Mansion (2):
def mansion(variables):
    unlocked = variables["unlocked"]
    spells = variables["spells"]
    inventory = variables["inventory"]
    if "Servant" not in unlocked:
        print_delay("A few moments later, a man in"
                    " servant attire opens the door.")
        print_delay("You decide to ask him if he knows"
                    " where your mentor might be.")
        print_delay("He tells you that this is his house!"
                    " However, he hasn't been"
                    " back for over a day, which is unusual of him,"
                    " especially when expecting guests.")
        print_delay("The last thing the servant knew of him,"
                    " was that he had left for the woods"
                    " to gather some herbs.")
        print_delay("He then asks you if you have seen or heard anything"
                    " that could have to do with his master"
                    " and could help in locating him.\n")
        unlocked.append("Servant")
    elif "Servant" in unlocked:
        print_delay("The same servant rushes to open the"
                    " door and greets you.")
        print_delay("'Did you find anything out"
                    " from your visit to the woods?', he asks eagerly.\n")
    if "Woodcutter" in unlocked and "Magic Staff" not in inventory:
        print_delay("You tell him about your observations"
                    " and what the woodcutter said.")
        print_delay("The servant is visibly concerned."
                    " He mumbles something about the cave"
                    " being safe for no one.\n")
        print_delay("He then asks you to investigate further.")
        print_delay("'Please take this Magic Staff to be safe,"
                    " and see if there's anything else"
                    " to be found in the woods.'\n")
        inventory.append("Magic Staff")
        print_delay("You received the reward Magic Staff!"
                    " Now you can cast spells!\n")
    if "Ripped Wizard Robe" not in inventory:
        print_delay("\nHe continues:")
        print_delay("'In particular, please, go further into"
                    " the path towards the cave and see if there's"
                    " anything else you can find out. If you uncover"
                    " another clue, I will give you one of my master's"
                    " spell scrolls as a reward.\n")
    elif ("Ripped Wizard Robe" in inventory
          and "Ripped Wizard Robe" not in unlocked):
        print_delay("\nYou take the torn wizard robe and"
                    " show it to the servant.")
        print_delay("He immediately recognizes it as his master's.")
        print_delay("He tells you to investigate the cave more,"
                    " but with the utmost caution.")
        print_delay("\nThe servant gives you a magic"
                    " spell scroll as a reward!")
        print_delay("This one is called 'Aerial Cut'!\n")
        spells.append("Aerial Cut")
        check_staff(variables, "obtained")  # Defined Line: 125
        unlocked.append("Ripped Wizard Robe")
        if "Woodcutter" not in unlocked:
            print_delay("\n'I'm sure you can find out more in the"
                        " woods', he says.")
            print_delay("'Get back at me with some new info and I'll"
                        " reward you with your very own Magic Staff.'\n")
    else:
        print_delay("'Unfortunately not, didn't have the"
                    " time to investigate yet',"
                    " you say with shame.")
        print_delay("The servant then politely asks you"
                    " to go around the woods"
                    " in case you can uncover any clue or ask others"
                    " if they have seen him.")
        print_delay("'Talk to the bearded woodcutter living in a"
                    " cabin in the forest, maybe he saw something',"
                    " he said, 'and when you're back, I'll give you the"
                    " Magic Staff my master left for you'. ")
        print_delay("You tell him you'll do your best, and leave.\n")
    main_location(variables)  # Defined Line: 609


# FOREST:
# Woodcutter Cabin | Forest:
def forest_cabin(variables):
    unlocked = variables["unlocked"]
    inventory = variables["inventory"]
    print_delay("You walk towards the wooden cabin.")
    if "Woodcutter" not in unlocked:
        print_delay("As you get closer, you start to make out the"
                    " figure of a middle-aged bearded man sitting"
                    " at a table outside near a campfire.")
        print_delay("On the wooden table before him"
                    " lays the carcass of a pig.")
        print_delay("You ask him if he has seen your mentor nearby"
                    " recently, to which he says that he has in fact"
                    " spotted him the other day while cutting wood,"
                    " and it seemed as if he was in a big hurry. ")
        print_delay("You thank the woodcutter for his help, and he offers"
                    " you a piece of raw pig meat as a visitor's gift.\n")
        inventory.append("Raw Meat")
        unlocked.append("Woodcutter")
    else:
        print_delay("You spot the woodcutter, but he appears to"
                    " be busy with cutting wood, so you decide"
                    " not to disturb him.\n")
    forest(variables)  # Defined Line: 576


# Pond | Forest:
def forest_pond(variables):
    spells = variables['spells']
    unlocked = variables["unlocked"]
    inventory = variables["inventory"]
    if "Goblin" not in unlocked:
        print_delay("As you come closer to its waters, you notice"
                    " a hostile looking goblin a few meters away.")
        print_delay("It appears to be guarding a treasure chest.\n")
        # Options:
        response = input("What would you like to do?\n1. Fight it! "
                         " Then loot the treassure chest.\n"
                         "2. Don't fight it yet! It looks pretty tough."
                         " Maybe it'd be better to come back"
                         " better prepared.\n(Enter the number of your"
                         " choice. Alternatively, enter 'i' to view your"
                         " health & inventory, or 's' to view detailed"
                         " info on your spells.)\n")
        if response == "1":  # 1. Fight it!
            print_delay("\nYou march towards the Goblin ready for fight!\n")
            combat("Goblin", variables)  # Defined Line: 138
        elif response == "2":  # 2. Don't fight it yet!
            print_delay("\nYou decide to come back later and"
                        " better prepared for the fight.")
            forest(variables)  # Defined Line: 576
        else:  # i. Show inventory, s. Show detailed spell info.
            item_info(variables, response)  # Defined Line: 115
    else:
        print_delay("\nYour eyes gaze at the tranquil surface of the "
                    "water before turning to the treasure chest still"
                    " standing on the land by it, right where"
                    " you defeated the evil goblin.\n")
        # Options:
        response = input("What would you like to do now?\n"
                         "1. Open the treassure chest.\n"
                         "2. Leave.\n(Enter the number of your choice."
                         " Alternatively, enter 'i' to view your inventory,"
                         " or 's' to view detailed info on your spells.)\n")
        if response == "1":  # 1. Open the treassure chest.
            if "Chest Key" in inventory and 'Inferno' not in spells:
                print_delay("You take out the strange key you found"
                            " and test it on the chest's lock.")
                print_delay("It fits! Now the treasure chest is opened.")
                print_delay("Inside, is another magic spell scroll!")
                print_delay("This one is called 'Inferno'.")
                spells.append("Inferno")
                check_staff(variables, "obtained")  # Defined Line: 125
            elif "Chest Key" in inventory and 'Inferno' in spells:
                print_delay("You open the chest again,"
                            " but it's empty this time.")
            else:
                print_delay("\nYou try to open the chest,"
                            " but it appears to be well locked.")
        elif response == "2":  # 2. Leave.
            print_delay("\nYou head back to the forest crosspaths.")
            forest(variables)  # Defined Line: 576
        else:  # i. Show inventory, s. Show detailed spell info.
            item_info(variables, response)  # Defined Line: 115
    forest_pond(variables)


# Narrow Path | Cave | Forest:
def cave_narrow_path(variables):
    inventory = variables["inventory"]
    print_delay("\nYou decide to follow the narrow and dark pathway.")
    print_delay("The more you walk, the more it sounds"
                " like someone is there.")
    print_delay("As you reach an opening to a large section of the cave,"
                " your suspicion is confirmed: Someone is here!\n")
    enemy = random.choice(enemies)
    print_delay(f"To the back of the open cave space, you see a {enemy}!")
    print_delay("Behind the new enemy is a particularly wide"
                " and short stone that resembles a makeshift table."
                " There appears to be something on top of it.\n")
    # Options:
    response = input("What would you like to do?\n"
                     "1. Fight and then investigate the rock!\n"
                     "2. Maybe some other time, leave for now.\n"
                     "(Enter the number of your choice. Alternatively,"
                     " enter 'i' to view your health & inventory, or 's'"
                     " to view detailed info on your spells.)\n")
    if response == "1":  # 1. Fight and then investigate the rock!
        combat(enemy, variables)  # Defined Line: 138
        print_delay("You walk towards the table-like rock.")
        if "Chest Key" not in inventory:
            print_delay("Upon closer inspection, you see a strange"
                        " key resting on it!")
            print_delay("You put it in your inventory - you never know!")
            inventory.append("Chest Key")
        else:
            print_delay("Sadly, turns out there's nothing of value here.")
    elif response == "2":  # 2. Maybe some other time, leave for now.
        print_delay("You decide to leave this pathway for now.")
        forest_cave(variables)  # Defined Line: 540
    else:  # i. Show inventory, s. Show detailed spell info.
        item_info(variables, response)  # Defined Line: 115
        cave_narrow_path(variables)


# Wider Path | Cave | Forest:
def cave_wider_path(variables):
    print_delay("\nYou follow the wider path.")
    print_delay("It however becomes narrower and narrower"
                " the more you move along.")
    print_delay("Suddenly, you reach a closed door. It's red and metallic,"
                " complementing the stone orange-y walls"
                " of the cave in a rather ominous way.")
    print_delay("\nYou realize that there is an engraved"
                " message on the door:")
    print_delay("Here lies the Great Red Dragon,\n"
                "The cruelest of them all.\n"
                "This is an entrance to death itself for the naive ones.\n"
                "Enter only if you are prepared for Hell and back.")
    print_delay("\nIt sounds like whatever's behind that door will be")
    print_delay(" tough to beat. And as you contemplate that, you hear a"
                " roar and a man crying for help on the other side.\n")
    # Options:
    response = input("What do you want to do?\n1. Enter. Bring it on!\n"
                     "2. Perhaps not now.. This seems like a whole"
                     " other level of challenge.\nBest to prepare"
                     " a little better and make sure I"
                     " have the best equipment available."
                     "(Enter the number of your choice. Alternatively,"
                     " enter 'i' to view your health & inventory, or 's'"
                     " to view detailed info on your spells.)\n")
    if response == "1":  # 1. Enter. Bring it on!
        print_delay("\nYou open the door and are immediately"
                    " met with a view from Hell:")
        print_delay("Everywhere around, the room you entered has burning"
                    " fires, and at the center lay a huge red dragon.")
        print_delay("The next thing you notice is the man chained up"
                    " behind the dragon-that's your mentor!")
        print_delay("There is not enough time to think"
                    "-the dragon noticed you!\n")
        combat("Great Red Dragon", variables)  # Defined Line: 138
        print_delay("After an excruciating and exhausting battle,")
        print_delay(" you finally won!You now run to your mentor,"
                    " untying him.")
        print_delay("He explains that he was abducted by a rival"
                    " wizard and left there to die, with his"
                    " Magic Staff broken, completely defendless.")
        print_delay("You help him out and the both of you head to his"
                    " mansion for the beginning of your mentorship!")
        game_over("victory")  # Defined Line: 69
    elif response == "2":  # 2. Perhaps not now..
        print_delay("You decide to go back.")
        forest_cave(variables)
    else:  # i. Show inventory, s. Show detailed spell info.
        item_info(variables, response)  # Defined Line: 115
        cave_wider_path(variables)


# Cave | Forest:
def forest_cave(variables):
    unlocked = variables["unlocked"]
    inventory = variables["inventory"]
    if "Ripped Wizard Robe" not in inventory:
        print_delay("As you walk inside the large, cool cave,"
                    " suddenly something catches your attention.")
        print_delay("It's a torn, wizard robe, laying on the floor."
                    " You pick it up and take it with you.")
        inventory.append("Ripped Wizard Robe")
        if "Servant" in unlocked:
            print_delay("This must be another clue to get back"
                        " to the mentor's servant with!")
    else:
        print_delay("Inside the cave, you see two pathways. One is narrow"
                    " and dark, and the other is wide with rough edges.\n")
        # Options:
        response = input("Where would you like to go now?\n"
                         "1. Follow the narrow and dark pathway.\n"
                         "2. Follow the wide and rough pathway.\n"
                         "3. Leave the cave.\n(Enter the number of your"
                         " choice. Alternatively, enter 'i' to view"
                         " your health & inventory, or 's' to view"
                         " detailed info on your spells.)\n")
        if response == "1":  # 1. Follow the narrow and dark pathway.
            cave_narrow_path(variables)  # Defined Line: 449
        elif response == "2":  # 2. Follow the wide and rough pathway.
            cave_wider_path(variables)  # Defined Line: 487
        elif response == "3":  # 3. Leave the cave.
            print_delay("\nYou decide to leave the cave.\n")
            forest(variables)  # Defined Line: 576
        else:  # i. Show inventory, s. Show detailed spell info.
            item_info(variables, response)  # Defined Line: 115
    forest_cave(variables)


# Forest (3):
def forest(variables):
    print_delay("After some time walking, you reach a crossroad.\n")
    # Options:
    response = input("Where would you like to go next?\n"
                     "1. Path towards a cabin, to the left.\n"
                     "2. Path towards the pond, to the right.\n"
                     "3. Path to the cave, straight ahead.\n"
                     "4. Leave the forest and get back to the central"
                     " street.\n(Enter the number of your choice."
                     " Alternatively, enter 'i' to view your health &"
                     " inventory, or 's' to view detailed"
                     " info on your spells.)\n")
    if response == "1":  # 1. Path towards a cabin, to the left.
        forest_cabin(variables)  # Defined Line: 362
    elif response == "2":  # 2. Path towards the pond, to the right.
        print_delay("\nYou slowly make your way to the misty,"
                    " peaceful pond.\n")
        forest_pond(variables)  # Defined Line: 388
    elif response == "3":  # 3. Path to the cave, straight ahead.
        print_delay("\nYou continue the path until a large,"
                    " cold grey cave lies in front of you. It is"
                    " pitch black, but thankfully you find a torch"
                    " by the entrance to help you see.")
        forest_cave(variables)  # Defined Line: 540
    elif response == "4":  # 4. Leave the forest.
        print_delay("\nYou decide to leave the forest for now.\n")
        main_location(variables)  # Defined Line: 609
    else:  # i. Show inventory, s. Show detailed spell info.
        item_info(variables, response)  # Defined Line: 115
        forest(variables)


# Central Street Location - Get Next Move from Player:
def main_location(variables):
    print_delay("You are now at the map-indicated street.\n")
    # Options:
    response = input("Where would you like to go next?\n"
                     "1. Old abandoned house to your left.\n"
                     "2. Two floor mansion in front of you.\n"
                     "3. Path towards the forest to your right.\n"
                     "(Enter the number of your choice. Alternatively,"
                     " enter 'i' to view your health & inventory, or 's'"
                     " to view detailed info on your spells.)\n")
    if response == "1":  # 1. Old abandoned house to your left.
        print_delay("\nYou walk towards the old abandoned house.")
        print_delay("You go to knock on the door,"
                    " but it simply opens as you touch it.")
        print_delay("Inside, you find mostly broken furniture,"
                    " an old chest and a black cat.")
        old_house(variables)  # Defined Line: 222
    elif response == "2":  # 2. Two floor mansion in front of you.
        print_delay("\nYou move towards the beautiful mansion.")
        print_delay("The door appears to be locked, so you knock.\n")
        mansion(variables)  # Defined Line: 286
    elif response == "3":  # 3. Path towards the forest to your right.
        print_delay("\nYou take the path to the forest.")
        print_delay("The path is very long, overshadowed by the beautiful"
                    " vibrant green trees to its left and right side.")
        forest(variables)  # Defined Line: 576
    else:  # i. Show inventory, s. Show detailed spell info.
        item_info(variables, response)  # Defined Line: 115
    main_location(variables)


# MAIN:
def main():
    # Resetting Variable Values for New Games:
    variables = {'player_health': 15,
                 'inventory': ["Dagger"],
                 'spells': [],
                 'unlocked': []}
    # Functions:
    intro()  # Defined Line: 55
    main_location(variables)


main()
