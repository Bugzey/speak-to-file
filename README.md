#	Speak-to-text micro application

## Description
Single-command application that passes a long text to a user's preferred Text-To-Speech (TTS)
program. The output is then automatically routed to a separately installed audio conversion program,
and the final result is an audio file in the current directory.


## Installation
Clone the repository via git or download the project zip file:
```
$ git clone https://github.com/Bugzey/speak-to-file.git
```

Buld using the `build` module:
```
$ python -m build --wheel
```

Install the module through pip:
```
$ pip install dist/*.whl
```

##  Usage
Upon installation the program becomes available as a system-wide script invoked via `$
speak_to_file`. When no command line options are given, then an audio file named after the first
non-whitespace line from the input text is created in the working directory.

```
Speak to file

Usage: speak_to_file [options] [-]

Options:
    -h, --help             Display this help message
    -l, --license          Display license
    -v, --verbose          More output
    -o, --output=FILE      Set output file path
    -y, --overwrite        Overwrite existing file
    --reader=READER        Set path to TTS application
    --reader-args=ARGS     Pass custom arguments to reader in the form "-key=value"
    --converter=CONVERTER  Set path to file converter
    --converter-args=ARGS  Pass custom arguments to converter in the form "-key=value"
    --version              Print program version and quit
```

## Current features
- Automatic selection among all supported TTS engines and audio converters
- Default output to the current working directory
- Console interaction:
  - argument parsing via `docopt`
  - configurable output directory and file name
- Long filenames are clipped
- Invalid characters in the file name are deleted
- Allow selection of and passing arguments to TTS engines and audio converters
- Unit tests

The program automatically detects what TTS engines and audio converters are installed.

Currently supported TTS engines:

- [X] espeak
- [ ] festival
- [ ] flite
- [ ] mimic

Supported audio converters:

- [X] ffmpeg
- [X] avconv
- [X] oggenc
- [X] opusenc
- [X] lame


## Changelog
Refer to [Changelog](./CHANGELOG.md)


## Licence
Speak-to-file is licenced under the GNU General Public Licence version 3 (GPLv3). For more
information visit <https://www.gnu.org/licenses/gpl-3.0.en.html>.

