from kanren import Relation, facts, run, conde, var
from sympy import symbols

from typing import Optional

bird_facts = Relation()

facts(
    bird_facts,
    ("Синица", "маленькая", "желтая", "лес"),
    ("Ласточка", "маленькая", "черная", "лес"),
    ("Пеликан", "большая", "белая", "берег"),
    ("Аист", "средняя", "белая", "болото"),
    ("Павлин", "большая", "синяя", "парк")
)

def get_bird(size: str, color: str, habitat: str) -> Optional[str]:
    x = var()
    condition = conde(
        (bird_facts(x, size, color, habitat),)
    )
    result = run(1, x, condition)
    
    return result[0] if result else None


def main():
    try:
        size, color, habitat = [str(x).lower() for x in symbols(input("Введите описание птицы: "))]
    except (TypeError, ValueError):
        print("Неверный ввод данных")
        return

    bird_name = get_bird(size, color, habitat)

    if bird_name is not None:
        print(f"Это: {bird_name}")
    else:
        print("Не знаю такую птицу")

main()
