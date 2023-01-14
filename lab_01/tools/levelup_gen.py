from random import random, choice, randint, randrange


def gen_levelup(f, character_id: int, class_id: int, level: int):
    f.write(str(character_id) + ";")
    f.write(str(class_id) + ";")
    f.write(str(level))

    f.write("\n")


def main():
    CLASS_COUNT = 12
    with open("dnd_characters.csv", "r", encoding='utf-8') as f_chars, open("dnd_levels.csv", "w", encoding='utf-8') as f_levels:
        next(f_chars)
        for p in f_chars:
            arr = p.split(sep=';', maxsplit=5)
            index = int(arr[0])
            level = int(arr[2])

            case = random()
            if level == 1 or case > 0.05:
                gen_levelup(f_levels, index, randint(1, CLASS_COUNT), level)
            else:
                level_in_classes = [0] * CLASS_COUNT
                while level > 0:
                    x = max(randint(1, level), randint(1, level))
                    level_in_classes[randrange(0, CLASS_COUNT)] += x
                    level -= x
                for i in range(CLASS_COUNT):
                    if level_in_classes[i] > 0:
                        gen_levelup(f_levels, index, i + 1, level_in_classes[i])
                    

if __name__ == '__main__':
    main()
