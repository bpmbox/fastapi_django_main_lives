from dataclasses import dataclass

@dataclass
class Account:
    id: int
    user_id: int
    balance: float

    def __init__(self, id: int, user_id: int, balance: float = 0.0):
        self.id = id
        self.user_id = user_id
        self.balance = balance