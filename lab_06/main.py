import psycopg2


def task_1(cur):
    cur.execute("select count(*) from character where level = 20")
    print(cur.fetchall())


def task_2(cur):
    cur.execute('''
    SELECT "name", GENDER, PERSON_NAME, PERSON_GENDER, PERSON_RACE, CITY, DEATH_REASON
    from PLAYER P  
    join (select id, "name" as PERSON_NAME, GENDER as PERSON_GENDER, RACE as PERSON_RACE, DEATH_REASON
	      from "character" C
	      join (select CHARACTER_ID, DEATH_REASON
	  	        from DEATH D 
	  		    where lower(D.DEATH_REASON) NOT LIKE '%старость%') cx
	      on C.ID = cx.CHARACTER_ID) cy
    on P.ID = cy.ID
''')
    for ln in cur.fetchall():
        print(ln)


def task_3(cur):
    cur.execute('''
    with tmp as(
	select P."name" as player_name, P.city, c."name" as character_name,
		min(c."level") over (partition by c."name") as min_level,
		max(c."level") over (partition by c."name") as max_level
	from "character" c left join "player" p on p.ID = c.PLAYER_ID
)
select * from tmp where min_level < max_level
''')
    for ln in cur.fetchall():
        print(ln)


def task_4(cur):
    cur.execute('select table_name from information_schema.tables')
    for ln in cur.fetchall():
        print(ln)


def task_5(cur):
    cur.execute('select my_count(1130)')
    for ln in cur.fetchall():
        print(ln)


def task_6(cur):
    cur.execute('select * from my_table2(1129)')
    for ln in cur.fetchall():
        print(ln)


def task_7(cur):
    cur.execute('call proc_count(1130)')
    cur.execute('select * from deads_t')
    for ln in cur.fetchall():
        print(ln)


def task_8(cur):
    cur.execute('select current_role')
    for ln in cur.fetchall():
        print(ln)


tflag = False
def task_9(cur):
    cur.execute('''
        CREATE TABLE if not exists spells(
        id SERIAL PRIMARY KEY,
        "level" int CHECK("level" between 0 and 9),
        "name" text, 
        "description" text
    );
    ''')
    global tflag
    tflag = True
    print('Готово.')


def task_10(cur):
    if tflag == False:
        print("Таблица не создана")
        return

    cur.execute('''
            INSERT into spells (level, name, description)
            values(3, 'Fireball', 'Destroy EVERYTHING')
            ''')
    print('Готово.')

    cur.execute('select * from spells')
    for ln in cur.fetchall():
        print(ln)


def get_info(cur):
    print('''0  --- Help
1  --- Скалярный запрос
2  --- Несколько Join'ов
3  --- Запрос с ОТВ и оконными функциями
4  --- Запрос к метаданным
5  --- Вызов скалярной функции
6  --- Вызов многооператорной функции
7  --- Вызов процедуры
8  --- Вызов системной функции
9  --- Создать таблицу в БД
10 --- Вставить данные в таблицу из п. 9
-1 --- EXIT
''')


def main():
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

    print("База данных успешно открыта")
    cur = con.cursor()

    cmd_index = 0
    tasks = [get_info, task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8, task_9, task_10]

    while True:
        if cmd_index < 0 or cmd_index >= len(tasks):
            break
        tasks[cmd_index](cur)
        cmd_index = int(input("Введите номер команды:"))

    cur.close()
    con.close()
    return


if __name__ == '__main__':
    main()
