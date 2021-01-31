import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from functions import *


class PornhubDownloader():
	def __init__(self):
		self.URL_PORNHUB = "https://rt.pornhub.com"
		self.URL_DOWNLOADER = "https://www.pornhubdownload.com/"
		self.BASE_DIR = Path(__file__).resolve().parent
		self.PATH = self.BASE_DIR.joinpath('videos')
		self.REQUEST_STATUS_CODE = 200

		self.HEADERS = {
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
		}

		self.options = webdriver.ChromeOptions()

		self.options.add_argument(
			"user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36")

		# headless mode
		self.options.add_argument("--headless")

		self.driver = webdriver.Chrome(
			executable_path= self.BASE_DIR.joinpath("chromedriver.exe"),
			options=self.options
		)

	@staticmethod
	def get_video_title(soup):
		"""Возвращает название видео."""
		title = soup.find("div", class_="video-wrapper")\
			.find("div", class_="title-container")\
			.find("h1", class_="title")\
			.find("span", class_="inlineFree")\
			.get_text()
		return title

	@staticmethod
	def get_video_author(soup):
		"""Возвращает автора видео."""
		author_name = soup.find("div", class_="userInfo")\
			.find("div", class_="usernameWrap")\
			.find("span", class_="usernameBadgesWrapper")\
			.find("a", class_="bolded")\
			.get_text()
		return author_name

	@staticmethod
	def get_video_views(soup):
		"""Вовращает количество просмотров на видео."""
		views = soup.find("div", class_="views")\
			.find("span", class_="count")\
			.get_text()
		return views

	def download(self):
		"""Заходим с помощью вебдрайвера на сайт pornhubdownload.com и
		через него скачиваем видео.
		"""
		self.driver.get(self.URL_DOWNLOADER)

		link_input = self.driver.find_element_by_id("ytUrl")
		link_input.send_keys(self.link)

		self.driver.find_element_by_id("convBtn").click()

		page_url = self.driver.current_url

		self.driver.close()
		self.driver.quit()

		resp = requests.get(page_url)
		soup = BeautifulSoup(resp.content, "html.parser")
		video_quality_array = soup.find_all("tr")

		# Выбираем видео в наилучшем качестве
		for q in video_quality_array [::-1]:
			self.video_url = q.find_all("td")[-1].find("a")["href"]
			if self.video_url != "/itubego/":
				self.video_quality = q.find_all("td")[0].get_text()
				break

		r = requests.get(self.video_url, headers=self.HEADERS)
		if r.status_code == self.REQUEST_STATUS_CODE:
			with open(self.file_path, mode="wb") as f:
				f.write(r.content)
			return True
		else:
			return False

	def main(self):
		# Создаём папку с порно, если её ещё нет
		if not Path(self.PATH).exists():
			Path(self.PATH).mkdir(parents=True, exist_ok=True)

		# Получаем от пользователя ссылку на видео, которое нужно скачать
		self.link = input("Введите ссылку на видео\n> ")

		resp = requests.get(self.link, headers=self.HEADERS)
		if resp.status_code == self.REQUEST_STATUS_CODE:
			soup = BeautifulSoup(resp.content, "html.parser")
			self.title = self.get_video_title(soup)
			self.author = self.get_video_author(soup)
			self.views = self.get_video_views(soup)

			# Проверяем, скачано ли уже видео
			self.file_path = self.PATH.joinpath(self.title + ".mp4")
			if Path(self.file_path).exists():
				print(f"Видео '{self.title}' уже скачано.")
			else:
				print(
					f"Навание видео: {self.title}\n"
					f"Автор: {self.author}\n"
					f"Количество просмотров: {self.views}"
				)

				print("Начинаем скачивать видео...")

				time_start = time.time()  # сохраняем время начала скачивания
				success = self.download()

				if success:
					time_finish = time.time()  # сохраняем время конца скачивания
					download_time = round(time_finish - time_start)
					download_time_phrase = get_num_ending(download_time, [
						"секунду",
						"секунды",
						"секунд"
					])
					print("Видео '{}' в качесте {} скачено за {} {}.".format(
						self.title,
						self.video_quality,
						download_time,
						download_time_phrase
					))
				else:
					print("Что-то пошло не так...")
		else:
			print("Что-то пошло не так...")

if __name__ == "__main__":
	PD = PornhubDownloader()
	PD.main()