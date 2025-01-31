import pytest
from MyHashMap import MyHashMap

@pytest.fixture
def empty_map():
    return MyHashMap()

@pytest.fixture
def filled_map():
    m = MyHashMap()
    m.put("apple", 1)
    m.put("banana", 2)
    m.put("orange", 3)
    return m


def test_put_and_get(filled_map):
    """
    Тест вставки (put) и получения (get).
    """
    assert filled_map.get("apple") == 1
    assert filled_map.get("banana") == 2
    assert filled_map.get("orange") == 3

    # Попробуем получить ключ, которого нет
    assert filled_map.get("kiwi") is None

    # Обновим значение существующего ключа
    filled_map.put("banana", 42)
    assert filled_map.get("banana") == 42


def test_remove(filled_map):
    """
    Тест удаления (remove).
    """
    # Удалим ключ, проверим, что он пропал
    filled_map.remove("apple")
    assert filled_map.get("apple") is None
    assert filled_map.size() == 2

    # Удалим несуществующий ключ - всё должно остаться без изменений
    filled_map.remove("kiwi")
    assert filled_map.size() == 2


def test_size(empty_map, filled_map):
    """
    Тест корректности размера (size).
    """
    assert empty_map.size() == 0

    empty_map.put("one", 1)
    assert empty_map.size() == 1

    filled_map.remove("banana")
    assert filled_map.size() == 2  # Из 3-х удалили 1


def test_update_value(empty_map):
    """
    Тест повторной вставки одного и того же ключа (обновление значения).
    """
    empty_map.put("x", 10)
    assert empty_map.get("x") == 10

    # Обновим
    empty_map.put("x", 999)
    assert empty_map.get("x") == 999

    # Размер не должен увеличиться, т.к. мы обновили существующий ключ
    assert empty_map.size() == 1


def test_rehash():
    """
    Тест расширения (rehash) при достижении порога загрузки.
    """
    m = MyHashMap(initial_capacity=2)  # Начальный размер 2, порог 0.75
    # Вставляем несколько элементов, чтобы переполнить
    m.put("a", 1)
    m.put("b", 2)
    # Коэффициент загрузки = 2 / 2 = 1.0 > 0.75 -> должен произойти rehash

    # Проверим, что все элементы доступны и размер верен
    assert m.size() == 2
    assert m.get("a") == 1
    assert m.get("b") == 2

    # Продолжим вставлять, чтобы убедиться, что таблица работает корректно
    m.put("c", 3)
    assert m.size() == 3
    assert m.get("c") == 3

    # Удалим и проверим
    m.remove("b")
    assert m.size() == 2
    assert m.get("b") is None
