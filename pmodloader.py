import os
import subprocess
import time
import hashlib
modsfolderex = 0
processes = []
proccount = 0
if(os.path.exists(os.path.abspath('.') + '\\mods')):
	print('Папка с модами существует.')
	modsfolderex = 1
	respath = os.path.abspath('gtaSA\\multiplayer\\mods\\deathmatch\\resources')
	workpath = os.path.abspath('.')
	modpath = workpath + '\\mods'
	print('Проверка структуры каталога модов...')
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
			print(path+' существует.                             ')
			ffolders = ffolders + 1
		else:
			os.mkdir(dirr)
			print(path+' создана.                             ')
			cfolders = cfolders + 1
		print(f'Проверка структуры каталога модов [{ffolders}/{tfolders}]            ', end='\r')
		time.sleep(0.005)

	print(f'Проверка завершена. [{ffolders}/{tfolders}]                            ')
	if cfolders != 0:
		print(f'Создано папок: {cfolders}')
else:
	modsfolderex = 0
	piplibs = subprocess.Popen(["pip", "freeze"], encoding='cp866', shell=True, stdout=subprocess.PIPE)
	pipstd = piplibs.stdout.read()
	#print(pipstd)
	if('keyboard' in pipstd):
		print('keyboard установлен')
	else:
		yn = input('Сейчас будут установлены недостающие библиотеки. Продолжить?[Y/n]: ')
		if(yn.lower() == 'y'):
			print('установка keyboard...')
			os.system('pip install keyboard')
		else:
			print('bye.')
			time.sleep(2)
			exit()

	if('pyshortcuts' in pipstd):
		print('pyshortcuts установлен')
	else:
		print('установка pyshortcuts...')
		os.system('pip install pyshortcuts')

	if('gdown' in pipstd):
		print('gdown установлен')
	else:
		print('установка gdown...')
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

print('\nПроверка актуальности...')

version = 'v0.0.4'
response = requests.get("https://api.github.com/repos/MersonDarklight/Proxima-ModLoader/releases/latest")
response.raise_for_status()
release = response.json()
print(f"Последний релиз: {release['tag_name']}, установлена: {version}.\n")
if version == release['tag_name']:
	print('Версия актуальна.')
else:
	print(f"Доступен новый релиз: {release['name']}.\nЧто нового:\n{release['body']}")
	if(input("\nУстановить? [Y/n]: ").lower() == 'y'):
		os.execv(sys.executable, ['python', 'update.py'])
time.sleep(2)

parser = argparse.ArgumentParser(description='A tutorial of argparse!')
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
	processes.append(process)

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

def gtacheck():
	while True:
		if(started == 1):
			tasklist = subprocess.Popen('tasklist', encoding='cp866', shell=True, stdout=subprocess.PIPE)
			stdlist = tasklist.stdout.read()
			if('gta_sa.exe' in stdlist):
				print('gta found')
			else:
				#print('gta closed, exiting..')
				#exit()
				pass
		time.sleep(10)

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
							print(f'{filename} соответствует моду')
						else:
							print('Копируем '+filename+' в '+dirname)
							os.remove(dirr+'\\'+filename)
							shutil.copy(root2+'\\'+filename, dirr)
							success = success + 1
						print('Блокируем файл...\n')
					except:
						print('ошибка')
					blockpath=dirr+'\\'+filename
					t = threading.Thread(target=blockfile)
					t.start()
		break
	print('Моды успешно загружены!')
	time.sleep(1)

def close_gta():
	keyboard.wait('ctrl+alt+x')
	os.system('taskkill /f /im gta_sa.exe')

def start():
	threads = (
		threading.Thread(target=close_gta),
		threading.Thread(target=gtacheck, daemon=True)
	)
	for t in threads:
		t.start()

def modloader_install():
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
		print(path+' создан.                             ')
		cfolders=cfolders+1
		try:
			os.mkdir(dirr)
		except:
			pass
		for filename in files:
			pass
		print(f'Создание каталогов.. [{cfolders}/{tfolders}]', end='\r')
		time.sleep(0.005)
	print(f'Каталог для модов создан. [{cfolders}/{tfolders}]')
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
	print('Установка завершена. Запустите модлоадер с ярлыка на рабочем столе.')
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
	print('Запуск МТА...')
	os.system("mode con cols=70 lines=25")
	#os.system('launcher.exe')
	os.system("mode con cols=60 lines=25")
	ctypes.windll.kernel32.SetConsoleTitleA(b"PROxima ModLoader")
	os.system('cls')
	print('МТА запускается.')
	time.sleep(444)
	print('разблокировка файлов...')
	for process in processes:
		subprocess.Popen.kill(process)
	exit()
	started = 1
	#os.system('cls')
	#pass
					
		#for filename in files:
    	 #   print(filename)
start()
