from random import random, choice, randint, shuffle


def gen_party(f, adventure_id: int,  character_id: int):
    f.write(str(adventure_id) + ";")
    f.write(str(character_id))

    f.write("\n")


def main():
    adventures = []
    characters = []

    with open("dnd_adventures.csv", "r", encoding='utf-8') as f_adventures:
        next(f_adventures)
        for a in f_adventures:
            index = int(a.split(sep=';', maxsplit=2)[0])
            adventures.append(index)

    with open("dnd_characters.csv", "r", encoding='utf-8') as f_chars:
        next(f_chars)
        for p in f_chars:
            index = int(p.split(sep=';', maxsplit=2)[0])
            characters.append(index)

    shuffle(adventures)
    shuffle(characters)

    with open("dnd_party.csv", "w", encoding='utf-8') as f_party:
        for p in characters:
            gen_party(f_party, choice(adventures), p)


if __name__ == '__main__':
    main()
