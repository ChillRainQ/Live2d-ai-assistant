import os
def get_files_in_dir(dir_path):
    all_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".py"):
                continue
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files