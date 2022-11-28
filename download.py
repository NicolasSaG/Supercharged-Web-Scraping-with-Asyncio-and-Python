from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time

url = "http://www.aire.cdmx.gob.mx/default.php?opc=%27aKBk%27"


class WebDriver:

    location_data = {}

    def __init__(self):

        self.PATH = "chromedriver.exe"
        self.options = Options()
        # self.options.add_argument("--headless")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--disable-site-isolation-trials")
        self.driver = webdriver.Chrome(self.PATH, options=self.options)

    def click_download(self):
        try:
            element = self.driver.find_element_by_class_name(
                "btn")
            element.click()
        except:
            print("error al presionar boton btn")
            # self.driver.quit()
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

        for i in range(2010, 2020):
            select = Select(self.driver.find_element_by_id(
                'seluniano'))
            print("descargando datos de ", i)
            select.select_by_visible_text(str(i))

            if self.click_download():
                print("descarga de {}...".format(i))
            else:
                print("no descarga de {}...".format(i))
            time.sleep(3)

        self.driver.quit()
        return("fin datos")  # Returning the Scraped Data.


x = WebDriver()
print(x.scrape(url))

# source_files = "C:\Users\fnico\Downloads"
