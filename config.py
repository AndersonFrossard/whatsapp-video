from dotenv import dotenv_values, find_dotenv

class configuration(object):
	#todo: variaveis estaticas que terao seus valores definidos pelas funcoes abaixo
	# ta dando erro falando que ele nao consegue enxergar esse load_config+file
	#https://devnote.in/how-to-call-one-method-from-another-within-the-same-class-in-python/
	output_dir, arq_ffmpeg, arq_ffprobe, max_filesize = 0, 0, 0, 0

	def __init__(self):
		configuration.output_dir, configuration.arq_ffmpeg, configuration.arq_ffprobe, configuration.max_filesize = self.load_config_file()


	def get_config_file_default_settings(self):
		configuration_settings = dict()
		configuration_settings['output_location']  = './output/'
		configuration_settings['ffmpeg_location'] = 'c:/ffmpeg/bin/ffmpeg.exe'
		configuration_settings['ffprobe_location'] = 'c:/ffmpeg/bin/ffprobe.exe'
		configuration_settings['max_filesize_bytes'] = 15000000

		configuration_settings['output_dir_text'] = 'output_dir'
		configuration_settings['ffmpeg_path_text'] = 'path_ffmpeg'
		configuration_settings['ffprobe_path_text'] = 'path_ffprobe'
		configuration_settings['max_filesize_text'] = 'max_filesize'
		return configuration_settings

	def create_config_file(self, filename):
		configuration_settings = get_config_file_default_settings()

		output_dir_text = configuration_settings['output_dir_text']
		ffmpeg_text = configuration_settings['ffmpeg_path_text']
		ffprobe_text = configuration_settings['ffprobe_path_text']
		max_filesize_text = configuration_settings['max_filesize_text']

		output_location = configuration_settings['output_location']
		ffmpeg_location = configuration_settings['ffmpeg_location']
		ffprobe_location = configuration_settings['ffprobe_location']
		max_filesize = configuration_settings['max_filesize_bytes']

		with open (filename, 'w+') as f:
			f.write(f"{output_dir_text} = '{output_location}'\n")
			f.write(f"{ffmpeg_text} = '{ffmpeg_location}'\n")
			f.write(f"{ffprobe_text} = '{ffprobe_location}'\n")
			f.write(F"{max_filesize_text} = {max_filesize}\n")

	def load_config_file(self):	
		CONFIG_FILENAME = '.env'
		try:
			if not find_dotenv():
				create_config_file(CONFIG_FILENAME)
			config_dict = dotenv_values(CONFIG_FILENAME)
			output_dir = config_dict['output_dir']
			arq_ffmpeg = config_dict['path_ffmpeg'] # 'C:/Program Files/ffmpeg/bin/ffmpeg.exe'
			arq_ffprobe = config_dict['path_ffprobe'] #C:/Program Files/ffmpeg/bin/ffprobe.exe'
			max_filesize = config_dict['max_filesize']

			return output_dir, arq_ffmpeg, arq_ffprobe, max_filesize
		except Exception as error:
			exception_routine(error)


	def exception_routine(self,error):
		if type(error) == NameError:
			print('Could neither create nor locate .env configuration file.')
		if type(error) == IndexError:
			print('Opção inválida !! ')
		elif type(error) == KeyError:
			print('I wasnt able to read values from the configuration file.')
		elif type(error) == ValueError:
			print('Opção inválida. Somente números são permitidos.')
		else:
			print(str(error))
			print('Program Terminated.')
			raise SystemExit