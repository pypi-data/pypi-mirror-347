import os

while True: 
    os.system('cls' if os.name == 'nt' else 'clear')
    dice_roll = input('\nRoll a dice: ')
    print("\nResult: ", Dice.roll(dice_roll))
    print("Min and max values possible: ", Dice.get_min_max(dice_roll))
    input()