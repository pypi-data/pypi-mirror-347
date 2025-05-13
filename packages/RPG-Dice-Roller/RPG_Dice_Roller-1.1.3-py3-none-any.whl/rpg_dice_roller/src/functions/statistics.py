from ..models.dice_controller import _DiceController

def get_dice_range(dice_str: str) -> int:
    return _DiceController.get_dice_range(dice_str)

def get_dice_rolled() -> int:
    return _DiceController.get_dice_rolled()