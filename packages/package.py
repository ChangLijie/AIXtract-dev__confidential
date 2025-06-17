import os
import shutil
from pathlib import Path

# Project Ori name & Temp name
ORIG_NAME = "AIXtract-dev__confidential"
TEMP_NAME = "AIXtract"

MODULE_LIST = [
    "converter",
    "evaluator",
    "GenAIServices",
    "metrics",
    "models",
    "preprocessor",
    "readers",
    "utils",
]

PACKAGES_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGES_DIR.parent
OUTPUT_DIR = "packages/AIXtract/"
EXCLUDE_DIRS = {"packages", "__pycache__"}


def should_exclude(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def collect_py_files(modules, base_path):
    py_files = []
    for module in modules:
        module_path = base_path / module
        for py_file in module_path.rglob("*.py"):
            if should_exclude(py_file.relative_to(base_path)):
                continue
            py_files.append(py_file)
    return py_files


def cleanup_temp_files(py_file: Path):
    c_file = py_file.with_suffix(".c")
    html_file = py_file.with_suffix(".html")
    if c_file.exists():
        c_file.unlink()
    if html_file.exists():
        html_file.unlink()

    pycache = py_file.parent / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        for f in pycache.glob(f"{py_file.stem}*.cpython*.so"):
            try:
                f.unlink()
            except Exception:
                pass


def build_so(py_file: Path, base_path: Path):
    rel_path = py_file.relative_to(base_path)
    out_dir = base_path / OUTPUT_DIR / rel_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[BUILD] {rel_path}")
    os.system(f"cythonize -3 -i {py_file}")

    so_name = None
    pycache_dir = py_file.parent / "__pycache__"
    stem = py_file.stem
    if pycache_dir.exists():
        for f in pycache_dir.glob(f"{stem}*.so"):
            so_name = f
            break
    if not so_name:
        for f in py_file.parent.glob(f"{stem}*.so"):
            so_name = f
            break
    if so_name and so_name.exists():
        shutil.move(str(so_name), str(out_dir / f"{stem}.so"))
        print(f"[MOVE] {so_name.name} → {out_dir}")
    else:
        print(f"❌ Can't find .so file for {rel_path}")

    cleanup_temp_files(py_file)


# def build_all_so():
#     all_py_files = collect_py_files(module_list)
#     if not all_py_files:
#         print("❌ Can't find .py.")
#         return
#     for py_file in all_py_files:
#         build_so(py_file)


def main():
    actual_project_root = PROJECT_ROOT
    renamed = False
    module_list = MODULE_LIST
    if PROJECT_ROOT.name == ORIG_NAME:
        temp_path = PROJECT_ROOT.parent / TEMP_NAME
        print(f"🔄 Rename folder name:  {TEMP_NAME} ...")
        PROJECT_ROOT.rename(temp_path)
        actual_project_root = temp_path
        renamed = True

    try:
        all_py_files = collect_py_files(module_list, base_path=actual_project_root)
        if not all_py_files:
            print("❌ Can't find .py file.")
            return
        for py_file in all_py_files:
            build_so(py_file, actual_project_root)
    finally:
        if renamed:
            print(f"🔙 Back folder name: {ORIG_NAME}")
            temp_path.rename(temp_path.parent / ORIG_NAME)


if __name__ == "__main__":
    main()
