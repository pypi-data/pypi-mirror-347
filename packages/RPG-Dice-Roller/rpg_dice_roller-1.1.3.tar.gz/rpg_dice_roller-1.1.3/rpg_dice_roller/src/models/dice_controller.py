import random

from .errors import InvalidDiceNotation
from .dice_input import _DiceInfo

class _DiceController:
    _dice_rolled: int = 0
    
    @classmethod
    def roll(cls, dice_str: str) -> int:
        def simple_roll(max: int) -> int:
            return random.randint(1, max)
        
        cls._dice_rolled += 1
        
        dice_info = _DiceInfo(dice_str)

        # Thow dice for n rolls
        result_sum = 0
        for die in dice_info.get_dice_list():
            for _ in range(die['rolls']):
                result_sum += simple_roll(die['type'])
                
        return result_sum + dice_info.get_bonus()
    
    @staticmethod
    def get_dice_range(dice_str) -> dict:
        dice_info = _DiceInfo(dice_str)
        
        # Sum of rolls + bonus
        min_val = sum([die['rolls'] for die in dice_info.get_dice_list()]) + dice_info.get_bonus()
        # (Sum of rolls * max result) + bonus
        max_max = sum([die['rolls'] * die['type'] for die in dice_info.get_dice_list()]) + dice_info.get_bonus()

        return {
            'min': min_val,
            'max': max_max
        }
        
    @classmethod
    def get_dice_rolled(cls) -> int:
        return cls._dice_rolled