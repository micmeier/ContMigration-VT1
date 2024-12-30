import os
import json

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    def create_node(name, path, is_file):
        node = {
            "label": name,
            "data": path.replace(rootdir, "").lstrip("/"),
            "expandedIcon": "pi pi-folder-open" if not is_file else "pi pi-file",
            "collapsedIcon": "pi pi-folder" if not is_file else "pi pi-file",
        }
        if not is_file:
            node["children"] = []
        return node

    def add_children(node, path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if item == "temp":
                continue
            if os.path.isdir(item_path):
                child_node = create_node(item, item_path, False)
                add_children(child_node, item_path)
                node["children"].append(child_node)
            else:
                node["children"].append(create_node(item, item_path, True))

    root_node = {"children": []}
    add_children(root_node, rootdir)
    return root_node["children"]

root_directory = "/home/ubuntu/contMigration_logs"
directory_structure = get_directory_structure(root_directory)

with open("directory_structure.json", "w") as f:
    json.dump({"data": directory_structure}, f, indent=4)