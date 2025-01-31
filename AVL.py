class Node:
    """
    Класс узла АВЛ-дерева.
    key   : Значение (натуральное число).
    height: Высота данного узла в дереве.
    left  : Ссылка на левое поддерево.
    right : Ссылка на правое поддерево.
    """
    __slots__ = ['key', 'height', 'left', 'right']

    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None


class AVLTree:
    """
    Класс АВЛ-дерева
    """

    def __init__(self):
        self.root = None

    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ДЛЯ БАЛАНСИРОВКИ ==========

    def get_height(self, node):
        """
        Возвращает высоту узла node.
        Если node = None, высота равна 0.
        """
        if not node:
            return 0
        return node.height

    def get_balance_factor(self, node):
        """
        Вычисляет баланс-фактор узла:
        разность высот левого и правого поддеревьев.
        """
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        """
        Обновляет высоту узла на основе высот его дочерних узлов.
        """
        node.height = max(self.get_height(node.left),
                          self.get_height(node.right)) + 1

    def rotate_right(self, y):
        """
        Правый поворот вокруг узла y.
        Возвращает новую вершину, которая стала вместо y.
        """
        x = y.left
        T2 = x.right

        # Выполняем поворот
        x.right = y
        y.left = T2

        # Обновляем высоты
        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        """
        Левый поворот вокруг узла x.
        Возвращает новую вершину, которая стала вместо x.
        """
        y = x.right
        T2 = y.left

        # Выполняем поворот
        y.left = x
        x.right = T2

        # Обновляем высоты
        self.update_height(x)
        self.update_height(y)

        return y

    def balance_node(self, node):
        """
        Балансирует узел node и возвращает
        ссылку на корень этого поддерева.
        """
        self.update_height(node)
        balance = self.get_balance_factor(node)

        # Если левое поддерево "тяжелее" правого
        if balance > 1:
            # Проверяем баланс поддерева слева
            if self.get_balance_factor(node.left) < 0:
                # LR-случай: сначала левый поворот левого потомка
                node.left = self.rotate_left(node.left)
            # Выполняем правый поворот
            return self.rotate_right(node)

        # Если правое поддерево "тяжелее" левого
        if balance < -1:
            # Проверяем баланс поддерева справа
            if self.get_balance_factor(node.right) > 0:
                # RL-случай: сначала правый поворот правого потомка
                node.right = self.rotate_right(node.right)
            # Выполняем левый поворот
            return self.rotate_left(node)

        return node

    # ========== БАЗОВЫЕ ОПЕРАЦИИ ==========

    def search(self, key):
        """
        Поиск ключа в дереве.
        Возвращает True, если ключ найден, иначе False.
        """
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if not node:
            return False
        if node.key == key:
            return True
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:  # key > node.key
            return self._search_recursive(node.right, key)

    def insert(self, key):
        """
        Вставка ключа key в АВЛ-дерево.
        """
        if key <= 0:
            raise ValueError("Ключ должен быть натуральным числом (> 0).")
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        """
        Рекурсивная функция вставки.
        Возвращает корень сбалансированного поддерева.
        """
        if not node:
            return Node(key)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key)
        else:
            # Допустим, мы не храним дубликаты ключей,
            # поэтому ничего не делаем или выбрасываем исключение
            # raise ValueError("Ключ уже существует!")
            return node

        # Балансируем и возвращаем корень
        return self.balance_node(node)

    def delete(self, key):
        """
        Удаление ключа key из АВЛ-дерева.
        """
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        """
        Рекурсивная функция удаления.
        Возвращает корень сбалансированного поддерева.
        """
        if not node:
            return None

        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Узел найден.
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Узел имеет двух потомков
                # Ищем минимальный ключ в правом поддереве
                min_larger_node = self._get_min_node(node.right)
                node.key = min_larger_node.key
                node.right = self._delete_recursive(node.right, min_larger_node.key)

        return self.balance_node(node)

    def _get_min_node(self, node):
        """
        Вспомогательная функция, возвращающая узел с минимальным ключом
        в поддереве с корнем node.
        """
        current = node
        while current.left:
            current = current.left
        return current

    # ========== ДОПОЛНИТЕЛЬНЫЕ ОПЕРАЦИИ ==========

    def split(self, key):
        """
        Разделение дерева по ключу 'key'.
        Возвращает кортеж (T1, T2), где:
        T1 - АВЛ-дерево с ключами <= key
        T2 - АВЛ-дерево с ключами > key
        """
        # Создадим два новых экземпляра AVLTree
        T1 = AVLTree()
        T2 = AVLTree()
        T1.root, T2.root = self._split_recursive(self.root, key)
        return T1, T2

    def _split_recursive(self, node, key):
        """
        Рекурсивная часть split.
        Возвращает кортеж (left_subtree_root, right_subtree_root).
        """
        if not node:
            return None, None

        if node.key <= key:
            # Правое поддерево может содержать элементы > key
            left_subtree_root, right_subtree_root = self._split_recursive(node.right, key)
            node.right = left_subtree_root
            node = self.balance_node(node)
            return node, right_subtree_root
        else:
            # Левое поддерево может содержать элементы <= key
            left_subtree_root, right_subtree_root = self._split_recursive(node.left, key)
            node.left = right_subtree_root
            node = self.balance_node(node)
            return left_subtree_root, node

    @staticmethod
    def merge(T1, T2):
        """
        Слияние двух АВЛ-деревьев T1 и T2.
        Предполагается, что все ключи в T1 <= все ключи в T2.
        Возвращает новое дерево - результат слияния.

        Принцип:
        1. Находим максимальный элемент в T1.
        2. Удаляем его из T1.
        3. Делаем его корнем, ставим левым поддеревом T1, правым - T2.
        4. Балансируем результат.
        """
        # Если одно из деревьев пустое, возвращаем второе
        if not T1.root:
            return T2
        if not T2.root:
            return T1

        # Находим максимальный узел в T1
        max_node = T1._get_max_node(T1.root)
        max_key = max_node.key

        # Удаляем его из T1
        T1.root = T1._delete_recursive(T1.root, max_key)

        # Создаем новый узел
        new_root = Node(max_key)
        new_root.left = T1.root
        new_root.right = T2.root

        # Создаем новое дерево, балансируем
        merged_tree = AVLTree()
        merged_tree.root = merged_tree.balance_node(new_root)
        return merged_tree

    def _get_max_node(self, node):
        """
        Вспомогательная функция для получения узла с максимальным ключом
        в поддереве node.
        """
        current = node
        while current.right:
            current = current.right
        return current

    # ========== СТАТИЧЕСКИЕ/ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

    def count_nodes(self):
        """
        Подсчёт количества узлов в дереве.
        """
        return self._count_nodes_recursive(self.root)

    def _count_nodes_recursive(self, node):
        if not node:
            return 0
        return 1 + self._count_nodes_recursive(node.left) + self._count_nodes_recursive(node.right)

    def inorder_traversal(self):
        """
        Симметричный (in-order) обход дерева.
        Возвращает список ключей в отсортированном порядке.
        """
        result = []
        self._inorder_traversal_recursive(self.root, result)
        return result

    def _inorder_traversal_recursive(self, node, result):
        if node:
            self._inorder_traversal_recursive(node.left, result)
            result.append(node.key)
            self._inorder_traversal_recursive(node.right, result)

    # ========== ВАЛИДАЦИЯ АВЛ-ДЕРЕВА ==========

    def validate_avl(self):
        """
        Проверка, что дерево является корректным АВЛ-деревом:
        1. Удовлетворяется свойство BST (левые < узел < правые).
        2. Баланс-фактор каждого узла по модулю <= 1.
        """
        # Проверим BST-свойство + вычислим высоты рекурсивно
        keys_inorder = self.inorder_traversal()
        # Если ключи в отсортированном обходе не строго возрастают,
        # значит BST-свойство нарушено (зависит от задачи —
        # можно ли хранить равные ключи или нет).
        for i in range(len(keys_inorder) - 1):
            if keys_inorder[i] >= keys_inorder[i + 1]:
                return False

        return self._validate_balances(self.root)

    def _validate_balances(self, node):
        """
        Рекурсивно проверяет, что для каждого узла баланс-фактор <= 1 по модулю.
        """
        if not node:
            return True

        balance = self.get_balance_factor(node)
        if abs(balance) > 1:
            return False

        return self._validate_balances(node.left) and self._validate_balances(node.right)
