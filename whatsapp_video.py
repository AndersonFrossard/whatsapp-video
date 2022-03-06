"""
https://pypi.org/project/ffmpy/
ffmpeg -i "original-file.mp4" -vcodec libx264 -acodec aac "output-file.mp4"
-vf scale="720:-1" (para setar width em 720p) ou -vf scale="iw/2:ih/2" (para reduzir em 50%)
bitrate suggestion: 320kbits

Ideia p ficar perfeito: avaliar SIZE após 1/10 do tempo e então multiplicar por 10 p/ estimar tamanho final
total. Se nao estiver dentro da faixa de segurança, então abortar e reduzir bitrate em 2min.

Seria bom tb se o programa adicionasse legendas. amarelinhas. ja pensou. perfeito.
Lembrando que o mediainfo informa em kbits/segundo. BITS

(a)
algumas opcoes para escolha de biblioteca
https://kkroening.github.io/ffmpeg-python/
https://github.com/kkroening/ffmpeg-python#readme

(b)
http://johnriselvato.com/how-to-use-ffmpeg-in-python/
https://pypi.org/project/ffmpy/
https://ffmpy.readthedocs.io/en/latest/ffmpy.html

Estou escolhendo opção (b) porque parece mais fácil.
Como trabalhar com sublime e python virtual env:
https://www.youtube.com/watch?v=5UlFHn6FBxk
https://www.sublimetext.com/docs/build_systems.html#basic_example

https://medium.com/@dsml.harsha/sublime-text-build
-result-window-to-the-right-side-of-the-screen-aa1cf5c3c898


import ffmpy
 
ff = ffmpy.FFmpeg(executable='C:\\ffmpeg\\bin\\ffmpeg.exe', inputs={path+'/Stage1Rap.wav': None}, outputs={path+'/FinalRap.mp3': ["-filter:a", "atempo=0.5"]})
ff.run()


def __init__(self, executable='D:\\FFmpeg\\bin\\ffmpeg.exe', global_options=None, inputs=None, outputs=None):
        self.executable = executable
        self._cmd = [executable]


-y (global)
Overwrite output files without asking.

-metadata title="my title"

-target vcd /tmp/vcd.mpg
opcoes disponiveis: vcd, svcd, dvd, dv, dv50


-nostats 
(para nao exibir o progresso)

-stats_period

-acodec (set the audio codec)

-scodec (set the subtitle codec)
ffmpeg -i input.mp4 -vf "subtitles=subtitle.srt" output.mp4


# o programa tem que ter opcao de cortar o video em N partes para 
# enviar em varias partes
"""

import ffmpy
from ffprobe import FFProbe
import sys
from colorama import init
from colorama import Fore, Back, Style
import os
import re

init()

def is_whatsapp_compatible(filename):
	ffprobe_file = FFProbe(filename)
	condition1 = (os.path.getsize(ffprobe_file.path_to_video) < 64000000) 
	condition2 = (ffprobe_file.metadata['major_brand'].lower() == 'isom')
	return condition1 and condition2

def get_warning_color(boolean_input):
	return get_red_color() if boolean_input else get_default_color()

def get_red_color():
	return '\033[31m'

def get_yellow_color():
	return '\033[33m'

def get_default_color():
	return '\033[39m'

def get_max_filesize():
	return 63000000

def get_filesize(filename):
	return os.path.getsize(filename)

def show_warning(filename):
	if (is_whatsapp_compatible(filename)):
		return get_yellow_color() + ' ** Whatsapp Ready **' + get_default_color()
	else:
		return get_red_color() + '   ** Not Whatsapp compatible ** ' + get_default_color()

