from typing import Any, Dict
import fnmatch

PathString = str


def build_windows_tree_recursive(
    path: PathString,
    depth: int = 0,
    max_depth: int = 5
) -> Dict[str, Any]:
    """
    Рекурсивное построение дерева каталогов Windows
    """

    name = os.path.basename(path) or path
    tree = {
        "name": name,
        "type": "directory",
        "children": []
    }

    # Ограничение глубины
    if depth >= max_depth:
        return tree

    # Пропуск системных каталогов
    if utils.is_hidden_windows_file(path):
        return tree

    try:
        items = utils.safe_windows_listdir(path)
    except Exception:
        return tree

    for item in items:
        full_path = os.path.join(path, item)

        try:
            if os.path.isdir(full_path):
                subtree = build_windows_tree_recursive(
                    full_path,
                    depth + 1,
                    max_depth
                )
                tree["children"].append(subtree)
            else:
                tree["children"].append({
                    "name": item,
                    "type": "file"
                })
        except (PermissionError, OSError):
            continue

    return tree




#второе задание

from typing import Generator, Tuple, List, Set


def recursive_path_explorer(
    start_path: str,
    history: List[str] = None
) -> Generator[Tuple[str, List[str]], None, None]:
    """
    Рекурсивный генератор навигации с историей
    """

    if history is None:
        history = []

    visited: Set[str] = set()

    def _explore(path: str):
        if path in visited:
            return

        visited.add(path)
        history.append(path)

        yield path, history.copy()

        try:
            items = utils.safe_windows_listdir(path)
        except Exception:
            return

        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                yield from _explore(full_path)

        history.pop()

    yield from _explore(start_path)


#третье задание



def analyze_windows_structure_recursive(
    path: str,
    pattern: str = "*",
    level: int = 0
) -> List[Tuple[int, str, str]]:
    """
    Рекурсивный анализ структуры каталогов Windows
    """
    results: List[Tuple[int, str, str]] = []

    try:
        is_hidden = utils.is_hidden_windows_file(path)
        is_dir = os.path.isdir(path)

        if is_dir:
            item_type = "SYS" if is_hidden else "DIR"
        else:
            item_type = "HIDDEN_FILE" if is_hidden else "FILE"

        if fnmatch.fnmatch(os.path.basename(path), pattern):
            results.append((level, item_type, path))

        if is_dir:
            items = utils.safe_windows_listdir(path)
            for item in items:
                full_path = os.path.join(path, item)
                results.extend(
                    analyze_windows_structure_recursive(
                        full_path,
                        pattern,
                        level + 1
                    )
                )

    except (PermissionError, OSError):
        pass

    return results
