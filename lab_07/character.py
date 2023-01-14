class Character:
    id = int()
    player_id = int()
    name = str()
    level = int()
    race = str()
    gender = str()
    background = str()
    alignment = str()
    is_alive = bool()

    def __init__(self, id, player_id, name, level, race, gender, background, alignment, is_alive):
        self.id = id
        self.player_id = player_id
        self.name = name
        self.level = level
        self.race = race
        self.gender = gender
        self.background = background
        self.alignment = alignment
        self.is_alive = is_alive

    def __getitem__(self, item):
        return {'id': self.id, 'player_id': self.player_id, 'name': self.name, 'level': self.level,
                'race': self.race, 'gender': self.gender, 'background': self.background,
                'alignment': self.alignment, 'is_alive': self.is_alive}[item]

    def __str__(self):
        return f"{self.id:<4} {self.player_id:<4} {self.name:<15} {self.level:<2} {self.race:<15} " \
               f"{self.gender:<4} {self.background:<30} {self.alignment:<30} {self.is_alive:<5}"

    def dictionary(self):
        return {'id': self.id, 'player_id': self.player_id, 'name': self.name, 'level': self.level,
                'race': self.race, 'gender': self.gender, 'background': self.background,
                'alignment': self.alignment, 'is_alive': self.is_alive}


def create_characters(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        tmp = list()
        for line in file:
            a = line.split(';')
            tmp.append(Character(int(a[0]), int(a[1]), a[2], int(a[3]), a[4], a[5], a[6], a[7], str(bool(a[8]))))
    return tmp
