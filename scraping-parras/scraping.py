from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

url = "https://goo.gl/maps/Uwii6dWu6ZGtQ5AT7"


class WebDriver:

    location_data = {}

    def __init__(self):

        self.PATH = "chromedriver.exe"
        self.options = Options()
        # self.options.add_argument("--headless")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--disable-site-isolation-trials")
        self.driver = webdriver.Chrome(self.PATH, options=self.options)

        self.location_data["rating"] = "NA"
        self.location_data["num_resenas"] = "NA"
        self.location_data["locacion"] = "NA"
        self.location_data["Resenas"] = []

    def get_location_data(self):
        try:
            avg_rating = self.driver.find_element_by_class_name(
                "aMPvhf-fI6EEc-KVuj8d")
            total_reviews = self.driver.find_element_by_class_name(
                "Yr7JMd-pane-hSRGPd")
            address = self.driver.find_element_by_class_name(
                "QSFF4-text gm2-body-2")

        except:
            pass

        try:
            self.location_data["rating"] = avg_rating.text
            self.location_data["num_resenas"] = total_reviews.text
            self.location_data["locacion"] = address.text
        except:
            pass

    def click_all_reviews_button(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "wNNZR gm2-button-alt")))

            element = self.driver.find_element_by_class_name(
                "wNNZR gm2-button-alt")
            element.click()

        except:
            self.driver.quit()
            return False

        return True

    def scroll_the_page(self):
        try:
            # Waits for the page to load.
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root")))
            pause_time = 2  # Waiting time after each scroll.
            # Number of times we will scroll the scroll bar to the bottom.
            max_count = 5
            x = 0

            while(x < max_count):
                # It gets the section of the scroll bar.
                scrollable_div = self.driver.find_element_by_css_selector(
                    'div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
                try:
                    # Scroll it to the bottom.
                    self.driver.execute_script(
                        'arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                except:
                    pass

                time.sleep(pause_time)  # wait for more reviews to load.
                x = x+1

        except:
            self.driver.quit()

    def expand_all_reviews(self):
        try:
            element = self.driver.find_elements_by_class_name(
                "ODSEW-KoToPc-ShBeI gXqMYb-hSRGPd")
            for i in element:
                i.click()
        except:
            pass

    def get_reviews_data(self):
        try:
            # Its a list of all the HTML sections with the reviewer name.
            review_names = self.driver.find_elements_by_class_name(
                "ODSEW-ShBeI-title")
            # Its a list of all the HTML sections with the reviewer reviews.
            review_text = self.driver.find_elements_by_class_name(
                "ODSEW-ShBeI-text")
            # Its a list of all the HTML sections with the reviewer reviewed date.
            review_dates = self.driver.find_elements_by_class_name(
                "ODSEW-ShBeI-RgZmSc-date")
            # Its a list of all the HTML sections with the reviewer rating.
            review_stars = self.driver.find_elements_by_class_name(
                "ODSEW-ShBeI-H1e3jb")

            review_stars_final = []

            for i in review_stars:
                review_stars_final.append(i.get_attribute("aria-label"))

            review_names_list = [a.text for a in review_names]
            review_text_list = [a.text for a in review_text]
            review_dates_list = [a.text for a in review_dates]
            review_stars_list = [a for a in review_stars_final]

            for (a, b, c, d) in zip(review_names_list, review_text_list, review_dates_list, review_stars_list):
                self.location_data["Resenas"].append(
                    {"name": a, "review": b, "date": c, "rating": d})

        except Exception as e:
            pass

    def scrape(self, url):  # Passed the URL as a variable
        try:
            # Get is a method that will tell the driver to open at that particular URL
            self.driver.get(url)

        except Exception as e:
            self.driver.quit()
            return

        time.sleep(10)  # Waiting for the page to load.

        # Calling the function to get all the location data.
        self.get_location_data()

        # Clicking the all reviews button and redirecting the driver to the all reviews page.
        if(self.click_all_reviews_button() == False):
            return(self.location_data)

        time.sleep(5)  # Waiting for the all reviews page to load.

        self.scroll_the_page()  # Scrolling the page to load all reviews.
        # Expanding the long reviews by clicking see more button in each review.
        self.expand_all_reviews()
        self.get_reviews_data()  # Getting all the reviews data.

        self.driver.quit()  # Closing the driver instance.

        return(self.location_data)  # Returning the Scraped Data.


x = WebDriver()
print(x.scrape(url))
