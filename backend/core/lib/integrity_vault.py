def open_with_integrity(path, mode='r'):
    import os
    if not os.path.exists(path):
        raise PermissionError("Unauthorized file access attempt")
    return open(path, mode)
