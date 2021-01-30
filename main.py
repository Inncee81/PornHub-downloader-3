import os
from time import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from functions import *

options = webdriver.ChromeOptions()

options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36")

# headless mode
options.add_argument("--headless")

driver = webdriver.Chrome(
	executable_path= os.getcwd() + r"\chromedriver.exe",
	options=options
)

URL_PORNHUB = "https://rt.pornhub.com"
URL_DOWNLOADER = "https://www.pornhubdownload.com/"
PATH = "videos/"
REQUEST_STATUS_CODE = 200

HEADERS = {
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
}

class PornhubDownloader():
	def __init__(self):
		self.URL_PORNHUB = "https://rt.pornhub.com"
		self.URL_DOWNLOADER = "https://www.pornhubdownload.com/"
		self.PATH = "videos/"
		self.REQUEST_STATUS_CODE = 200
		self.driver = driver

		self.HEADERS = {
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
		}

	def get_video_title(self, soup):
		"""Возвращает название видео."""
		title = soup.find("div", class_="video-wrapper").find("div", class_="title-container").find("h1", class_="title").find("span", class_="inlineFree").get_text()
		return title

	def get_video_author(self, soup):
		"""Возвращает автора видео."""
		author_name = soup.find("div", class_="userInfo").find("div", class_="usernameWrap").find("span", class_="usernameBadgesWrapper").find("a", class_="bolded").get_text()
		return author_name

	def get_video_views(self, soup):
		"""Вовращает количество просмотров на видео."""
		views = soup.find("div", class_="views").find("span", class_="count").get_text()
		return views

	def download(self):
		"""Заходим с помощью вебдрайвера на сайт pornhubdownload.com и
		через него скачиваем видео.
		"""
		self.driver.get(self.URL_DOWNLOADER)

		link_input = self.driver.find_element_by_id("ytUrl")
		link_input.send_keys(self.link)

		submit = self.driver.find_element_by_id("convBtn").click()

		page_url = self.driver.current_url

		self.driver.close()
		self.driver.quit()

		resp = requests.get(page_url)
		soup = BeautifulSoup(resp.content, "html.parser")
		video_quality = soup.find_all("tr")

		# Выбираем видео в наилучшем качестве.
		for q in video_quality[::-1]:
			try:
				video_url = q.find_all("td")[-1].find("a")["href"]
				r = requests.get(video_url)
				break
			except:
				pass

		if r.status_code == self.REQUEST_STATUS_CODE:
			with open("{}{}.mp4".format(self.PATH, self.title), "wb") as f:
				f.write(r.content)
			self.success = True

	def main(self):
		"""Получаем от пользователя ссылку на видео, которое нужно скачать."""
		self.link = input("Введите ссылку на видео\n> ")

		resp = requests.get(self.link, headers=self.HEADERS)
		if resp.status_code == self.REQUEST_STATUS_CODE:
			soup = BeautifulSoup(resp.content, "html.parser")
			self.title = self.get_video_title(soup)
			self.author = self.get_video_author(soup)
			self.views = self.get_video_views(soup)

			# Проверяем, скачено ли уже видео
			if os.path.exists("{}{}.mp4".format(self.PATH, self.title)):
				print(f"Видео '{self.title}' уже скачено.")
			else:
				print("Навание видео: {}\nАвтор: {}\nКоличество просмотров: {}".format(
					self.title,
					self.author,
					self.views
				))

				print("Начинаем скачивать видео...")

				time_start = time()  # сохраняем время начала скачивания
				self.success = False

				self.download()

				time_finish = time() # сохраняем время конца скачивания
				if self.success:
					download_time = round(time_finish - time_start)
					print("Видео '{}' скачено за {} {}.".format(
						self.title,
						download_time,
						get_num_ending(download_time, [
							"секунду",
							"секунды",
							"секунд"
						])
					))
				else:
					print("Что-то пошло не так...")
		else:
			print("Что-то пошло не так...")

if __name__ == "__main__":
	# Создаём папку с порно, если её ещё нет
	if not os.path.exists(PATH):
		os.mkdir(PATH)
	PD = PornhubDownloader()
	PD.main()