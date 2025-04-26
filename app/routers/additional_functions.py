from pathlib import Path
import zipfile
import rarfile
import os


async def arch_to_folder(path: str) -> str:
    match path.split('.')[-1]:
        case "rar":
            new_file_name = await unrar_file(path)
            return new_file_name
        case "zip":
            new_file_name = await unzip_file(path)
            return new_file_name
        case _:
            return "Unsupported file type"



async def unrar_file(path: str) -> str:
    folder = os.path.dirname(path)
    with rarfile.RarFile(path) as rar_ref:
        rar_ref.extractall(folder)
    os.remove(path) 
    return folder


async def unzip_file(path: str) -> str:
    with zipfile.ZipFile(path, 'r') as zip_ref:
        new_path = path.split("/")
        new_path = "/".join(new_path[:-1])
        zip_ref.extractall(new_path)
    os.remove(path)
    return new_path


async def get_file_names_from_folder(path: str) -> list[str]:
    folder = Path(path)
    file_names = [
        i.name
        for i in folder.iterdir()
        if i.is_file() and i.name.endswith(".json")
    ]
    return file_names


async def clear_temp_files(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)