from random import random, choice, randint

alignments = ["Хаотично-злой", "Хаотично-нейтральный", "Хаотично-добрый",
              "Нейтрально-злой", "Истинно-нейтральный", "Нейтрально-добрый",
              "Законопослушный-злой", "Законопослушный-нейтральный", "Законопослушный-добрый"
              ]

backgrounds = ["Артист",
               "Беспризорник",
               "Благородный",
               "Гильдейский ремесленник",
               "Моряк",
               "Мудрец",
               "Народный герой",
               "Отшельник",
               "Преступник",
               "Прислужник",
               "Солдат",
               "Чужеземец",
               "Шарлатан"
               ]


class Race:
    tag = "race"
    male_names = []
    female_names = []

    def __init__(self, tag: str, male_names: list, female_names: list):
        self.tag = tag
        self.male_names = male_names
        self.female_names = female_names


human = Race("Человек",
             ["Айвор", "Алвор", "Грегор", "Бран", "Рауль", "Салазар", "Диего", "Рендал", "Нед", "Эддард", "Эйст",
              "Чен", "Джон", "Сэм", "Патрик", "Ричард", "Артур", "Кевин", "Дуэйн", "Брайан", "Пол", "Мет"],
             ["Натали", "Арья", "Люси", "Мара", "Тана", "Марта", "Арвин", "Мей", "Лея", "Тереза",
              "Грейс", "Мишель", "Робин", "Абигейл", "Стана", "Гвен"]
             )

elf = Race("Эльф",
           ["Адран", "Араннис", "Ауст", "Берриан", "Варрис", "Иммераль", "Леон", "Миндартис", "Митрандир", "Перен",
            "Риаррдон", "Теон", "Тауриллион", "Тиррион", "Эниллиас", "Эрдан"],
           ["Бетриана", "Андрасте", "Квиласи", "Дени", "Лара", "Нисса", "Эовин", "Виенна", "Торувьель",
            "Францеска", "Ида", "Итлина", "Сабрина", "Цинтия", "Калантэ"]
           )

dwarf = Race("Дварф",
             ["Рюрик", "Вульфрик", "Адрик", "Баренд", "Гимли", "Димли", "Глоен", "Дурин", "Дорин", "Траин", "Торин"],
             ["Аврора", "Кейра", "Бардин", "Рисвин", "Трис", "Клара", "Марти", "Номи", "Кристид", "Берта", "Эмбер"]
             )

gnome = Race("Гном",
             ["Алвин", "Брок", "Брук", "Глим", "Глен", "Гимбл", "Димбл", "Элдон", "Эрки"],
             ["Августина", "Карлин", "Лилли", "Никс", "Тонкс", "Тана", "Элла", "Токи"]
             )

dragonborn = Race("Дроконорожденный",
                  ["Довакин", "Арч", "Дебиан", "Товальдс"],
                  ["Убунту", "Федора", "Монжара", "Расби", "Гну", ]
                  )

tiefling = Race("Тифлинг",
                ["Гирцин", "Малакат", "Мерунес", "Шео", "Клавикус", "Периайт", "Хермиус", "Сангвин"],
                ["Боэтия", "Намира", "Мефала", "Ноктюрнал", "Азура", "Меридия", "Вермина"]
                )

tabaxi = Race("Табакси",
              ["Майк-Лжец", "Тархун", "Барбарис", "Квас", "Колокольчик", "Эдельвейс", "Спрайт"],
              ["Ситро", "Дюшес", "Пепси", "Кока", "Кола", "Фанта", "Фантола", "Бонаква", "Баржоми"]
              )

races = [human, elf, dwarf, gnome, dragonborn, tiefling, tabaxi]


def gen_character(f, player_id: int):
    race = choice(races)
    gender = random()

    f.write(str(player_id) + ";")
    f.write(str(randint(1, 21)) + ";")  # Level
    f.write(str(random() > 0.3) + ";")  # Is Alive

    f.write(race.tag + ";")
    f.write("Муж.;" if gender >= 0.5 else "Жен.;")
    f.write((choice(race.male_names) if gender >= 0.5 else choice(race.female_names)) + ";")
    f.write(choice(backgrounds) + ";")
    f.write(choice(alignments))

    f.write("\n")


def main():
    with open("dnd_players.csv", "r", encoding='utf-8') as f_players, open("dnd_characters.csv", "w", encoding='utf-8') as f_chars:
        next(f_players)
        for p in f_players:
            index = int(p.split(sep=';', maxsplit=2)[0])
            count = randint(1, 4) if random() < 0.75 else randint(1, 8)

            for i in range(count):
                gen_character(f_chars, index)


if __name__ == '__main__':
    main()
