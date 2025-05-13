from ..models.dice_controller import _DiceController

def roll_dice(dice_str: str) -> int:
    return _DiceController.roll(dice_str)