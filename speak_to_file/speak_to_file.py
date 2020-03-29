#!/usr/bin/python
#   Speak-to-file
#   Read stdin, pass to espeak, convert to ogg
#   
#   Copyright (C) 2018 Radoslav Dimitrov
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

####################################################################################################
#   Input settings
####################################################################################################

"""Speak to file

Usage: speak_to_file [options] [-]

Options:
    -h, --help  Display this help message
    -l, --license  Display license
    -v, --verbose  More output
    -o, --output=FILE  Set output file path
    --reader=READER  Set path to TTS application
    --converter=CONVERTER  Set path to file converter
    --version  Print version information
"""

__version__ = "0.1.0"


####################################################################################################
#   Libraries
####################################################################################################

from shutil import which
import os
import sys
import subprocess
from docopt import docopt

import logging
logger = logging.getLogger(__name__)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(msg)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


####################################################################################################
#   Globals
####################################################################################################

#   GPL Notice
GPL_NOTICE = """
speak-to-file Copyright (C) 2018  Radoslav Dimitrov
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions. For more information please visit: 
https://www.gnu.org/licenses/gpl-3.0.en.html
"""


####################################################################################################
#   Define external software
####################################################################################################

def set_up(reader = None, converter = None):
    #   Default behaviour: check if several open-source programs are available and pick one
    #   TTS and conversion command
    supported_readers = ['espeak', 'festival', 'flite', 'mimic']
    supported_converters = ['ffmpeg', 'avconv', 'oggenc', 'opusenc', 'lame']
    installed_readers = zip(supported_readers, map(which, supported_readers))
    installed_converters = zip(supported_converters, map(which, supported_converters))
    
    if not installed_readers or not installed_converters:
        if not installed_readers:
            logger.error(f'Error! No supported TTS engines found: {", ".join(supported_readers)}')
        
        if not installed_converters:
            logger.error(f'Error! No supported media converters found: {", ".join(supported_converters)}')

        if reader is not None and reader not in installed_reader:
            logger.error(f"Desired reader not found or supported: {reader}")

        if converter is not None and converte not in installed_convertes:
            logger.error(f"Desired converter not found or supported: {converter}")
    
        sys.exit(1)
    
    #   Command-line arguemnts for each supported platform
    reader_args = {
        'espeak': ['-s', '195', '--stdout', '-f'],
        'festival': None,
        'flite': None,
        'mimic': None
    }
    converter_args = {
        'ffmpeg': ['-hide_banner', '-i', 'pipe:0',  '-c:a', 'libvorbis',  '-q:a', '1', '-ac', '1', '-ar', '22050', '-y'],
        'avconv': ['-hide_banner', '-i', 'pipe:0',  '-c:a', 'libvorbis',  '-q:a', '1', '-ac', '1', '-ar', '22050', '-y'],
        'oggenc': ['-q', '1', '--resample', '22050', '--downmix', '-', '-o'],
        'opusenc': ['--bitrate', '32', '--vbr', '--downmix-mono', '-'],
        'lame': ['-V', '8', '-m', 'm', '-']
    }
    converter_extensions = {
        'ffmpeg': '.ogg',
        'avconv': '.ogg',
        'oggenc': '.ogg',
        'opusenc': '.ogg',
        'lame': '.mp3'
    }
    
    cur_reader = [{"command": reader, "path": path} for (reader, path) in installed_readers if path is not None][0]
    cur_converter = [{"command": converter, "path": path} for (converter, path) in installed_converters if path is not None][0]

    #   Add appropriate args
    cur_reader["args"] = reader_args[cur_reader["command"]]
    cur_converter["args"] = converter_args[cur_converter["command"]]
    cur_converter["extension"] = converter_extensions[cur_converter["command"]]

    logger.debug(cur_reader)
    logger.debug(cur_converter)
    
    return (cur_reader, cur_converter)


def read_stdin():
    #   Stdin
    text = []
    while True:
        try:
            text.append(input())
        except EOFError:
            break
        except KeyboardInterrupt:
            print()
            sys.exit(0)
    
    text = list(filter(lambda x: x.isspace() or len(x) != 0, text))
    title = text[0][:99]
    #   Remove invalid characters from title
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for item in invalid_chars:
        title.replace(item, '')

    #   Combine text list items to a single string
    text = '\n'.join(text)
    text_file = os.path.join("/tmp/", title)

    return(text, title, text_file)


def execute_read_convert(out_dir, out_file, text, title, text_file, cur_reader, cur_converter):
    with open(text_file, 'w+') as file_object:
        file_object.write(text)
        file_object.close()
    
    out_dir = os.getcwd() if out_dir == "" else out_dir
    logger.debug(f"Processed out_dir: {out_dir}")

    if out_file == "":
        out_file = f"{title}{cur_converter['extension']}"
    else:
        given_extension = os.path.splitext(out_file)[1]
        expected_extension = cur_converter["extension"]

        if given_extension != expected_extension:
            logger.warn(f"Given extension: {given_extension} not supported; replacing with {expected_extension}")
            out_file = out_file.replace(given_extension, expected_extension)
        else:
            out_file = out_file

    logger.debug(f"Processed out_file: {out_file}")

    final_out = os.path.join(out_dir, out_file)
    assert not os.path.exists(final_out), f"File already exists: {final_out}"

    #   Add filenames to commands
    cur_reader["args"].append(text_file)
    cur_converter["args"].append(final_out)
    
    logger.debug(f"Final reader command: {[cur_reader['command'], *cur_reader['args']]}")
    logger.debug(f"Final converter command: {[cur_converter['command'], *cur_converter['args']]}")

    reader_proc = subprocess.Popen([cur_reader["command"], *cur_reader["args"]], stdin = None, stdout = subprocess.PIPE)
    convert_proc = subprocess.Popen([cur_converter["command"], *cur_converter["args"]], stdin = reader_proc.stdout)
    
    try:
        while reader_proc.poll() is None or convert_proc.poll() is None:
            pass
    except Exception as e:
        logger.error(e)
    finally:
        #   Cleanup
        logger.debug(f"Removing temporary file: {text_file}")
        os.remove(text_file)


def main():
    args = docopt(__doc__, sys.argv[1:])
    loglevel = logging.DEBUG if args["--verbose"] else logging.WARN
    logger.setLevel(loglevel)
    logger.debug(args)
    
    if args["--license"]:
        print(GPL_NOTICE)
        sys.exit(0)

    if args["--version"]:
        print(__version__)
        sys.exit(0)

    #   Output destination validation
    if args["--output"]:
        output = args["--output"]
        out_dir, out_file = os.path.split(output)
        logger.debug(f"Out dir: {out_dir}")
        logger.debug(f"Out file: {out_file}")
        assert os.path.exists(out_dir), f"Path does not exist: {out_dir}"
        if out_file != "":
            assert not os.path.exists(output), f"File already exists: {output}"
    else:
        output = None
        out_dir = ""
        out_file = ""

    if args["--reader"]:
        logger.warn(f"Unimplemented: {args['--reader']}")

    if args["--converter"]:
        logger.warn(f"Unimplemented: {args['--reader']}")

    logger.debug(f"Output split: {output}")

    reader = args["--reader"]
    converter = args["--converter"]

    #   Execute
    reader_command, converter_command = set_up(reader, converter)
    text, title, text_file = read_stdin()
    execute_read_convert(out_dir, out_file, text, title, text_file, reader_command, converter_command)
    logger.debug("Finished execution")


if __name__ == "__main__":
    main()

