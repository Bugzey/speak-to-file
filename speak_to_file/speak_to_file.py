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
    -h, --help             Display this help message
    -l, --license          Display license
    -v, --verbose          More output
    -o, --output=FILE      Set output file path
    -y, --overwrite        Overwrite existing file
    --reader=READER        Set path to TTS application
    --reader-args=ARGS     Pass custom arguments to reader in the form "-key=value"
    --converter=CONVERTER  Set path to file converter
    --converter-args=ARGS  Pass custom arguments to converter in the form "-key=value"
    --version              Print version information
"""

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
from speak_to_file.__version__ import __version__

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

def replace_invalid_chars(input_string):
    """
    Replace characters that are not allowed as parts of file names in Windows

    Inputs:
        input_string: string to be cleansed
    """
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for item in invalid_chars:
        input_string = input_string.replace(item, '')

    return(input_string)


def glue_args(args_dict):
    """Glue together command args for use in subprocess.Popen

    Inputs:
        args_dict: dictionary of arguments to be passed on

    Returns:
        List of arguments in input dict keys and items are a sequence,
            and only keys if the keys' value is Boolean
    """
    result_list = [[key, value] if value != True else [key] for key, value in args_dict.items() if value != False]
    result = [item for pair in result_list for item in pair]
    return(result)


def split_args(args_string):
    """
    Parse input downstream commandline arguments and split them into something
        resembling the output from docopt

    Inputs:
        args_string: string of arguments, formatted "key1=value1,key2=value2", 
            it is left for the user to pass short or long arguments correctly
            e.g. to change the language in espeak: "-v=de"
    Outputs:
        Dictionary of keys and items

    Raises:
        AssertionError if any argument has more than one key/item delimeter "="
    """
    arg_pairs = args_string.split(",")
    args_list = [item.split("=") for item in arg_pairs]

    assert max(map(len, args_list)) == 2, \
        "Invalid argument string: {args_string}"

    args_dict = {item[0]: True if item[1] == "" else item[1] for item in args_list}

    return(args_dict)


def set_up(reader = None, converter = None):
    #   Default behaviour: check if several open-source programs are available and pick one
    #   TTS and conversion command
    supported_readers = ['espeak', 'festival', 'flite', 'mimic']
    supported_converters = ['ffmpeg', 'avconv', 'oggenc', 'opusenc', 'lame']

    installed_readers = {reader: {"command": reader, "path": which(reader)} for reader in supported_readers if which(reader) is not None}
    installed_converters = {converter: {"command": converter, "path": which(converter)} for converter in supported_converters if which(converter) is not None}
    
    assert any(installed_readers), \
        f"No supported readers installed: {', '.join(supported_readers)}"
    assert any(installed_converters), \
        f"No supported converters installed: {', '.join(supported_converters)}"
    assert reader is None or reader in installed_readers, \
        f"Desired reader not found or supported: {reader}"
    assert converter is None or converter in installed_converters, \
        f"Desired converter not found or supported: {converter}"
    
    #   Command-line arguemnts for each supported platform
    reader_args = {
        'espeak': {'-s': '195', '--stdout': True},
        'festival': {},
        'flite': {},
        'mimic': {}
    }
    converter_args = {
        'ffmpeg': {'-hide_banner': True, '-i': 'pipe:0',  '-c:a': 'libvorbis',  '-q:a': '1', '-ac': '1', '-ar': '22050', '-y': True},
        'avconv': {'-hide_banner': True, '-i': 'pipe:0',  '-c:a': 'libvorbis',  '-q:a': '1', '-ac': '1', '-ar': '22050', '-y': True},
        'oggenc': {'-q': '1', '--resample': '22050', '--downmix': True, '-': True},
        'opusenc': {'--bitrate': '32', '--vbr': True, '--downmix-mono': True, '-': True},
        'lame': {'-V': '8', '-m': 'm', '-': True}
    }
    converter_extensions = {
        'ffmpeg': '.ogg',
        'avconv': '.ogg',
        'oggenc': '.ogg',
        'opusenc': '.ogg',
        'lame': '.mp3'
    }
    add_reader_input = {
        # how to modify reader_args to include a named output file
        "espeak": lambda x, y: {**x, **{"-f": y}},
    }
    add_converter_output = {
        "ffmpeg": lambda x, y :{**x, **{"--": y}},
        "avconv": lambda x, y :{**x, **{"--": y}},
        "oggenc": lambda x, y: {**x, **{"-o": y}},
        "opusenc": lambda x, y :{**x, **{"--": y}},
        "lame": lambda x, y :{**x, **{"": y}},
    }

    logger.debug(installed_readers)
    logger.debug(installed_converters)

    if reader is None:
        cur_reader = installed_readers[list(installed_readers.keys())[0]]
    else:
        cur_reader = installed_readers[reader]

    if converter is None:
        cur_converter = installed_converters[list(installed_converters.keys())[0]]
    else:
        cur_converter = installed_converters[converter]
    
    #   Add appropriate args
    cur_reader["args"] = reader_args[cur_reader["command"]]
    cur_converter["args"] = converter_args[cur_converter["command"]]
    cur_converter["extension"] = converter_extensions[cur_converter["command"]]

    #   Add input / output function
    cur_reader["add_input"] = add_reader_input[cur_reader["command"]]
    cur_converter["add_output"] = add_converter_output[cur_converter["command"]]

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
    title = replace_invalid_chars(title)

    #   Combine text list items to a single string
    text = '\n'.join(text)
    text_file = os.path.join("/tmp/", title)

    return(text, title, text_file)


def execute_read_convert(out_dir, out_file, text, title, text_file, cur_reader, cur_converter, overwrite = False, reader_args = None, converter_args = None):
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

        if given_extension == "":
            out_file = f"{out_file}{expected_extension}"
        elif given_extension != expected_extension:
            logger.warn(f"Given extension: {given_extension} not supported; replacing with {expected_extension}")
            out_file = out_file.replace(given_extension, expected_extension)
        else:
            out_file = out_file

    out_file = replace_invalid_chars(out_file)

    logger.debug(f"Processed out_file: {out_file}")

    final_out = os.path.join(out_dir, out_file)
    assert overwrite or not os.path.exists(final_out), f"File already exists: {final_out}"

    #   Add custom arguments to commands
    if reader_args is not None:
        cur_reader["args"] = {**cur_reader["args"], **reader_args}

    if converter_args is not None:
        cur_converter["args"] = {**cur_converter["args"], **converter_args}

    #   Add filenames to commands
    cur_reader["args"] = cur_reader["add_input"](cur_reader["args"], text_file)
    cur_converter["args"] = cur_converter["add_output"](cur_converter["args"], final_out)
    
    logger.debug(f"Final reader command: {[cur_reader['command'], glue_args(cur_reader['args'])]}")
    logger.debug(f"Final converter command: {[cur_converter['command'], glue_args(cur_converter['args'])]}")

    reader_proc = subprocess.Popen([cur_reader["command"]] + glue_args(cur_reader["args"]), stdout = subprocess.PIPE)
    convert_proc = subprocess.Popen([cur_converter["command"]] + glue_args(cur_converter["args"]), stdin = reader_proc.stdout)
    
    try:
        convert_proc.wait()
    except Exception as e:
        logger.error(e)
        convert_proc.kill()
        raise e
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

    reader = args["--reader"]
    converter = args["--converter"]
    overwrite = args["--overwrite"]

    #   Output destination validation
    if args["--output"]:
        output = args["--output"]
        out_dir, out_file = os.path.split(output)
        logger.debug(f"Out dir: {out_dir}")
        logger.debug(f"Out file: {out_file}")
        assert out_dir == "" or os.path.exists(out_dir), f"Path does not exist: {out_dir}"
        if out_file != "":
            assert overwrite or not os.path.exists(output), f"File already exists: {output}"
    else:
        output = None
        out_dir = ""
        out_file = ""

    logger.debug(f"Output split: {output}")

    #   Custom args processing
    if args["--reader-args"] is not None:
        reader_args = split_args(args["--reader-args"])
    else:
        reader_args = None

    logger.debug(f"reader_args: {reader_args}")

    if args["--converter-args"] is not None:
        converter_args = split_args(args["--converter-args"])
    else:
        converter_args = None

    logger.debug(f"converter_args: {converter_args}")

    #   Execute
    reader_command, converter_command = set_up(reader, converter)
    text, title, text_file = read_stdin()
    execute_read_convert(out_dir, out_file, text, title, text_file, reader_command, converter_command, overwrite, reader_args, converter_args)
    logger.debug("Finished execution")


if __name__ == "__main__":
    main()

