import psycopg2
from peewee import *

con = PostgresqlDatabase(
	database='postgres',
	user='postgres',
	password='qwerty',
	host='127.0.0.1',
	port=5432
)


class BaseModel(Model):
    class Meta:
        database = con


class Character(BaseModel):
    id = IntegerField('id')
    player_id = IntegerField('player_id')
    name = TextField('name')
    level = IntegerField('level')
    race = TextField('race')
    gender = TextField('gender')
    background = TextField('background')
    alignment = TextField('alignment')
    is_alive = BooleanField('is_alive')

    class Meta:
        table_name = 'character_copy'


class Party(BaseModel):
    adventure_id = IntegerField('adventure_id')
    character_id = IntegerField('character_id')

    class Meta:
        table_name = 'party'


class Adventure(BaseModel):
    id = IntegerField('id')
    master_id = IntegerField('master_id')
    name = TextField('name')
    game_world = TextField('game_world')
    genre = TextField('genre')
    deus_ex_machina_count = TextField('deus_ex_machina_count')
    robbed_caravans_count = TextField('robbed_caravans_count')

    class Meta:
        table_name = 'adventure'


def q1():
    c = Character.get(Character.id == 1)

    print('Поиск по ID:')
    print(c.id, c.name, c.level, c.race, c.gender, c.background, c.alignment)

    q = Character.select().where(Character.level == 1).limit(5).order_by(Character.name)
    selected = q.dicts().execute()
    print('Select по уровню:')
    for elem in selected:
        print(f"{elem['name']:<10} {elem['level']:<4} {elem['race']:<29} {elem['gender']:<7}")


def q2():
    q = Character.select(Character.id, Character.name, Adventure.name, Adventure.genre)\
        .join(Party, on=(Character.id == Party.character_id))\
        .join(Adventure, on=(Party.adventure_id == Adventure.id))\
        .limit(5)\
        .where(Character.level == 1)

    selected = q.dicts().execute()
    print('Character Join Adventure:')
    for elem in selected:
        print(f"{elem['id']:<6} {elem['name']:<10}  {elem['genre']:<7}")


def q3():
    q = Character.select().limit(5).order_by(Character.id.desc())

    selected = q.dicts().execute()
    print('Последние 5 персонажей:')
    for elem in selected:
        print(f"{elem['name']:<10} {elem['level']:<4} {elem['race']:<29} {elem['gender']:<7}")

    c1 = Character.get(Character.id == q[1].id)
    c1.level = 1
    c1.save()

    c2 = Character.get(Character.id == q[0].id)
    c2.delete_instance()

    c3 = Character.create(id=q[0].id + 1, name='Майк-Лжец', race='Каджит', level=20, gender='Жен.')


def q4():
    global con

    cursor = con.cursor()

    cursor.execute("call character_dies(1130)")
    cursor.execute("select * from dies_t")

    print("Список смертей персонажа:")
    c = Character.get(Character.id == 1130)

    print(c.id, c.name, c.level, c.race, c.gender, c.background, c.alignment)

    for elem in cursor.fetchall():
        print(elem)

    con.commit()
    cursor.close()


def task_3():
    global con

    print('\n1. Однотабличный запрос на выборку\n')
    q1()

    print('\n2. Многотабличный запрос на выборку\n')
    q2()

    print('\n3. Запросы на Добавление, Удаление и Изменение в БД\n')
    q3()

    print('\n4. Использование Хранимой Процедуры\n')
    q4()

    con.close()
    print("\nБаза данных закрыта\n")

