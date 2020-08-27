from os import mkdir
from os.path import exists

from requests import get
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from random import choice, randint
from string import ascii_lowercase, digits


def create_header():
	useragent = UserAgent().random
	header = {'user-agent': useragent}
	return header


def write_img(code: str, img):
	if not exists('images'):
		mkdir('images')

	with open(f'images/{code}.jpg', 'wb') as file:
		file.write(img)


def return_img(img_link: str):
	header = create_header()

	img = get(img_link, headers=header).content
	return img


def img_link(responce):
	soup = BeautifulSoup(responce, 'lxml')
	try:
		img_link = soup.find('img', class_='no-click screenshot-image').get('src')

	except AttributeError:
		img_link = None

	return img_link


def get_page(url: str):
	header = create_header()

	responce = get(url, headers=header)
	return responce.text


def gen_code():
	sumbols = ascii_lowercase + digits

	code = ''
	for i in range(randint(4, 7)):
		code += choice(sumbols)

	return code


def main():
	URL = 'https://prnt.sc/'
	code = gen_code()

	responce = get_page(URL + code)
	link_to_img = img_link(responce)

	if link_to_img and link_to_img != '//st.prntscr.com/2020/08/01/0537/img/0_173a7b_211be8ff.png':
		print(f'[+] {URL+code}')
		img = return_img(link_to_img)
		write_img(code, img)

	else:
		print(f'[-] {URL+code}')


if __name__ == '__main__':
	while True:
		try:
			main()

		except KeyboardInterrupt:
			print()
			print('------FINISHED------')
			break
