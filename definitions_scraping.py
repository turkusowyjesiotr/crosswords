from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


options = Options()
options.headless = True
driver = webdriver.Chrome('C:/Users/X/Desktop/chromedriver.exe', options=options)


def check_definitions_exists():
    try:
        driver.find_element(By.CSS_SELECTOR, '.alert > button:nth-child(1)')
    except NoSuchElementException:
        return True
    return False


def check_button_exists():
    try:
        driver.find_element(By.CSS_SELECTOR, 'a.btn-default:nth-child(1)')
    except NoSuchElementException:
        return False
    return True


def scrape_definitions(word):
    driver.get(f'http://wordlist.eu/slowo/{word}')
    if check_button_exists() is True:
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        button = driver.find_element(By.CSS_SELECTOR, 'a.btn-default:nth-child(1)')
        button.click()
    elements = driver.find_elements(By.XPATH, '//dd[contains(@id, "dfn")]')
    definitions = [el.text for el in elements]
    if definitions is []:
        driver.quit()
        return False
    else:
        driver.quit()
        return definitions


print(scrape_definitions('roztocze'))



