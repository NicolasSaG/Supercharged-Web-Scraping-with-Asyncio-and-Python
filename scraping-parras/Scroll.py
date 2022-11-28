from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

url = "https://goo.gl/maps/Uwii6dWu6ZGtQ5AT7"
# url = "https://www.geeksforgeeks.org/check-whether-html-element-has-scrollbars-using-javascript/"


class WebDriver:

    location_data = {}

    def __init__(self):

        self.PATH = "chromedriver.exe"
        self.options = Options()
        # self.options.add_argument("--headless")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--disable-site-isolation-trials")
        self.driver = webdriver.Chrome(self.PATH, options=self.options)

    def scroll_the_page(self):

        print("haciendo scroll...")
        try:
            pause_time = 2  # Waiting time after each scroll.
            # Number of times we will scroll the scroll bar to the bottom.
            max_count = 5
            x = 0

            while(x < max_count):
                # It gets the section of the scroll bar.

                # scrollable_div = self.driver.find_element_by_xpath(
                #     "//*[text()='Compartir']")
                scrollable_div = self.driver.find_element_by_xpath(
                    "/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]")

                try:
                    # Scroll it to the bottom.
                    self.driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                    # self.driver.execute_script(
                    # "arguments[0].scrollIntoView(true);", scrollable_div)
                except:
                    pass

                time.sleep(pause_time)  # wait for more reviews to load.
                x = x+1
                print("scroll exitoso")

        except Exception as e:
            print("scroll fallido: ", e)
            self.driver.quit()

    def click_all_reviews_button(self):
        try:
            element = self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[49]/div/button")
            element.click()

        except:
            self.driver.quit()
            return False

        return True

    def scrape(self, url):  # Passed the URL as a variable
        try:
            # Get is a method that will tell the driver to open at that particular URL
            self.driver.get(url)

        except Exception as e:
            self.driver.quit()
            return

        time.sleep(3)  # Waiting for the page to load.

        if self.click_all_reviews_button():
            time.sleep(3)  # Waiting for the page to load.
            self.scroll_the_page()  # Scrolling the page to load all reviews.
        else:
            print("no se encuentran resenas")

        return ("fin de scroll")


x = WebDriver()
print(x.scrape(url))
