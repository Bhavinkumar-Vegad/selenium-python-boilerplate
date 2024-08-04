import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.form_handler import FormHandler
from utils.helpers import SeleniumUtils
from utils.csv_utils import CSVUtils


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def selenium_utils(driver):
    return SeleniumUtils(driver)


@pytest.fixture(scope="session")
def form_handler(driver):
    return FormHandler(driver)


# Reading test data from CSV file
def get_test_data():
    data_file = os.path.join(os.path.dirname(__file__), '..', 'form_data', 'login_data.csv')
    return CSVUtils.read_csv(data_file)


@pytest.mark.parametrize("test_data", get_test_data())
def test_login_form(form_handler, selenium_utils, test_data):
    driver = form_handler.driver
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    selenium_utils.maximize_window()
    selenium_utils.wait(5)

    # Using FormHandler to fill the form from CSV
    fields_file = os.path.join(os.path.dirname(__file__), '..', 'form_definitions', 'login_form.csv')

    # Pass only the current row data to the FormHandler
    form_handler.fill_form(fields_file, test_data)

    selenium_utils.wait(2)
    # Click the submit button
    selenium_utils.click_element((By.CLASS_NAME, "orangehrm-login-button"))
    selenium_utils.wait(2)

    # Assuming successful login will be verified by checking a user dropdown or profile name
    selenium_utils.click_element((By.CLASS_NAME, "oxd-userdropdown-name"))
    selenium_utils.wait(2)
    selenium_utils.click_element((By.XPATH, "//a[text()='Logout']"))
    selenium_utils.wait(3)
