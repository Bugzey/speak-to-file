#	Speak-to-text micro application

## Description
Single-command application that passes a long text to a user's preferred Text-To-Speech (TTS)
program. The output is then automatically routed to a separately installed audio conversion
program, and the final result is an audio file in the current directory.

## Installation
Clone the repository via git: `$ git clone https://github.com/Bugzey/speak-to-file.git` or
download the python file `speak-to-text.py`.

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

## Usage
Run speak-to-file.py via the python interpreter: `$ python speak-to-file.py`. Paste the desired
text to the console. An audio file titled with the first non-whitespace line from the text input
is created in the current directory.

## Current features
- Automatic selection among all supported TTS engines and audio converters
- Output to the current working directory
- Long filenames are clipped
- Invalid characters in the file name are deleted

## Planned features
- Console interaction
- Help documentation
- More TTS engines

## Licence
Speak-to-file is licenced under the GNU General Public Licence version 3 (GPLv3). For more information
visit (https://www.gnu.org/licenses/gpl-3.0.en.html).
