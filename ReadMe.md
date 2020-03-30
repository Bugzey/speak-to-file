#	Speak-to-text micro application

## Description
Single-command application that passes a long text to a user's preferred Text-To-Speech (TTS) program. The output is then automatically routed to a separately installed audio conversion program, and the final result is an audio file in the current directory.


## Installation
Clone the repository via git or download the project zip file:
```
$ git clone https://github.com/Bugzey/speak-to-file.git
```
Install the module through pip:
```
$ pip install /path/to/download/speak-to-file/
```

##  Usage
Run speak-to-file.py via the python interpreter: `$ python speak-to-file.py` or invoke it as a Python module `$ python -m speak_to_file`, and paste the desired text to the console. When no command line options are given, then an audio file named after the first non-whitespace line from the input text is created in the working directory.

```
Speak to file

Usage: speak_to_file [options] [-]

Options:
    -h, --help  Display this help message
    -l, --license  Display license
    -v, --verbose  More output
    -o, --output=FILE  Set output file path
    --reader=READER  Set path to TTS application
    --converter=CONVERTER  Set path to file converter
    --version  Print version information
```

## Current features
- Automatic selection among all supported TTS engines and audio converters
- Default output to the current working directory
- Console interaction:
  - argument parsing via `docopt`
  - configurable output directory and file name
- Long filenames are clipped
- Invalid characters in the file name are deleted

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


## Planned features
- More TTS engines
- Allow selection of and passing arguments to TTS engines and audio converters
- Unit tests

## Licence
Speak-to-file is licenced under the GNU General Public Licence version 3 (GPLv3). For more information
visit <https://www.gnu.org/licenses/gpl-3.0.en.html>.
