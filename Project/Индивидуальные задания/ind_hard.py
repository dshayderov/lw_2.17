#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json
import os


def add_plane(staff, destination, num, typ):
    """
    Добавить данные о самолете.
    """
    staff.append(
        {
            "destination": destination,
            "num": num,
            "typ": typ,
        }
    )
    return staff


def display_planes(staff):
    """
    Отобразить список самолетов.
    """
    # Проверить, что список самолетов не пуст.
    if staff:
        # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+-{}-+".format("-" * 4, "-" * 30, "-" * 20, "-" * 15)
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^15} |".format(
                "No", "Пункт назначения", "Номер рейса", "Тип самолета"
            )
        )
        print(line)

        # Вывести данные о всех самолетах.
        for idx, plane in enumerate(staff, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:>15} |".format(
                    idx,
                    plane.get("destination", ""),
                    plane.get("num", 0),
                    plane.get("typ", ""),
                )
            )

        print(line)

    else:
        print("Список самолетов пуст")


def select_planes(staff, typ):
    """
    Выбрать самолеты с заданным типом.
    """
    # Сформировать список самолетов.
    result = [plane for plane in staff if typ == plane.get("typ", "")]

    # Возвратить список выбранных самолетов.
    return result


def save_planes(file_name, staff):
    """
    Сохранить все самолеты в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_planes(file_name):
    """
    Загрузить все самолеты из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


@click.command()
@click.argument('filename')
@click.option('--command', '-c', help="Commands")
@click.option('--destination', '-d', help="The plane's destination")
@click.option('--num', '-n', type=int, help="The plane's numer")
@click.option('--typ', '-t', help="The plane's type")
def main(filename, command, destination, num, typ):
    """
    Главная функция программы.
    """
    # Загрузить всех работников из файла, если файл существует.
    is_dirty = False
    if os.path.exists(filename):
        planes = load_planes(filename)
    else:
        planes = []

    # Добавить работника.
    if command == "add":
        planes = add_plane(planes, destination, num, typ)
        is_dirty = True

    # Отобразить всех работников.
    elif command == "display":
        display_planes(planes)

    # Выбрать требуемых рааботников.
    elif command == "select":
        selected = select_planes(planes, typ)
        display_planes(selected)

    # Сохранить данные в файл, если список работников был изменен.
    if is_dirty:
        save_planes(filename, planes)


if __name__ == "__main__":
    main()