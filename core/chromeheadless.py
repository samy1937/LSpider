#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: chromeheadless.py.py
@time: 2020/3/17 15:17
@desc:
'''


import time

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import os
from urllib.parse import urlparse

from LSpider.settings import CHROME_WEBDRIVER_PATH
from utils.base import random_string
from utils.log import logger


class ChromeDriver:
    def __init__(self):
        self.chromedriver_path = CHROME_WEBDRIVER_PATH
        self.checkos()

        self.init_object()

        self.origin_url = ""

    def checkos(self):

        if os.name == 'nt':
            self.chromedriver_path = os.path.join(self.chromedriver_path, "chromedriver_win32.exe")
        elif os.name == 'posix':
            self.chromedriver_path = os.path.join(self.chromedriver_path, "chromedriver_linux64")
        else:
            self.chromedriver_path = os.path.join(self.chromedriver_path, "chromedriver_mac64")

    def init_object(self):

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.chromedriver_path)

        self.driver.set_page_load_timeout(15)
        self.driver.set_script_timeout(5)

    def get_resp(self, url):

        try:
            self.origin_url = url

            self.driver.get(url)
            self.driver.implicitly_wait(10)
            # self.click_page()

        except selenium.common.exceptions.TimeoutException:
            logger.warning("Chrome Headless request timeout..{}".format(url))
            return False

        return self.driver.page_source

    def click_page(self):

        self.click_link()
        self.click_button()

    def click_link(self):
        self.driver.refresh()

        links = self.driver.find_elements_by_tag_name('a')

        for link in links:

            try:
                href = link.get_attribute('href')

                if href.startswith('#'):
                    link.click()

                    if self.check_host():
                        new_url = self.driver.current_url
                        self.driver.back()

                if href == "javascript:void(0);":
                    link.click()

                    if self.check_host():
                        new_url = self.driver.current_url
                        self.driver.back()

            except selenium.common.exceptions.ElementNotInteractableException:
                logger.warning("[ChromeHeadless][Click Page] error interact")
                break

            except selenium.common.exceptions.StaleElementReferenceException:
                logger.warning("[ChromeHeadless][Click Page] page reload or wrong back redirect")
                break

    def click_button(self):

        try:
            inputs = self.driver.find_elements_by_tag_name('input')

            for input in inputs:
                input.send_keys(random_string())

            submit = self.driver.find_element_by_xpath("//input[@type='submit']")
            submit2 = self.driver.find_element_by_tag_name('button')

            submit.click()
            submit2.click()
        except selenium.common.exceptions.NoSuchElementException:
            logger.warning("[ChromeHeadless][Click Page] No Such Element")
            return

    def check_host(self):
        origin = urlparse(self.origin_url)
        now = urlparse(self.driver.current_url)

        if (origin.netloc != now.netloc) or (origin.path.replace('/', '') != now.path.replace('/', '')) or (origin.params != now.params) or (origin.query != now.query):
            return now.geturl()

        return False

    def close_driver(self):
        self.driver.quit()
        # self.driver.close()
        time.sleep(1)

    def __del__(self):
        self.close_driver()


if __name__ == "__main__":
    Req = ChromeDriver()

    Req.get_resp("https://lightless.me")

    # print(Req.get_resp("https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js"))
