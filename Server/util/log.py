import logging

def loginit():
    logger = logging.getLogger("http-server")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - [%(process)d-%(thread)d] - [%(funcName)s - %(lineno)d] - %(levelname)s - %(message)s")

    fh = logging.FileHandler("http-server.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

