import pytest
from AVL import AVLTree


@pytest.fixture
def example_tree():
    tree = AVLTree()
    for key in [10, 20, 5, 6, 15, 30, 25]:
        tree.insert(key)
    return tree


def test_search(example_tree):
    """
    Проверяем, что поиск существующего и несуществующего ключа
    возвращает ожидаемые результаты.
    """
    assert example_tree.search(15) is True
    assert example_tree.search(100) is False


def test_insert():
    """
    Тест вставки (включая проверку исключений) и корректности структуры.
    """
    tree = AVLTree()

    # Проверка, что при вставке не-натурального числа возникает исключение
    with pytest.raises(ValueError):
        tree.insert(0)

    # Вставляем несколько ключей и проверяем их порядок через обход
    keys_to_insert = [10, 5, 20, 15]
    for k in keys_to_insert:
        tree.insert(k)

    # Ожидаем отсортированный список [5, 10, 15, 20]
    assert tree.inorder_traversal() == [5, 10, 15, 20]

    # Проверяем, что дерево по-прежнему валидно
    assert tree.validate_avl() is True


def test_delete(example_tree):
    """
    Тест удаления элемента.
    Проверяем, что элемент действительно удаляется,
    а дерево остаётся валидным АВЛ-деревом.
    """
    # Перед удалением убедимся, что ключ есть
    assert example_tree.search(20) is True

    # Удаляем ключ
    example_tree.delete(20)

    # Проверяем, что он удалён
    assert example_tree.search(20) is False

    # Проверяем, что дерево остаётся валидным
    assert example_tree.validate_avl() is True


def test_count_nodes(example_tree):
    """
    Проверяем подсчёт числа элементов.
    """
    # Изначально 7 вставленных узлов
    assert example_tree.count_nodes() == 7

    # Удалим несколько ключей и проверим
    example_tree.delete(10)
    example_tree.delete(5)
    assert example_tree.count_nodes() == 5


def test_inorder_traversal(example_tree):
    """
    Проверяем, что симметричный обход возвращает отсортированный список ключей.
    """
    result = example_tree.inorder_traversal()
    assert result == sorted(result)
    assert result == [5, 6, 10, 15, 20, 25, 30]


def test_split_merge():
    """
    Тестируем операции split и merge
    """
    tree = AVLTree()
    for k in [1, 2, 3, 4, 5, 6]:
        tree.insert(k)

    # Разделим дерево по ключу 3 (T1 должен содержать <=3, T2 >3)
    T1, T2 = tree.split(3)

    # Проверяем результат split
    assert T1.inorder_traversal() == [1, 2, 3], "Ошибка в split (левая часть)"
    assert T2.inorder_traversal() == [4, 5, 6], "Ошибка в split (правая часть)"

    # Обратно сольём
    merged_tree = AVLTree.merge(T1, T2)
    # В итоговом дереве должны быть ключи [1, 2, 3, 4, 5, 6]
    assert merged_tree.inorder_traversal() == [1, 2, 3, 4, 5, 6], "Ошибка в merge"

    # Проверяем, что итоговое дерево АВЛ-валидно
    assert merged_tree.validate_avl() is True


def test_validate_avl(example_tree):
    """
    Проверяем, что примерное дерево действительно
    распознаётся как валидное АВЛ-дерево.
    """
    assert example_tree.validate_avl() is True, "Дерево должно быть валидным АВЛ"
    example_tree.root.left.height = 1000  # Нарушаем высоту
    assert example_tree.validate_avl() is False, "Теперь дерево не должно быть валидным"


def test_empty_tree():
    """
    Проверяем пограничные случаи на пустом дереве.
    """
    empty_tree = AVLTree()

    assert empty_tree.count_nodes() == 0, "Пустое дерево должно иметь 0 узлов"
    assert empty_tree.inorder_traversal() == [], "Обход пустого дерева должен быть пустым"
    assert empty_tree.search(10) is False, "Поиск в пустом дереве всегда False"
    assert empty_tree.validate_avl() is True, "Пустое дерево можно считать валидным АВЛ"

    # Удаление/разделение в пустом дереве не должно приводить к ошибкам
    empty_tree.delete(10)  # Просто не изменит дерево
    assert empty_tree.count_nodes() == 0

    T1, T2 = empty_tree.split(10)
    assert T1.count_nodes() == 0
    assert T2.count_nodes() == 0

    # Слияние пустого дерева с непустым должно давать непустое дерево
    non_empty_tree = AVLTree()
    non_empty_tree.insert(5)
    merged_tree = AVLTree.merge(empty_tree, non_empty_tree)
    assert merged_tree.count_nodes() == 1
    assert merged_tree.inorder_traversal() == [5]
