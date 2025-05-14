import os
import json

KAGGLE_USERNAME = "miloskatanic"
NOTEBOOK_DIR = "examples"

for folder in os.listdir(NOTEBOOK_DIR):
    folder_path = os.path.join(NOTEBOOK_DIR, folder)
    if not os.path.isdir(folder_path) or folder.startswith("."):
        continue

    notebooks = [f for f in os.listdir(folder_path) if f.endswith(".ipynb")]
    if not notebooks:
        print(f"No notebook found in {folder}")
        continue

    notebook_file = notebooks[0]
    meta_data_path = os.path.join(folder_path, "kernel-metadata.json")

    metadata = {
        "id": f"{KAGGLE_USERNAME}/{folder.replace('_', '-')}",
        "title": folder.replace("_", " ").title(),
        "code_file": notebook_file,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": False,
        "auto_commit": False,
    }
    with open(meta_data_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f" Created: {meta_data_path}")
