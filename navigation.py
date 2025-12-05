import os
import ctypes
from datetime import datetime
from typing import List, Dict, Tuple, Any
import utils

def get_current_drive() -> str:
    """Получение текущего диска Windows"""
    # TODO: Вернуть текущий диск (например: "C:")
    # Использовать os.path.splitdrive()
    current_path = os.getcwd()
    drive, _ = os.path.splitdrive(current_path)
    if drive:
        return drive
    # В случае, если не определился, возвращаем диск C:
    return 'C:'
    pass

def list_available_drives() -> List[str]:
    """Получение списка доступных дисков Windows"""
    # TODO: Вернуть список доступных дисков (['C:', 'D:', ...])
    # Использовать os.listdir('/') не подойдет для Windows!
    # Исследовать: использовать win32api или другие методы
    drives_bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    drives = []
    for i in range(26):
        if drives_bitmask & (1 << i):
            drive_letter = chr(65 + i) + ':'
            drives.append(drive_letter)
    return drives
    pass

def list_directory(path: str) -> Tuple[bool, List[Dict[str, Any]]]:
    """Отображение содержимого каталога в Windows"""
    # TODO: Используя utils.safe_windows_listdir(), получить содержимое
    # Для каждого элемента вернуть словарь с информацией:
    # {'name': 'file.txt', 'type': 'file', 'size': 1024, 'modified': '2024-01-15', 'hidden': False}
    # Использовать utils.is_hidden_windows_file() для проверки скрытых файлов
    # Вернуть (True, данные) при успехе, (False, []) при ошибке
    entries = []
    try:
        items = utils.safe_windows_listdir(path)
        for item in items:
            full_path = os.path.join(path, item)
            is_hidden = utils.is_hidden_windows_file(full_path)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path) if not is_dir else 0
            modified_time = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d')
            entries.append({
                'name': item,
                'type': 'folder' if is_dir else 'file',
                'size': size,
                'modified': modified_time,
                'hidden': is_hidden
            })
        return True, entries
    except Exception:
        return False, []
    pass

def format_size(size_bytes: int) -> str:
    # Форматирование размера файла
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"
    pass

def format_directory_output(items: List[Dict[str, Any]]) -> None:
    """Форматированный вывод содержимого каталога для Windows"""
    # TODO: Красиво отформатировать вывод используя данные из list_directory()
    # Учесть что в Windows есть системные и скрытые файлы
    # Показать диски если находимся в корне
    if not items:
        print("Пустая директория.")
        return
    for item in items:
        name = item['name']
        type_icon = '[D]' if item['type'] == 'folder' else '[F]'
        size_str = format_size(item['size']) if item['type'] == 'file' else ''
        hidden_marker = '(скрыто)' if item['hidden'] else ''
        print(f"{type_icon} {name} {size_str} {hidden_marker}")
    pass

def move_up(current_path: str) -> str:
    """Переход в родительский каталог в Windows"""
    # TODO: Использовать utils.get_parent_path() для получения родителя
    # Проверить валидность нового пути через utils.validate_windows_path()
    # Учесть переход между дисками
    parent_path = utils.get_parent_path(current_path)
    valid, msg = utils.validate_windows_path(parent_path)
    if valid:
        return parent_path
    else:
        print(f"Не удалось перейти в родительский каталог: {msg}")
        return current_path
    pass

def move_down(current_path: str, target_dir: str) -> Tuple[bool, str]:
    """Переход в указанный подкаталог в Windows"""
    # TODO: Проверить что target_dir существует через utils.safe_windows_listdir()
    # Сформировать новый путь и проверить через utils.validate_windows_path()
    # Вернуть (True, новый_путь) при успехе, (False, текущий_путь) при ошибке
    new_path = os.path.join(current_path, target_dir)
    valid, msg = utils.validate_windows_path(new_path)
    if valid:
        return True, new_path
    else:
        print(f"Ошибка при переходе: {msg}")
        return False, current_path
    pass

def get_windows_special_folders() -> Dict[str, str]:
    """Получение путей к специальным папкам Windows"""
    # TODO: Вернуть словарь с путями к папкам:
    # {'Desktop': 'C:\\Users\\...', 'Documents': '...', 'Downloads': '...'}
    # Использовать os.environ для получения USERPROFILE и других переменных
    user_profile = os.environ.get('USERPROFILE', '')
    return {
        'Desktop': os.path.join(user_profile, 'Desktop'),
        'Documents': os.path.join(user_profile, 'Documents'),
        'Downloads': os.path.join(user_profile, 'Downloads')
    }
        pass
