import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.helpers import SeleniumUtils


def test_scenario2(login):
    driver1 = login
    utils = SeleniumUtils(driver1)

    # Replace with actual steps for scenario 2
    utils.wait(2)
    utils.click_element((By.XPATH,"//span[normalize-space()='PIM']"))
    utils.wait(3)