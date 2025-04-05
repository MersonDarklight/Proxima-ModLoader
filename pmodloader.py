import os
import subprocess
import time
import hashlib
import datetime
modsfolderex = 0
pfileblock = []
pscripts = []
proccount = 0



def log(message, show=True, ptime=False):
	ctime = datetime.datetime.now().strftime('%H:%M:%S')
	if show == True:
		if ptime == True:
			print(f"[{ctime}]: {message}")
		else:
			print(message)
	with open('pmodloader.log', 'a', encoding='utf-8') as f:
		f.write(f"[{ctime}]: {message}\n")

with open('pmodloader.log', 'w', encoding='utf-8') as f:
	f.write('')

log('Запуск Proxima ModLoader...')
log('Проверка наличия папки с модами...')

if(os.path.exists(os.path.abspath('.') + '\\mods')):
	log('Папка с модами существует.')
	modsfolderex = 1
	respath = os.path.abspath('gtaSA\\multiplayer\\mods\\deathmatch\\resources')
	workpath = os.path.abspath('.')
	modpath = workpath + '\\mods'
	log('Проверка структуры каталога модов...')
	tfolders = 0
	ffolders = 0
	cfolders = 0
	time.sleep(0.1)
	for root, dirs, files in os.walk(respath):
		tfolders = tfolders + 1
		print(f'Папок всего: {tfolders}', end='\r')
		time.sleep(0.001)

	time.sleep(0.5)
	print(f'Проверка структуры каталога модов [{ffolders}/{tfolders}]', end='\r')
	time.sleep(1)
	for root, dirs, files in os.walk(respath):
		path = root.replace(respath, '')
		dirr = modpath + path
		if os.path.exists(dirr):
			log(path+' существует.                             ')
			ffolders = ffolders + 1
		else:
			os.mkdir(dirr)
			log(path+' создана.                             ')
			cfolders = cfolders + 1
		print(f'Проверка структуры каталога модов [{ffolders}/{tfolders}]            ', end='\r')
		time.sleep(0.005)

	log(f'Проверка завершена. [{ffolders}/{tfolders}]                            ')
	if cfolders != 0:
		log(f'Создано папок: {cfolders}')
else:
	log('Папка с модами не найдена.')
	log('Проверка библиотек...')
	modsfolderex = 0
	piplibs = subprocess.Popen(["pip", "freeze"], encoding='cp866', shell=True, stdout=subprocess.PIPE)
	pipstd = piplibs.stdout.read()
	#print(pipstd)
	if('keyboard' in pipstd):
		log('keyboard установлен')
	else:
		yn = input('Сейчас будут установлены недостающие библиотеки. Продолжить?[Y/n]: ')
		if(yn.lower() == 'y'):
			log('установка keyboard...')
			os.system('pip install keyboard')
		else:
			log('выход...')
			time.sleep(2)
			exit()

	if('pyshortcuts' in pipstd):
		log('pyshortcuts установлен')
	else:
		log('установка pyshortcuts...')
		os.system('pip install pyshortcuts')

	if('gdown' in pipstd):
		log('gdown установлен')
	else:
		log('установка gdown...')
		os.system('pip install gdown')


import keyboard
import shutil
import gdown

import threading

import argparse

import ctypes

import requests
import json
import sys

log('')
log('Проверка актуальности...')

version = 'v0.0.4'
response = requests.get("https://api.github.com/repos/MersonDarklight/Proxima-ModLoader/releases/latest")
response.raise_for_status()
release = response.json()
log(f"Последний релиз: {release['tag_name']}, установлена: {version}.\n")
if version == release['tag_name']:
	log('Версия актуальна.')
else:
	log('Версия устарела.', False)
	print(f"Доступен новый релиз: {release['name']}.\nЧто нового:\n{release['body']}")
	if(input("\nУстановить? [Y/n]: ").lower() == 'y'):
		log('Скачивание обновлений...', False)
		os.execv(sys.executable, ['python', 'update.py'])
time.sleep(2)

parser = argparse.ArgumentParser(description='')
parser.add_argument("--m", default="game", help="work mode")
args = parser.parse_args()
mode = args.m

