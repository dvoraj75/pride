from pride.dialogs.error_dialog import ErrorDialog


def file_exception_handling(f):
    def wrapper(self, *args, **kwargs):
        try:
            f(self, *args, **kwargs)
        except PermissionError:
            ErrorDialog("Permission error", "Can't open this file: permission denied", self).show()
        except FileNotFoundError:
            ErrorDialog("File not found", "Can't open this file: file not found", self).show()
        except Exception as e:
            ErrorDialog("Unknown error", "Can't open this file: unknown error", self).show()
    return wrapper


def dir_exception_handling(f):
    def wrapper(self, *args, **kwargs):
        try:
            f(self, *args, **kwargs)
        except PermissionError:
            ErrorDialog("Permission error", "Can't open this directory: permission denied", self).show()
        except FileNotFoundError:
            ErrorDialog("File not found", "Can't open this directory: directory not found", self).show()
        except Exception as e:
            ErrorDialog("Unknown error", "Can't open this directory: unknown error", self).show()
    return wrapper

