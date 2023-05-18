import os.path
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_env_path(env_prop):
    return os.path.join(get_project_root(), os.getenv(env_prop))


def get_env_val(env_prop):
    return os.getenv(env_prop)


def delete_files(dir, ext):
    test = os.listdir(dir)
    for item in test:
        if item.endswith(ext):
            os.remove(os.path.join(dir, item))


def list_files_with_content(directory):
    for child in Path(directory).iterdir():
        if child.is_file():
            print(f"{child.name}:\n{child.read_text()}\n")
