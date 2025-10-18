from typing import Callable, Dict, Optional, Any
from collections import deque
import timeit
import matplotlib.pyplot as plt


def build_tree_recursive(
    root: int,
    height: int,
    left_leaf: Callable[[int], int] = lambda x: 2 - (x - 1),
    right_leaf: Callable[[int], int] = lambda x: x * 2
) -> Optional[Dict[str, Any]]:
    """
    Рекурсивное построение бинарного дерева.

    Аргументы:
        root (int): Значение корня дерева.
        height (int): Высота дерева (>= 1).
        left_leaf (Callable[[int], int]): Функция для вычисления левого потомка.
        right_leaf (Callable[[int], int]): Функция для вычисления правого потомка.

    Возвращает:
        dict: Дерево в формате {'value': <узел>, 'left': <левое>, 'right': <правое>}
    """
    if height < 1:
        return None

    return {
        "value": root,
        "left": build_tree_recursive(left_leaf(root), height - 1, left_leaf, right_leaf),
        "right": build_tree_recursive(right_leaf(root), height - 1, left_leaf, right_leaf)
    }


def build_tree_iterative(
    root: int,
    height: int,
    left_leaf: Callable[[int], int] = lambda x: 2 - (x - 1),
    right_leaf: Callable[[int], int] = lambda x: x * 2
) -> Dict[str, Any]:
    """
    Нерекурсивное построение бинарного дерева с использованием очереди.

    Аргументы:
        root (int): Значение корня дерева.
        height (int): Высота дерева (>= 1).
        left_leaf (Callable[[int], int]): Функция для вычисления левого потомка.
        right_leaf (Callable[[int], int]): Функция для вычисления правого потомка.

    Возвращает:
        dict: Дерево в формате {'value': <узел>, 'left': <левое>, 'right': <правое>}
    """
    if height < 1:
        raise ValueError("Высота дерева должна быть >= 1")

    tree = {"value": root, "left": None, "right": None}
    queue = deque([(tree, 1)])

    while queue:
        node, level = queue.popleft()
        if level < height:
            l_val = left_leaf(node["value"])
            r_val = right_leaf(node["value"])
            node["left"] = {"value": l_val, "left": None, "right": None}
            node["right"] = {"value": r_val, "left": None, "right": None}
            queue.append((node["left"], level + 1))
            queue.append((node["right"], level + 1))

    return tree


def compare_build_times(max_height: int = 10, repeat: int = 3):
    """
    Сравнение времени построения рекурсивного и нерекурсивного дерева.
    Строит график время (Y) vs высота дерева (X).

    Аргументы:
        max_height (int): Максимальная высота дерева.
        repeat (int): Количество повторений для timeit.
    """
    heights = list(range(1, max_height + 1))
    recursive_times = []
    iterative_times = []

    for h in heights:
        rec_time = timeit.timeit(
            stmt=f'build_tree_recursive(14, {h})',
            setup='from __main__ import build_tree_recursive',
            number=repeat
        ) / repeat
        it_time = timeit.timeit(
            stmt=f'build_tree_iterative(14, {h})',
            setup='from __main__ import build_tree_iterative',
            number=repeat
        ) / repeat

        recursive_times.append(rec_time)
        iterative_times.append(it_time)

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(heights, recursive_times, marker='o', label='Рекурсивная')
    plt.plot(heights, iterative_times, marker='s', label='Нерекурсивная')
    plt.xlabel('Высота дерева')
    plt.ylabel('Время построения (сек)')
    plt.title('Сравнение времени построения бинарного дерева')
    plt.legend()
    plt.grid(True)
    plt.show()

    return heights, recursive_times, iterative_times


if __name__ == "__main__":
    compare_build_times(max_height=12, repeat=5)