from pyshortcuts import make_shortcut

import re

started = 0

progresss = ''

print(os.path.abspath('.'))

blockpath = ''

def blockfile():
	#os.system('fileblock.py --f='+blockpath)
	global proccount
	process = subprocess.Popen(args=["python", "fileblock.py", "--f="+blockpath], shell=False, stdout=subprocess.PIPE)
	pfileblock.append(process)

	#f=open(blockpath)

def get_hash_md5(file):
	with open(file, 'rb') as f:
		m = hashlib.md5()
		while True:
			data = f.read(8192)
			if not data:
				break
			m.update(data)
		return m.hexdigest()	

def load_mods():
	global blockpath
	progresss = 'Загрузка модов...'
	respath = os.path.abspath('gtaSA\\multiplayer\\mods\\deathmatch\\resources')
	workpath = os.path.abspath('.')
	modpath = workpath + '\\mods'
	success = 0
	total = 0
	for root, dirs, files in os.walk(modpath):
		for dirname in dirs:
			#print(root, end ='\r')
			#print(dirname)
			path = root+'\\'+dirname
			#modpath = os.path.abspath(root+'\\'+dirname)
			for root2, dirs2, files2 in os.walk(path):
				for filename in files2:
					path = root2.replace(modpath, '')
					dirr = respath + path
					#print(dirr)
					#print(root2, end ='\r')
					total = total + 1
					try:
						modkey = get_hash_md5(root2+'\\'+filename)
						reskey = get_hash_md5(dirr+'\\'+filename)
						if(reskey == modkey):
							log(f'{filename} соответствует моду')
						else:
							log('Копируем '+filename+' в '+dirname)
							os.remove(dirr+'\\'+filename)
							shutil.copy(root2+'\\'+filename, dirr)
						success = success + 1
						log('Блокируем файл...\n')
					except:
						log('Ошибка.')
					blockpath=dirr+'\\'+filename
					t = threading.Thread(target=blockfile)
					t.start()
		break
	log(f'Моды успешно загружены![{success}/{total}]\n')
	time.sleep(1)

def scriptstdout():
	while True:
		for process in pscripts:
			output = process.stdout.readline()
			if output:
				scrname = str(process).split(':')[3]
				scrname = scrname.replace(" ['python', '",'')
				scrname = scrname.replace("']>",'')
				
				log(f'[{scrname}] >> ' + output.decode('utf-8').strip(), ptime=True)
		time.sleep(0.1)

def load_scripts():
	total = 0
	for root, dirs, files in os.walk('./scripts'):
		for file in files:
			with open('./scripts/'+file, 'r', encoding='utf-8') as f:
				ff = f.read()
				script = ff.split('\n')
				if 'pmodloader script' in script[0]:
					author = script[1].split(': ')[1]
					description = script[2].split(': ')[1]
					version = script[3].split(': ')[1]
					log(f'Загружается скрипт {file}[{version}] от {author}.\n{description}\n')
					process = subprocess.Popen(args=["python", "./scripts/"+file], shell=False, stdout=subprocess.PIPE)
					pscripts.append(process)
					total = total + 1
	if total > 0:
		log(f'Загружено скриптов: {total}.')
		pstdout = threading.Thread(target=scriptstdout, daemon=True)
		pstdout.start()
	else:
		log('Нет скриптов для загрузки.')
	pass

#def start():
#	threads = (
#		threading.Thread(target=close_gta),
#		threading.Thread(target=gtacheck, daemon=True)
#	)
#	for t in threads:
#		t.start()

