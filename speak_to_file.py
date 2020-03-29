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
    -o, --output=FILE  Set output file path
    --reader=READER  Set path to TTS application
    --converter=CONVERTER  Set path to file converter
"""

####################################################################################################
#   Libraries
####################################################################################################

from shutil import which
from os import system, remove
import sys
import subprocess
from docopt import docopt


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

def set_up():
    #   Default behaviour: check if several open-source programs are available and pick one
    #   TTS and conversion command
    supported_readers = ['espeak', 'festival', 'flite', 'mimic']
    supported_converters = ['ffmpeg', 'avconv', 'oggenc', 'opusenc', 'lame']
    installed_readers = zip(supported_readers, map(which, supported_readers))
    installed_converters = zip(supported_converters, map(which, supported_converters))
    
    if not installed_readers or not installed_converters:
        if not installed_readers:
            print(f'Error! No supported TTS engines found: {", ".join(supported_readers)}')
        
        if not installed_converters:
            print(f'Error! No supported media converters found: {", ".join(supported_converters)}')
    
        sys.exit(1)
    
    cur_reader = [(reader, path) for (reader, path) in installed_readers if path is not None][0]
    cur_converter = [(converter, path) for (converter, path) in installed_converters if path is not None][0]
    
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
    
    reader_command = [cur_reader[1]] + reader_args[cur_reader[0]]
    converter_command = [cur_converter[1]] + converter_args[cur_converter[0]]

    return (reader_command, converter_command)


def read_stdin():
    #   Stdin
    text = []
    while True:
        try:
            text.append(input())
        except EOFError:
            break
    
    text = list(filter(lambda x: x.isspace() or len(x) != 0, text))
    title = text[0][:99]
    #   Remove invalid characters from title
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for item in invalid_chars:
        title.replace(item, '')

    #   Combine text list items to a single string
    text = '\n'.join(text)
    text_file = f'/tmp/{title}'

    result = {
        "text": text,
        "title": title,
        "text_file": text_file
    }

    return(result)


def execute_read_convert():
    with open(text_file, 'w+') as file_object:
        file_object.write(text)
        file_object.close()
    
    #   Add filenames to commands
    reader_command.append(text_file)
    converter_command.append(''.join([title, converter_extensions[cur_converter[0]]]))
    
    reader_proc = subprocess.Popen(reader_command, stdin = None, stdout = subprocess.PIPE)
    convert_proc = subprocess.Popen(converter_command, stdin = reader_proc.stdout)
    
    while reader_proc.poll() is None or convert_proc.poll() is None:
        pass
    
    #   Cleanup
    remove(text_file)


def main():
    args = docopt(__doc__, sys.argv[1:])
    print(args)


if __name__ == "__main__":
    main()

