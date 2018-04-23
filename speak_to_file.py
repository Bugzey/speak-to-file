#   Read stdin, pass to espeak, convert to ogg
from shutil import which
from os import system, remove
from shlex import parse as shlex_split
import subprocess

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
