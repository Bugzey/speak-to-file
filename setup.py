from setuptools import setup
from speak_to_file.speak_to_file import __version__

setup(
    name = "speak_to_file",
    version = __version__,
    description = "Speak and transcode text in a single step",
    url = "https://github.com/Bugzey/speak-to-file",
    author = "Radoslav Dimitrov",
    author_email = "radddi@abv.bg",
    license = "GPLv3",
    packages = ["speak_to_file"],
    zip_safe = False
)
