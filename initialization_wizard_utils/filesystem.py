import os
import re
import shutil
from pathlib import Path


def rm_files(files: list):
    for file in files:
        if os.path.isdir(file):
            shutil.rmtree(file, ignore_errors=False)
        else:
            os.remove(file)


def sed_remove_line_matching(pattern: str, file_to_modify: str):
    with open(file_to_modify, "r", encoding="utf-8") as f:
        lines = f.readlines()
    new_lines = [line for line in lines if not re.search(pattern, line)]
    with open(file_to_modify, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def sed_in_place(filepath: str, old_string: str, new_string: str):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if old_string not in content:
        return
    new_content = content.replace(old_string, new_string)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)


def sed_remove_range(filepath: str, start_pattern: str, end_pattern: str):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    new_lines = []
    in_delete_block = False
    for line in lines:
        if re.search(start_pattern, line):
            in_delete_block = True
        if not in_delete_block:
            new_lines.append(line)
        if in_delete_block and re.search(end_pattern, line):
            in_delete_block = False
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def replace_text_in_file(filepath: str, old_text: str, new_text: str):
    sed_in_place(filepath, old_text, new_text)
    hyphenated_old = old_text.replace("_", "-")
    hyphenated_new = new_text.replace("_", "-")
    sed_in_place(filepath, hyphenated_old, hyphenated_new)


def rename_item(old_path: str, old_name: str, new_name: str):
    old_path = Path(old_path)
    base = old_path.name
    new_base = base.replace(old_name, new_name)
    new_path = old_path.parent / new_base
    shutil.move(str(old_path), str(new_path))


def traverse_and_rename(source_path: Path, old_name: str, new_name: str):
    dirs_to_rename = []
    for path in source_path.rglob("*"):
        base = path.name
        if path.is_dir():
            if old_name in base:
                dirs_to_rename.append(str(path))
        else:
            replace_text_in_file(str(path), old_name, new_name)
            if old_name in base:
                rename_item(str(path), old_name, new_name)
    for path in sorted(dirs_to_rename, key=lambda p: -len(Path(p).parts)):
        rename_item(path, old_name, new_name)
