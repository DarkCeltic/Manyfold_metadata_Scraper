import time

from selenium import webdriver
from selenium.common import TimeoutException, SessionNotCreatedException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from metaDataFiller.GlobalVariables.Global import add_new_model_urls, convert_license, add_new_creator_urls
from metaDataFiller.customErrors.notAvailableError import notAvailableError
from metaDataFiller.objects.creator import Creator
from metaDataFiller.objects.model import Model


def scrape_thingiverse(url: str, creator: Creator, model: Model):
    try:
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        wait = WebDriverWait(driver, timeout=20)
        try:
            driver.find_element(By.XPATH,
                                "//*[text()='It looks like this Thing has been removed or has never existed in Thingiverse.']")
            driver.stop_client()
            driver.close()
            driver.quit()
            raise notAvailableError('url no longer available')
        except NoSuchElementException:
            pass
        try:
            user_card = wait.until(expected_conditions.visibility_of_element_located(
                (By.CLASS_NAME, 'DetailPageTitle__thingTitleLink--QbOOV')))
            user_name = user_card.text
            user_url = user_card.get_attribute('href')
            if creator.creatorName is not user_name:
                creator.creatorName = user_name
            add_new_creator_urls('https://www.printables.com/@' + user_url, creator)
            time.sleep(5)
        except TimeoutException:
            pass
        try:
            license1 = wait.until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'License__licenseCode--Aezqo'))).text
            if model.license is not license1:
                model.license = convert_license(license1)
        except TimeoutException:
            pass
        time.sleep(5)

        add_new_model_urls(driver.current_url, model)
        driver.stop_client()
        driver.close()
        driver.quit()
    except SessionNotCreatedException as e:
        print(e)
        return
