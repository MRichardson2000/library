import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler("library.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
