import shutil
from pathlib import Path
from typing import List, Tuple, Callable, Optional, Dict

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z"],
}


def _unique_destination(dest_path: Path) -> Path:
    """
    Si dest_path existe, genera un nombre único: "name (1).ext", "name (2).ext", ...
    """
    if not dest_path.exists():
        return dest_path
    stem, suffix = dest_path.stem, dest_path.suffix
    i = 1
    while True:
        candidate = dest_path.with_name(f"{stem} ({i}){suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def _move_with_collision(src: Path, dst_folder: Path) -> Path:
    dst_folder.mkdir(parents=True, exist_ok=True)
    target = _unique_destination(dst_folder / src.name)
    shutil.move(str(src), str(target))
    return target


_DEFAULT_MESSAGES: Dict[str, str] = {
    "no_files": "No files to organize.",
    "moved": "✅ Moved {name} → {folder}",
    "moved_others": "📁 Moved {name} → Others",
}


def organize_files(
    source_folder: str,
    dest_folder: Optional[str] = None,
    progress_callback: Optional[Callable[[float], None]] = None,
    log_callback: Optional[Callable[[str], None]] = None,
    messages: Optional[Dict[str, str]] = None,
) -> List[Tuple[str, str]]:
    """
    Organiza archivos y devuelve una lista de movimientos [(dest_final, origen_inicial), ...]
    para poder deshacerlos después.
    """
    msgs = {**_DEFAULT_MESSAGES, **(messages or {})}

    source_path = Path(source_folder)
    dest_path = Path(dest_folder) if dest_folder else source_path

    files = [f for f in source_path.iterdir() if f.is_file()]
    total = len(files)

    moves: List[Tuple[str, str]] = []

    if total == 0:
        if log_callback:
            log_callback(msgs["no_files"])
        if progress_callback:
            progress_callback(1.0)
        return moves

    for i, file in enumerate(files, start=1):
        moved = False
        for folder, extensions in FILE_TYPES.items():
            if file.suffix.lower() in extensions:
                target_folder = dest_path / folder
                new_path = _move_with_collision(file, target_folder)
                moved = True
                moves.append((str(new_path), str(file)))  # (dest_final, origen_inicial)
                if log_callback:
                    log_callback(msgs["moved"].format(name=Path(new_path).name, folder=folder))
                break

        if not moved:
            other_folder = dest_path / "Others"
            new_path = _move_with_collision(file, other_folder)
            moves.append((str(new_path), str(file)))
            if log_callback:
                log_callback(msgs["moved_others"].format(name=Path(new_path).name))

        if progress_callback:
            progress_callback(i / total)

    return moves