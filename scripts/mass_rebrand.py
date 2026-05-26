import os

def rename_recursive(base_path):
    for root, dirs, files in os.walk(base_path, topdown=False):
        for name in files:
            if 'Spartan' in name or 'spartan' in name:
                old_path = os.path.join(root, name)
                new_name = name.replace('SpartanAI', 'SpartanAI').replace('Spartan', 'Spartan').replace('spartanai', 'spartanai').replace('spartan', 'spartan')
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
        for name in dirs:
            if 'Spartan' in name or 'spartan' in name:
                old_path = os.path.join(root, name)
                new_name = name.replace('SpartanAI', 'SpartanAI').replace('Spartan', 'Spartan').replace('spartanai', 'spartanai').replace('spartan', 'spartan')
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)

if __name__ == "__main__":
    rename_recursive('/mnt/c/GitHub/SpartanAI_Hub_Master')
