import pytest
from selenium import webdriver
from utils.helpers import SeleniumUtils
from selenium.webdriver.common.by import By


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()  # Or any other WebDriver
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def login(driver):
    utils = SeleniumUtils(driver)
    utils.maximize_window()
    utils.open_url("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    # Replace with actual login steps
    utils.enter_text((By.NAME, "username"), "Admin")
    utils.enter_text((By.NAME, "password"), "admin123")
    utils.click_element((By.CLASS_NAME, "orangehrm-login-button"))

    # Ensure login is successful, e.g., by checking for the presence of a logout button
    assert utils.is_element_visible((By.CLASS_NAME, "oxd-topbar-header-breadcrumb"))

    yield driver
