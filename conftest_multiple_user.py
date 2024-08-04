import pytest
from selenium import webdriver
from utils.helpers import SeleniumUtils
from selenium.webdriver.common.by import By


@pytest.fixture(scope="session")
def driver1():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def driver2():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def user1_login(driver1):
    utils = SeleniumUtils(driver1)
    utils.maximize_window()
    utils.open_url("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    # Replace with actual login steps
    utils.enter_text((By.NAME, "username"), "Admin")
    utils.enter_text((By.NAME, "password"), "admin123")
    utils.click_element((By.CLASS_NAME, "orangehrm-login-button"))

    # Ensure login is successful, e.g., by checking for the presence of a logout button
    assert utils.is_element_visible((By.CLASS_NAME, "oxd-topbar-header-breadcrumb"))

    yield driver1


@pytest.fixture(scope="session")
def user2_login(driver2):
    utils = SeleniumUtils(driver2)
    utils.open_url("https://example.com/login")

    # Replace with actual login steps for User2
    utils.enter_text((By.NAME, "username"), "user2_username")
    utils.enter_text((By.NAME, "password"), "user2_password")
    utils.click_element((By.ID, "loginButton"))

    assert utils.is_element_visible((By.ID, "logoutButton"))

    yield driver2
