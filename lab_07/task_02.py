import json

import psycopg2
from character import *


def read_table_json(cur, count=50):
    cur.execute("select * from character_import")
    rows = cur.fetchmany(count)
    array = list()
    for elem in rows:
        array.append(elem[0])
    return array


def update(arr):
    for el in arr:
        if el['level'] < 10:
            el['level'] += 1
        elif el['level'] > 18:
            el['is_alive'] = False


def add(arr, character):
    arr.append(character.dictionary())


def task_2():
    try:
        con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="qwerty",
            host="127.0.0.1",
            port="5432"
        )
    except:
        print("Ошибка при подключении к БД")
        return

    cur = con.cursor()
    print("База данных успешно открыта")

    arr = read_table_json(cur, 10)
    print("\nФайл загружен:\n")
    for el in arr:
        print(el)

    update(arr)
    add(arr, Character(99, 99, 'Паку', 1, 'Пчеловек', 'Муж.', 'Выращен пчелами', 'центрист', True))

    print("\nФайл обновлен:\n")
    for el in arr:
        print(el)

    cur.close()
    con.close()
    print("\nБаза данных закрыта\n")
