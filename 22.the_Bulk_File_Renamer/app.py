import os

def rename_files(folder_path, prefix):
    try:
        files = os.listdir(folder_path)
        for count, filename in enumerate(files):
            file_ext = os.path.splitext(filename)[1]
            new_name = f"{prefix}_{count+1}{file_ext}"
            src = os.path.join(folder_path, filename)
            dst = os.path.join(folder_path, new_name)
            os.rename(src, dst)
            print(f"Renamed: {filename} -> {new_name}")
    except Exception as e:
        print(f"Error: {e}")

folder = input("Enter the path to the folder: ")
prefix = input("Enter the prefix for new filenames: ")
rename_files(folder, prefix)
