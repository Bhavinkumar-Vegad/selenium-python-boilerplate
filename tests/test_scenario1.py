from selenium.webdriver.common.by import By
from utils.helpers import SeleniumUtils


def test_scenario1(login):
    driver = login
    utils = SeleniumUtils(driver)

    # Replace with actual steps for scenario 1
    utils.wait(2)
    utils.click_element((By.XPATH,"//span[normalize-space()='Admin']"))