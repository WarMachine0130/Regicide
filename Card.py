class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.filePath =  f"assets\Playing Cards\card-{suit}-{rank}.png"