def modloader_install():
	log('Установка...')
	log('Создание каталога для модов...')
	os.mkdir('mods')
	respath = os.path.abspath('gtaSA\\multiplayer\\mods\\deathmatch\\resources')
	workpath = os.path.abspath('.')
	modpath = workpath + '\\mods'
	tfolders = 0
	cfolders = 0
	time.sleep(0.1)
	for root, dirs, files in os.walk(respath):
		tfolders = tfolders + 1
		print(f'Папок всего: {tfolders}', end='\r')
		time.sleep(0.001)

	print(f'Создание каталогов.. [{cfolders}/{tfolders}]', end='\r')
	time.sleep(1)
	for root, dirs, files in os.walk(respath):
		path = root.replace(respath, '')
		#print(path)
		dirr = modpath + path
		log(path+' создан.                             ')
		cfolders=cfolders+1
		try:
			os.mkdir(dirr)
		except:
			pass
		for filename in files:
			pass
		print(f'Создание каталогов.. [{cfolders}/{tfolders}]', end='\r')
		time.sleep(0.005)
	log(f'Каталог для модов создан. [{cfolders}/{tfolders}]')
	gdown.download('https://drive.google.com/uc?id=1JR05KXbn3BITNuzZi-wS-s1esZXr1Ouh', 'icon.ico', quiet=False)
	gdown.download('https://drive.google.com/uc?id=1OzjgUbI3qIJIywzzC8unItkD_OoGGYO0', 'background_logo.png', quiet=False)
	gdown.download('https://drive.google.com/uc?id=1QMV8PIkzIYyOTinqMmq7YDKl795GtwFC', 'background.png', quiet=False)
	gdown.download('https://drive.google.com/uc?id=1jQJzgKEK4NyoxWGE0Pq3A4h212RzSLJk', 'mta_filler.png', quiet=False)
	gdown.download('https://drive.google.com/uc?id=1Ed6p2HWkIbQmvcn3DxZNIMU4N_aCqmhq', 'logo.png', quiet=False)
	gdown.download('https://drive.google.com/uc?id=1mVdSwIpXtRs7AxFliej-Y5n5d6YMcrdu', 'fileblock.py', quiet=False)

	f = open('start.bat', 'w')
	f.write(f'{workpath[0]}:\ncd {workpath}\ncls\npython {workpath}\\pmodloader.py')
	f.close()

	make_shortcut(workpath+'\\start.bat', name='Proxima ModLoader', icon=workpath+'\\icon.ico')

	cguipath = os.path.abspath('gtaSA\\multiplayer\\MTA\\cgui\\images')

	try:os.remove(cguipath+'\\background_logo.png')
	except:pass
	try:os.remove(cguipath+'\\background.png')
	except:pass
	try:os.remove(cguipath+'\\mta_filler.png')
	except:pass
	try:os.remove(modpath+'\\[proxima]spawn\\image\\logo.png')
	except:pass

	shutil.move('background_logo.png', cguipath)
	shutil.move('background.png', cguipath)
	shutil.move('mta_filler.png', cguipath)
	shutil.move('logo.png', modpath+'\\[proxima]spawn\\image\\')

	gdown.download('https://drive.google.com/uc?id=1LgboxwTk95nsWC_6OGb2NLnM8KFqoMIk', 'logo.png', quiet=False)
	try:os.remove(modpath+'\\[proxima]dxgui\\themes\\logo.png')
	except:pass
	shutil.move('logo.png', modpath+'\\[proxima]dxgui\\themes\\')

	os.system('cls')
	log('Установка завершена. Запустите модлоадер с ярлыка на рабочем столе.')
	time.sleep(6)
	exit()

os.system('cls')


os.system("mode con cols=47 lines=10")
ctypes.windll.kernel32.SetConsoleTitleA(b"PROxima ModLoader")

print('\033[36m\033[1m'.format('\n'))
print('____________ _______   __________  ___  ___  ')
print('| ___ \\ ___ \\  _  \\ \\ / /_   _|  \\/  | / _ \\ ')
time.sleep(0.1)
print('| |_/ / |_/ / | | |\\ V /  | | | .  . |/ /_\\ \\ ')
time.sleep(0.1)
print('|  __/|    /| | | |/   \\  | | | |\\/| ||  _  |')
time.sleep(0.1)
print('| |   | |\\ \\  \\_/ / /^\\ \\_| |_| |  | || | | |')
time.sleep(0.1)
print('\\_|   \\_| \\_|\\___/\\/   \\/\\___/\\_|  |_/\\_| |_/')
time.sleep(0.1)

