class InvalidDiceNotation(Exception):
    """Raised when the input isn't a valid rpg dice format"""
    def __init__(self, value, message="Not a valid dice format"):
        self.value = value
        self.message = message
        super().__init__(self.message)
