import os
import logging


def configure_logger(log_file_path, log_level):
    app_dir = os.path.dirname(log_file_path)
    var_dir = os.path.join(app_dir, "var")
    os.makedirs(var_dir, exist_ok=True)
    log_file_path = os.path.join(var_dir, os.path.basename(log_file_path))

    logger = logging.getLogger("py-store-logger")
    logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file_path, mode="w")
    file_handler.setLevel(log_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
