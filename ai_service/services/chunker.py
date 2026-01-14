import os

def read_files(repo_path):
    files = []

    for root, dirs, filenames in os.walk(repo_path):
        if "node_modules" in root or ".git" in root :
            continue

        for file in filenames:
            if file.endwith((".js" , ".py", ".java", ".md")):
                files.append(os.path.join(root, file))
    
    return files

def chunk_code(file_path, chunk_size= 400):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(tect[i: i+chunk_size])

    return chunks