from random import random, choice, randint
import datetime
import json

# Необходимо предварительно поместить в папку файл dnd_characters.csv, полученный при создании базы данных

reasons = ["Загрыз барсук",
           "Много болтал",
           "Много знал",
           "Недопонимание",
           "Несчастный случай",
           "Лежа в постели, в восемьдесят лет, напившись вина и...",
           "Старость",
           "Сражение с гоблинами",
           "Гильотина",
           "Повешен",
           "Топор палача",
           "Отравление",
           "Превращен в курицу волшебником",
           "Утонул",
           "Удар молнии",
           "Удар тупым предметом по голове",
           "Съеден волками",
           "Несоблюдение техники безопасности при обращении с сумкой хранения",
           "Убит великаном",
           "Огненный шар"
           ]

last_words = ["Через час те из вас кто останется в живых, будут завидовать мертвым!",
              "Я буду драться за троих, нет, за семерых! Нет, за двенадцатерых!"
              "Я вернусь!",
              "И ты, Брут!",
              "Наливай!",
              "Щас мы с ними разберемся",
              "Сейчас я им покажу"
              "Всё кончено."
              "Я умираю",
              "<Слово силы> \"Смерть\""
              "1 : 1",
              "Так не доставайся же ты никому",
              "Порталы... Ненавижу",
              "<...>"
              ]


def rand_date(start: datetime, end: datetime) -> str:
    val = start + datetime.timedelta(seconds=randint(0, int((end - start).total_seconds())))
    return str(val)


def gen_death(data, character_id: int):
    dt_start = datetime.date(1999, 1, 1)
    dt_end = datetime.date(2022, 12, 31)
    data.append( {"cid" : character_id, "reason" : choice(reasons), "last_words" : choice(last_words), "date" :  rand_date(dt_start, dt_end)})


def main():
    data = []
    with open("dnd_characters.csv", "r", encoding='utf-8') as f_chars, open("dnd_deaths.json", "w", encoding='utf-8') as f_deaths:
        next(f_chars)
        for p in f_chars:
            arr = p.split(sep=';', maxsplit=5)
            index = int(arr[0])
            is_alive = bool(arr[3])

            if is_alive:
                if random() < 0.05:
                    count = max(1, min(randint(0, 4), randint(0, 4), randint(0, 4)))
                    for i in range(count):
                        gen_death(data, index)
            else:
                gen_death(data, index)
                if random() < 0.05:
                    count = max(1, min(randint(0, 4), randint(0, 4), randint(0, 4)))
                    for i in range(count):
                        gen_death(data, index)
                        
        json.dump(data, f_deaths)


if __name__ == '__main__':
    main()
