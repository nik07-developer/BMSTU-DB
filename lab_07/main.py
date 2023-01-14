from task_01 import task_1
from task_02 import task_2
from task_03 import *


def main():
    answer = int(input("Task Number: "))

    if answer == 1:
        task_1()
    elif answer == 2:
        task_2()
    elif answer == 3:
        task_3()

    return


if __name__ == '__main__':
    main()
