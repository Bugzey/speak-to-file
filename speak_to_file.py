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
#   Libraries
####################################################################################################

from shutil import which
from os import system, remove
from shlex import quote, split
import subprocess


####################################################################################################
#   Settings
####################################################################################################

#   Read settings in order: /etc/speak_to_file.conf, $HOME/config/speak_to_file.conf,
#   $HOME/.speak_to_file.conf, (current dir)/speak_to_file.conf
#   TODO: settings

#   Command-line settings
#   TODO: command-line settings
#   -h  print help
#   -l  print license
#   -o  set out file
#   --reader set reader name or path
#   --converter set converter name or path

####################################################################################################
#   Console interaction
####################################################################################################

#   GPL Stuff
gpl_notice = """
    speak_to_file  Radoslav Dimitrov
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
"""
#   TODO: add terminal interaction: https://www.gnu.org/licenses/gpl-3.0.en.html


####################################################################################################
#   Define external software
####################################################################################################

#   Default behaviour: check if several open-source programs are available and pick one
#   TTS and conversion command
supported_readers = ['espeak', 'festival', 'flite', 'mimic']
supported_converters = ['ffmpeg', 'avconv', 'oggenc', 'opusenc', 'lame']
installed_readers = list(filter(lambda x: which(x), supported_readers))
installed_converters = list(filter(lambda x: which(x), supported_converters))

#   Command-line arguemnts for each supported platform
reader_args = {
    'espeak': '-s 195 --stdout -f',
    'festival': None,
    'flite': None,
    'mimic': None
}
converter_args = {
    'ffmpeg': '-hide_banner -i pipe:0 -c:v libvorbis -q:a 1 -ac 1 -ar 22050 -y',
    'avconv': None,
    'oggenc': None,
    'opusenc': None,
    'lame': None
}
cur_reader = installed_readers[0]
cur_converter = installed_converters[0]

reader_command = [which('espeak'), '-s', '195', '--stdout', '-f']
convert_command = [which('ffmpeg'), '-hide_banner', '-loglevel', 'error', '-i', 'pipe:0', '-c:v', 'libvorbis', '-q:a', '1', '-ac', '1', '-ar', '22050', '-y']

#   Stdin
text = []
while True:
    try:
        text.append(input())
    except EOFError:
        break

text = list(filter(lambda x: x.isspace() or len(x) != 0, text))
title = text[0]
text = '\n'.join(text)
text_file = f'/tmp/{title}'
with open(text_file, 'w') as cur_file:
    cur_file.write(text)
    cur_file.close()

reader_proc = subprocess.Popen(reader_command + [f'{text_file}'], stdout = subprocess.PIPE)
convert_proc = subprocess.Popen(convert_command + [f'{title}.ogg'], stdin = reader_proc.stdout)
#   TODO: finish adding other reader options

while reader_proc.poll() is None or convert_proc.poll() is None:
    pass

#   Cleanup
remove(text_file)
