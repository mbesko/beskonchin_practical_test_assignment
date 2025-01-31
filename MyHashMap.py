class MyHashMap:
    """
    Простейшая реализация ассоциативного массива (Map) на Python
    методом цепочек (separate chaining).
    """

    def __init__(self, initial_capacity=8):
        # Список "бакетов" (каждый бакет - список пар (key, value))
        self._buckets = [[] for _ in range(initial_capacity)]
        # Текущее число хранящихся элементов
        self._size = 0
        # Коэффициент загрузки, при котором происходит расширение
        self._load_factor_threshold = 0.75

    def _get_bucket_index(self, key):
        """
        Вычисляет индекс бакета для данного ключа,
        исходя из хеш-функции и длины списка бакетов.
        """
        return hash(key) % len(self._buckets)

    def _rehash(self):
        """
        Увеличивает размер массива бакетов (в 2 раза) и
        заново распределяет в них все имеющиеся пары (key, value).
        """
        old_buckets = self._buckets
        new_capacity = len(old_buckets) * 2
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0  # При повторном добавлении size пересчитается

        for bucket in old_buckets:
            for (key, value) in bucket:
                self.put(key, value)

    def put(self, key, value):
        """
        Добавляет пару (key, value) в ассоциативный массив.
        Если ключ уже есть, обновляет значение.
        """
        index = self._get_bucket_index(key)
        bucket = self._buckets[index]

        # Ищем, есть ли уже такой ключ, чтобы обновить
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (k, value)  # обновим значение
                return

        # Иначе - добавим новую пару
        bucket.append((key, value))
        self._size += 1

        # Проверяем, не нужно ли расширять таблицу
        if self._size / len(self._buckets) > self._load_factor_threshold:
            self._rehash()

    def get(self, key):
        """
        Извлекает значение по ключу.
        Возвращает None, если ключ не найден.
        """
        index = self._get_bucket_index(key)
        bucket = self._buckets[index]
        for (k, v) in bucket:
            if k == key:
                return v
        return None

    def remove(self, key):
        """
        Удаляет пару (key, value) из ассоциативного массива.
        Ничего не делает, если ключ не найден.
        """
        index = self._get_bucket_index(key)
        bucket = self._buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return

    def size(self):
        """
        Возвращает текущее количество пар (ключ, значение) в структуре.
        """
        return self._size

    def __str__(self):
        """
        Простейшее отображение внутреннего состояния для отладки.
        """
        return f"MyHashMap(size={self._size}, buckets={self._buckets})"
