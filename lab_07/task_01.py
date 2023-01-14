from py_linq import Enumerable
from character import *


def request_1(enm):
    result = enm.where(lambda x: x['race'] == "Гном" and x['level'] == 1)
    for elem in result:
        print(elem)


def request_2(enm):
    result = enm.count(lambda x: x['level'] == 20)
    print("Количество персонажей 20-го уровня:", result)


def request_3(enm):
    result = enm.where(lambda x: x['name'][0] in ('A', 'Б', 'В'))\
        .group_by(key_names=['name'], key=lambda x: x['name'])\
        .select(lambda x: {'key': x.key.name, 'count': x.count()})
    for elem in result:
        print(elem)


def request_4(enm):
    res1 = enm.where(lambda x: x['race'] == "Эльф" and x['level'] == 1)
    res2 = enm.where(lambda x: x['race'] == "Табакси" and x['level'] == 2)
    result = Enumerable(res1).union(res2, lambda x: x)\
        .where(lambda x: x['name'][0] in ('A', 'Б', 'В', 'Г', 'Д'))\
        .order_by(lambda x: x['name'])

    for elem in result:
        print(elem)


def request_5(enm):
    jj = Enumerable([{'race': 'Эльф',    'tag': 'Ушастый'},
                     {'race': 'Гном',    'tag': 'Низкий'},
                     {'race': 'Дварф',   'tag': 'Низкий'},
                     {'race': 'Табакси', 'tag': 'Любит Вискас'}])
    result = enm.where(lambda x: x['id'] <= 20).join(jj, lambda o_k: o_k['race'], lambda i_k: i_k['race'])

    for elem in result:
        print(elem[0], elem[1]['tag'])


def task_1():
    arr = create_characters("C:\\Users\\nik07\\Desktop\\character.csv")
    enm = Enumerable(arr)

    print("\nЗапрос 1:\n")
    request_1(enm)

    print("\nЗапрос 2:\n")
    request_2(enm)

    print("\nЗапрос 3:\n")
    request_3(enm)

    print("\nЗапрос 4:\n")
    request_4(enm)

    print("\nЗапрос 5:\n")
    request_5(enm)


