import logging

logger = logging.getLogger("aiwb.cli")
log_format = logging.Formatter(
    "%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s"
)
handler = logging.StreamHandler()
handler.setFormatter(log_format)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
