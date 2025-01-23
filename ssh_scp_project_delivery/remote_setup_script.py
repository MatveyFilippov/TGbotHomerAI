from setuptools import setup
from Cython.Build import cythonize
import glob


setup(
    name='ai', version="1.0.0", author="Homer",
    ext_modules=cythonize("settings.py"),
    zip_safe=False,
)
setup(
    name='ai', version="1.0.0", author="Homer",
    ext_modules=cythonize(
        glob.glob("ai/*.py") + glob.glob("ai/__database/*.py")
    ),
    zip_safe=False,
)
setup(
    name='tg_bot', version="1.0.0", author="Homer",
    ext_modules=cythonize(
        glob.glob("tg_bot/*.py") + glob.glob("tg_bot/tasks/*.py")  + glob.glob("tg_bot/tasks/dialog_states/*.py")
    ),
    zip_safe=False,
)
