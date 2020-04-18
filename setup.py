from setuptools import setup
from speak_to_file.__version__ import __version__

setup(
    name = "speak_to_file",
    version = __version__,
    description = "Speak and transcode text in a single step",
    url = "https://github.com/Bugzey/speak-to-file",
    author = "Radoslav Dimitrov",
    author_email = "radddi@abv.bg",
    license = "GPLv3",
    packages = ["speak_to_file"],
    install_requires = ["docopt"],
    zip_safe = False
)
