from git import Repo
import os

BASE_PATH = "./storage/repo"

def clone_repo(repo_url, project_id):
    path = os.path.join(BASE_PATH , project_id)

    if os.path.exists(path):
        return path

    repo.clone_from(repo_url , path)
    return path