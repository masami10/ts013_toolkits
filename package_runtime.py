import os
import shutil
from loguru import logger
os.environ['ENV_RUNTIME'] = 'prod'
try:
    if not os.path.exists('resources'):
        src = os.path.join(os.getcwd(), 'PyQt5', 'Qt', 'resources')
        shutil.copytree(src, 'resources')
    if not os.path.exists('translations'):
        src = os.path.join(os.getcwd(), 'PyQt5', 'Qt', 'translations')
        shutil.copytree(src, 'translations')
except Exception as e:
    logger.error(e)