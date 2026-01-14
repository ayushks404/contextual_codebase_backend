from git import Repo
import os

BASE_PATH = "./storage/repos"

def clone_repo(repo_url: str, project_id: str) -> str:
    path = os.path.join(BASE_PATH , project_id)

    if os.path.exists(path) and os.path.isdir(path):
        return path

    os.makedirs(path, exist_ok=True)
    Repo.clone_from(repo_url , path)
    return path