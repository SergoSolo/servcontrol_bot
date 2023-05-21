import re


def create_message_text(objects: list, object_type: str, page: int):
    text = (
        f"<b>Страница {page + 1} из {len(objects)}.</b>"
        "\n<i>Выберите объект нажав на кнопку:</i> \n\n"
    )
    if len(objects) == 0:
        text = "<i>Объектов нет.</i>"
    else:
        for index, db_object in enumerate(objects[page]):
            if object_type == "files" or object_type == "categories":
                text += f"{index + 1}) {db_object.name}\n"
            else:
                text += (
                    f"{index + 1}) {db_object.get_full_name()} "
                    f"г.{db_object.town}\n"
                )
    text += "\n<i>Для удаления сообщения нажмите ❌</i>"
    return text


def array_spliter(objects: list, limit: int):
    return [
        objects[db_object: db_object + limit]
        for db_object in range(0, len(objects), limit)
    ]


def validate(word: str) -> bool:
    valid_pattern = re.compile(r"^[А-Яа-я-]+$", re.I)
    return bool(re.match(valid_pattern, word))