def get_number_of_chunks(filename):
	return  (os.path.getsize(filename) // get_max_filesize() + 1)

def get_split_name(input, i=0):
	return	input[:-4] + f'_{str(i)}' + '_output' + input[-4:]

def get_name_with_suffix(input, suffix):
	return input[:-4] + f'_{suffix}' + input[-4:]

def get_time_in_secs(ffprobe_file):
	t1 = ffprobe_file.metadata['Duration']
	h, m, s, mm = re.split('[^0-9]', t1)
	temp_seg = int(h)*3600 + int(m)*60 + int(s)*1
	return (temp_seg-3)

def ask_to_continue(msg):
	answer = (input(msg)).lower()
	if (answer == 's' or answer == 'y'):
		return True
	return False

def is_resize_needed(filename):
	ffprobe_file = FFProbe(filename)
	for stream in ffprobe_file.streams:
		if stream.is_video():
			if (int(stream.width) > 720) or ( int(stream.height) > 720):
				return True
	return False

def resize_if_needed(filename):
	if (is_resize_needed(filename)):
		if not (ask_to_continue('File is too big. I will resize it first. (Y)es or (N)o ? ')):
			print("Program terminated by user.")
			exit(0)
		new_filename = get_name_with_suffix(filename, 'resized')
		resize_in_half(filename, new_filename)
		filename = new_filename
	return filename

def resize_in_half(input_filename, output_filename):
	arq_ffmpeg = 'C:/Program Files/ffmpeg/bin/ffmpeg.exe'
	bitrate = get_new_bitrate(input_filename)
	ff = ffmpy.FFmpeg(executable = arq_ffmpeg,
		inputs={input_filename: None},
		outputs={output_filename: ['-y', '-vf', 'scale=iw/2:ih/2', '-c:v', 'libx264', '-b:v', str(bitrate), '-c:a', 'aac']} )
	
	print(ff.cmd)
	ff.run()

def ask_and_convert(filename):
	if (not is_whatsapp_compatible(filename)):
		answer = (input("Do you wish converting to whatsapp compatible (Y/N) ? ")).lower()
		if (answer == 's' or answer == 'y'):
			print("Initiating conversion...")
			split_into_n_files(filename, get_number_of_chunks(filename)	)	


def get_new_bitrate(filename):
	new_bitrate = 0
	ffprobe_file = FFProbe(filename)
	for stream in ffprobe_file.streams:
		if stream.is_video():
			new_bitrate = int(int(stream.bit_rate) / 2)
	return new_bitrate



def print_info(filename):
	ffprobe_file = FFProbe(filename)
	for stream in ffprobe_file.streams:
		if stream.is_video():
			print(f'Major Brand..: {ffprobe_file.metadata["major_brand"]}' + show_warning(filename))
			print(f'Filesize.....: ' + str(get_filesize(filename))) 
			print(f'Tamanho......: {stream.frame_size()}')
			print(f'Pixel format.: {stream.pixel_format()}')
			print(f'Duração......: {stream.duration_seconds()} segundos')
			print(f'Codec........: {stream.codec()}')
			print(f'Codec desc...: {stream.codec_description()}')
			print(f'Codec tag....: {stream.__dict__.get("codec_tag_string", None)}')
			print(f'Bit rate.....: {stream.__dict__.get("bit_rate", "")} bits/seg')

		if stream.is_audio():
			print('Existe um stream de audio.')
			print(f'Tamanho......: {stream.frame_size()}')
			print(f'Pixel format.: {stream.pixel_format()}')
			print(f'Duração......: {stream.duration_seconds()} segundos')
			print(f'Codec........: {stream.codec()}')
			print(f'Codec desc...: {stream.codec_description()}')
			print(f'Codec tag....: {stream.__dict__.get("codec_tag_string", None)}')
			print(f'Bit rate.....: {stream.__dict__.get("bit_rate", "")} bits/seg')

	print(f'Para Whatsapp, teremos que dividir este arquivo em {get_number_of_chunks(filename)} parte(s).')

def split_into_n_files(filename, n_parts):
	print("Starting splitting file : " + filename + " into "+ str(n_parts) + " parts.")
	time_stack = 0;
	for i in range(1, n_parts+1):
		new_filename = get_split_name(filename, i)
		print(i, new_filename, time_stack)
		time_stack = time_stack + create_split_file(filename, new_filename, get_max_filesize(), time_stack )


def create_split_file(input_name, output_name, max_size, time_stack):
	arq_ffmpeg = 'C:/Program Files/ffmpeg/bin/ffmpeg.exe'
	max_size = str(max_size) 
	time_stack = str(time_stack)
	print(f'input: {input_name}, output: {output_name}')
	print(f'max_size: {max_size}, time_stack: {time_stack}')

	ff = ffmpy.FFmpeg(executable = arq_ffmpeg, inputs={input_name: None}, outputs={output_name: f'-y -fs {max_size} -ss {time_stack} -c:v copy -c:a copy'})
	print()
	print(ff.cmd)
	ff.run()
	ffprobe_file = FFProbe(output_name)
	return get_time_in_secs(ffprobe_file)


def main():
	#TODO:
	#verificar qual é o lado maior e se for maior q 720, fazer scale p 720, antes de dividir
	#https://ottverse.com/change-resolution-resize-scale-video-using-ffmpeg/
	#de repente é melhor dividir por 2 e mandar bala
	arguments = get_arguments()
	input_file = arguments[0]
	output_dir = './output/'
	arq_ffmpeg = 'C:/Program Files/ffmpeg/bin/ffmpeg.exe'
	arq_ffprobe = 'C:/Program Files/ffmpeg/bin/ffprobe.exe'
	sucess_message = "Execução encerrada  com sucesso"

	print("...Iniciando...")
	print_info(input_file)
	new_input_file = resize_if_needed(input_file)
	ask_and_convert(new_input_file)
	print(sucess_message)

def get_arguments():
	return sys.argv[1:]


if __name__ == '__main__':
	main()