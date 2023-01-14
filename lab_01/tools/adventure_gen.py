from random import choice, randint, random

names = ["Авторская"
         "Туда и обратно",
         "Битва пяти воинств",
         "Из бездны",
         "Врата Балдура",
         "Гром Штормового Короля",
         "Байки Зияющего портала",
         "Призраки Солтмарша",
         "Гробница Аннигиляции",
         "Затерянные рудники Фанделвера",
         "Погоня за Драконом",
         "Подземелье Безумного Мага",
         "Бесполезные земли",
         "Расколотые небеса",
         "Ультиматум дракона",
         "Проклятье алого трона",
         "Горькое пиво",
         "Поместье советника",
         "Двигатель торговли",
         "Великие башни",
         "Баронский счет",
         "Тени прошлого",
         "Большая проблема",
         "Смертельные слабости королей",
         "Королевский подвиг",
         "Жизнь и Смерть",
         "Золото Импра",
         "Хлопоты посмертия",
         "Вечная любовь",
         "Кровные обиды",
         "Претенденты на престол",
         "Советник демона",
         "Барон Логики",
         "Побеждаешь или погибаешь",
         "Война пяти королей",
         "Хаос - это лестница"
         ]

worlds = ["Авторский", "Авторский", "Авторский", "Авторский",
          "Забытые королевства", "Забытые королевства", "Забытые королевства",
          "Забытые королевства", "Забытые королевства", "Забытые королевства",
          "Эберрон", "Эберрон",
          "Тамриэль",
          "Средиземье",
          "Неверленд",
          "Плоский мир",
          ]

genres = ["Эпическое фентези", "Эпическое фентези",
          "Эпическое фентези", "Эпическое фентези",
          "Комедия", "Комедия",
          "Трагедия",
          "Детектив",
          "Хоррор"
          ]


def gen_adventure(f, master_id: int):
    f.write(choice(names) + ";")
    f.write(choice(worlds) + ";")
    f.write(choice(genres) + ";")
    f.write(str(master_id) + ";")
    f.write(str(randint(0, 20)) + ";")  # Count of Deus ex machina
    f.write(str(randint(0, 20)))  # Count of Robbed caravans

    f.write("\n")


def main():
    count = 0
    with open("dnd_players.csv", "r", encoding='utf-8') as f_players, open("dnd_adventures.csv", "w", encoding='utf-8') as f_adventures:
        next(f_players)
        for p in f_players:
            if random() < 0.05:
                index = int(p.split(sep=';', maxsplit=2)[0])
                gen_adventure(f_adventures, index)
                count += 1


if __name__ == '__main__':
    main()