print('\033[33m\033[1m'.format('\n'))
time.sleep(0.1)
print('               =[ MODLOADER ]=               ', end ='\r')
time.sleep(0.1)
print('             ===[ MODLOADER ]===             ', end ='\r')
time.sleep(0.1)
print('        ========[ MODLOADER ]========        ', end ='\r')
time.sleep(0.1)
print('   =============[ MODLOADER ]=============   ', end ='\r')
time.sleep(0.1)
print('================[ MODLOADER ]================', end ='\r')
time.sleep(0.1)
print('================[ MODLOADER ]====[v0.========', end ='\r')
time.sleep(0.1)
print('================[ MODLOADER ]====[v0.0.======', end ='\r')
time.sleep(0.1)
print('================[ MODLOADER ]====[v0.0.4]====', end ='\r')

time.sleep(2)
os.system('cls')
print("Author:")
time.sleep(0.1)
print('MDarklight aka Stefano_Barritono.  |', end = '\r')
time.sleep(0.25)
print('MDarklight aka Stefano_Barritono.  /', end = '\r')
time.sleep(0.25)
print('MDarklight aka Stefano_Barritono.  -', end = '\r')
time.sleep(0.25)
print('MDarklight aka Stefano_Barritono.  \\', end = '\r')
time.sleep(0.25)
print('MDarklight aka Stefano_Barritono.  |', end = '\r')
time.sleep(0.25)
print('MDarklight aka Stefano_Barritono.  /', end = '\r')
time.sleep(0.25)
print('MDarklight aka Stefano_Barritono.  -', end = '\r')
time.sleep(0.25)
print('MDarklight aka Stefano_Barritono.  \\', end = '\r')
time.sleep(0.2)

try:
	if version != release['tag_name']:
		os.system('cls')
		print('\033[31m\033[1m'.format('\n'))
		print('ВНИМАНИЕ!!! Используется неактуальная версия.', end = '\r')
		time.sleep(0.5)
		print('                                             ', end = '\r')
		time.sleep(0.5)
		print('ВНИМАНИЕ!!! Используется неактуальная версия.', end = '\r')
		time.sleep(0.5)
		print('                                             ', end = '\r')
		time.sleep(0.5)
		print('ВНИМАНИЕ!!! Используется неактуальная версия.', end = '\r')
		time.sleep(0.5)
		print('                                             ', end = '\r')
		time.sleep(0.5)
		print('ВНИМАНИЕ!!! Используется неактуальная версия.', end = '\r')
		time.sleep(0.5)
		print('                                             ', end = '\r')
		time.sleep(0.5)
		print('ВНИМАНИЕ!!! Используется неактуальная версия.')
		print('Обновите модлоадер.')
		time.sleep(5)
except:
	pass
print('\033[37m'.format('\n'))
os.system("mode con cols=60 lines=25")
os.system('cls')

if(modsfolderex == 1):
	pass
else:
	os.system("mode con cols=100 lines=35")
	if(input('Привет! Кажется, запуск происходит впервые. Необходимо пройти установку.\nНачать? [Y/n]: ').lower() == 'y'):
		if(input('Будет создана папка "mods" со всей структурой папки ресурсов.\nПродолжить [Y/n]: ').lower() == 'y'):
			print('На рабочем столе будет создан ярлык. Это нужно для запуска модлоадера.')
			time.sleep(4)
			modloader_install()
		else: exit()
	else: exit()
if(mode == 'game'):
	progresss = 'Загрузка модов...'
	load_mods()
	load_scripts()
	time.sleep(5)
	log('Запуск МТА...')
	os.system("mode con cols=70 lines=25")
	#os.system('launcher.exe')
	os.system("mode con cols=100 lines=25")
	ctypes.windll.kernel32.SetConsoleTitleA(b"PROxima ModLoader")
	os.system('cls')
	log('МТА запускается.')
	while True:
		f_read = open("./gtaSA/multiplayer/MTA/logs/console.log", "r", encoding='utf-8')
		last_line = f_read.readlines()[-1]
		if "clothes start" in last_line:
			log("Файлы разблокируются через минуту.")
			time.sleep(60)
			for process in pfileblock:
				subprocess.Popen.kill(process)
			break
	exit()
	#started = 1
#start()