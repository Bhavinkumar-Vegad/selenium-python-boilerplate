import csv
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.csv_utils import CSVUtils


class FormHandler:
    def __init__(self, driver):
        self.driver = driver

    def fill_form(self, fields_file, data):
        fields = CSVUtils.read_csv(fields_file)
        for field in fields:
            field_name = field['field_name']
            field_type = field['field_type']
            locator = self.get_locator(field)
            value = data.get(field_name, "").strip()  # Get value and strip any whitespace

            if not value:
                continue  # Skip fields with empty values

            if field_type == 'text' or field_type == 'password' or field_type == 'email' or field_type == 'tel' or field_type == 'url':
                self.enter_text(locator, value)
            elif field_type == 'select':
                self.select_dropdown_by_visible_text(locator, value)
            elif field_type == 'radio':
                self.select_radio_button(locator, value)
            elif field_type == 'checkbox':
                self.select_checkbox(locator, value)
            elif field_type == 'date':
                self.set_date(locator, value)
            elif field_type == 'range':
                self.set_range(locator, value)

    def get_locator(self, field):
        locators = [
            ('id_locator', By.ID),
            ('xpath_locator', By.XPATH),
            ('linktext_locator', By.LINK_TEXT),
            ('partiallinktext_locator', By.PARTIAL_LINK_TEXT),
            ('name_locator', By.NAME),
            ('tagname_locator', By.TAG_NAME),
            ('classname_locator', By.CLASS_NAME),
            ('cssselector_locator', By.CSS_SELECTOR)
        ]
        for key, by in locators:
            if field.get(key):
                return (by, field[key])
        raise ValueError("No valid locator found for field")

    def enter_text(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def select_dropdown_by_visible_text(self, locator, text):
        select = Select(self.wait_for_element(locator))
        select.select_by_visible_text(text)

    def select_radio_button(self, locator, value):
        radio_button = self.wait_for_element(locator)
        if value == 'checked' and not radio_button.is_selected():
            radio_button.click()

    def select_checkbox(self, locator, value):
        checkbox = self.wait_for_element(locator)
        if value == 'checked' and not checkbox.is_selected():
            checkbox.click()
        elif value == 'unchecked' and checkbox.is_selected():
            checkbox.click()

    def set_date(self, locator, date):
        date_element = self.wait_for_element(locator)
        date_element.clear()
        date_element.send_keys(date)

    def set_range(self, locator, value):
        range_element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].value = arguments[1]", range_element, value)

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
