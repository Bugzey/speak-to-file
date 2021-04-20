# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- More TTS engines

##	[v0.4.0] - 2021-04-20
###	Added
- Build package using `setuptools` and following [PEP 517](https://www.python.org/dev/peps/pep-0517/)

##	[v0.3.1] - 2020-07-16
###	Fixed
- Use system-agnostic temporary file location

##	[v0.3.0] - 2020-04-19
###	Added:
- Allow selection of and passing arguments to TTS engines and audio converters

##	[v0.2.0] - 2020-03-30
###	Added:
- Console interaction:
    - argument parsing via docopt
    - configurable output directory and file name
- Some unit tests
- Package build using setuptools

## [v0.1.0] - 2018-07-02
###	Added:
- Automatic selection among all supported TTS engines and audio converters
- Default output to the current working directory
- Long filenames are clipped
- Invalid characters in the file name are deleted

[v0.4.0]: https://github.com/Bugzey/speak-to-file/releases/tag/v0.4.0

[v0.3.1]: https://github.com/Bugzey/speak-to-file/releases/tag/v0.3.1

[v0.3.0]: https://github.com/Bugzey/speak-to-file/releases/tag/v0.3.0

