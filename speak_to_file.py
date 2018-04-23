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

from shutil import which
from os import system, remove
from shlex import parse as shlex_split
import subprocess

#   GPL Stuff
gpl_notice = """
    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
"""
#   TODO: add terminal interaction: https://www.gnu.org/licenses/gpl-3.0.en.html

text = []
while True:
    try:
        text.append(input())
    except EOFError:
        break

text = list(filter(lambda x: x != '\n', text))
title = text[0]
text = '\n'.join(text)
text_file = f'/tmp/{title}'
open(text_file, 'w').write(text)

#reader_command = which('espeak')
#convert_command = which('ffmpeg')

#convert_options = f'-hide_banner -i pipe:0 -c:v libvorbis -q:a 1 -ac 1 -ar 22050 -y "{title}".ogg'
reader_command = [which('espeak'), '-s', '195', '-f', text_file, '--stdout']
convert_command = [which('ffmpeg'), '-hide_banner', '-i', 'pipe:0', '-c:v', 'libvorbis', '-q:a', '1', '-ac', '1', '-ar', '22050', '-y', f'{title}.ogg']

#system(f'{reader_command} {reader_options} | {convert_command} {convert_options}')
reader_proc = subprocess.Popen(reader_command, stdout = subprocess.PIPE)
convert_proc = subprocess.Popen(convert_command, stdin = reader_proc.stdout)

while convert_proc.poll() is None:
    pass

remove(text_file)
