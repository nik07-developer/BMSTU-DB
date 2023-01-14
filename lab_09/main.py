from peewee import *
from redis import *
import json
import matplotlib.pyplot as plt

from time import sleep
from datetime import datetime


def info_postgres(cur):
    print("\nTop 10 Плутов в Базе Данных:\n")
    c = cur.description
    print(f"{c[0][0]:<6} {c[1][0]:<12} {c[2][0]:<12} {c[3][0]:<17} {c[4][0]:<15} {c[5][0]:<15} {c[6][0]:<15}")

    for elem in cur.fetchall():
        print(f"{elem[0]:<6} {elem[1]:<12} {elem[2]:<12} {elem[3]:<17} {elem[4]:<15} {elem[5]:<15} {elem[6]:<15}")

    print()


def info_redis(jsn):
    print("\nTop 10 Плутов в Базе Данных:\n")
    c = list(jsn[0].keys())
    print(f"{c[0]:<6} {c[1]:<12} {c[2]:<12} {c[3]:<17} {c[4]:<15} {c[5]:<15} {c[6]:<15}")
    for x in jsn:
        print(f"{x[c[0]]:<6} {x[c[1]]:<12} {x[c[2]]:<12} {x[c[3]]:<17} {x[c[4]]:<15} {x[c[5]]:<15} {x[c[6]]:<15}")
    print()


def find_last(cur) -> int:
    cur.execute("select max(id) from character_copy")
    for x in cur.fetchall():
        return int(x[0])


def update_last(cur):
    maxid = find_last(cur)
    cur.execute(f'update character_copy set level = 1 where "id" = {maxid}')


def append_new(cur):
    id = find_last(cur) + 1
    cur.execute(f"insert into character_copy (ID, PLAYER_ID, name, level, race, gender)"
                f"values({id}, 1, 'Maйк-говорит-правду', 1, 'Каджит', 'Муж.');")


def delete_last(cur):
    maxid = find_last(cur)
    cur.execute(f'delete from character_copy where "id" = {maxid}')


def main():
    rd = Redis(host='localhost', port=6379)
    print("Соединение с Redis установлено")

    con = PostgresqlDatabase(
        database='postgres',
        user='postgres',
        password='qwerty',
        host='127.0.0.1',
        port=5432
    )
    cur = con.cursor()
    print("Соединение с Postgres установлено")

    rx = []
    ry = []

    px = []
    py = []

    is_updated = True

    for i in range(20):
        rx.append(i)
        px.append(i)

        dt1 = datetime.now()
        cur.execute("select * from top_rogue(10)")
        dt2 = datetime.now()
        py.append((dt2 - dt1).total_seconds())
        # info_postgres(cur)

        delta = 0

        if i % 2 == 0:
            update_last(cur)
            # delete_last(cur)
            # append_new(cur)
            dt1 = datetime.now()
            cur.execute("select * from top_rogue(10)")
            tmp = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
            rd.set('key', json.dumps(tmp))
            dt2 = datetime.now()
            delta = (dt2 - dt1).total_seconds()

        dt1 = datetime.now()
        jsn = json.loads(rd.get('key'))
        dt2 = datetime.now()
        ry.append((dt2 - dt1).total_seconds() + delta)
        # info_redis(jsn)
        sleep(0.1)

    plt.plot(rx, ry, 'r', label='Redis')
    plt.plot(px, py, 'b', label='Postgres')
    plt.legend()
    plt.show()

    cur.execute("select * from top_rogue(5)")
    info_postgres(cur)

    cur.close()
    con.close()
    print("Соединение с Postgres заакрыто")

    rd.close()
    print("Соединение с Redis закрыто")
    return


if __name__ == '__main__':
    main()
