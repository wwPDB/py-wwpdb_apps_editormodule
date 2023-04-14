import os


def get_template_file_path():
    """Returns path to templates"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "templates"))
