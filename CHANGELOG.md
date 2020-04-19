# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- More TTS engines

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
