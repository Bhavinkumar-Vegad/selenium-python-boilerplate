import os
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class SeleniumUtils:

    def __init__(self, driver: webdriver):
        self.driver = driver

    # Browser Actions
    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()

    def go_back(self):
        """Navigate back in browser history."""
        self.driver.back()

    def go_forward(self):
        """Navigate forward in browser history."""
        self.driver.forward()

    def open_new_tab(self, url: str = "about:blank"):
        """Open a new tab with an optional URL."""
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_tab(self, index: int):
        """Switch to a specific tab."""
        self.driver.switch_to.window(self.driver.window_handles[index])

    def close_current_tab(self):
        """Close the current tab."""
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    # Window Management
    def maximize_window(self):
        """Maximize the browser window."""
        self.driver.maximize_window()

    def minimize_window(self):
        """Minimize the browser window."""
        self.driver.minimize_window()

    def set_window_size(self, width: int, height: int):
        """Set the browser window to a specific size."""
        self.driver.set_window_size(width, height)

    def get_window_size(self):
        """Get the current size of the browser window."""
        return self.driver.get_window_size()

    # Element Interactions
    def open_url(self, url: str):
        """Open a URL in the browser."""
        self.driver.get(url)

    def find_element(self, locator: tuple, timeout: int = 10):
        """Find a single element."""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: tuple, timeout: int = 10):
        """Find multiple elements."""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator: tuple, timeout: int = 10):
        """Click an element."""
        element = self.find_element(locator, timeout)
        element.click()

    def enter_text(self, locator: tuple, text: str, timeout: int = 10):
        """Enter text into an input field."""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def select_dropdown_by_visible_text(self, locator, text):
        select = Select(self.driver.find_element(*locator))
        select.select_by_visible_text(text)

    def select_radio_button(self, locator):
        radio_button = self.driver.find_element(*locator)
        if not radio_button.is_selected():
            radio_button.click()

    def select_multiple_checkboxes(self, locator, values):
        checkboxes = self.driver.find_elements(*locator)
        for checkbox in checkboxes:
            if checkbox.get_attribute("value") in values and not checkbox.is_selected():
                checkbox.click()

    def set_date(self, locator, date):
        date_element = self.driver.find_element(*locator)
        date_element.clear()
        date_element.send_keys(date)

    def set_range(self, locator, value):
        range_element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].value = arguments[1]", range_element, value)

    def get_text(self, locator: tuple, timeout: int = 10):
        """Get text from an element."""
        element = self.find_element(locator, timeout)
        return element.text

    def is_element_visible(self, locator: tuple, timeout: int = 10):
        """Check if an element is visible."""
        try:
            element = self.find_element(locator, timeout)
            return element.is_displayed()
        except TimeoutException:
            return False

    def wait_for_element_to_be_clickable(self, locator: tuple, timeout: int = 10):
        """Wait until an element is clickable."""
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def hover_over_element(self, locator: tuple, timeout: int = 10):
        """Hover over an element."""
        element = self.find_element(locator, timeout)
        ActionChains(self.driver).move_to_element(element).perform()

    def double_click_element(self, locator: tuple, timeout: int = 10):
        """Double click an element."""
        element = self.find_element(locator, timeout)
        ActionChains(self.driver).double_click(element).perform()

    def right_click_element(self, locator: tuple, timeout: int = 10):
        """Right click an element."""
        element = self.find_element(locator, timeout)
        ActionChains(self.driver).context_click(element).perform()

    def drag_and_drop(self, source_locator: tuple, target_locator: tuple, timeout: int = 10):
        """Drag and drop from source element to target element."""
        source_element = self.find_element(source_locator, timeout)
        target_element = self.find_element(target_locator, timeout)
        ActionChains(self.driver).drag_and_drop(source_element, target_element).perform()

    def scroll_to_element(self, locator: tuple, timeout: int = 10):
        """Scroll to an element."""
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def take_screenshot(self, file_path: str):
        """Take a screenshot of the current window."""
        self.driver.save_screenshot(file_path)

    def switch_to_frame(self, locator: tuple, timeout: int = 10):
        """Switch to a specific frame."""
        frame = self.find_element(locator, timeout)
        self.driver.switch_to.frame(frame)

    def switch_to_default_content(self):
        """Switch back to the default content."""
        self.driver.switch_to.default_content()

    def accept_alert(self, timeout: int = 10):
        """Accept an alert."""
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()

    def dismiss_alert(self, timeout: int = 10):
        """Dismiss an alert."""
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.dismiss()

    def get_alert_text(self, timeout: int = 10):
        """Get text from an alert."""
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        return alert.text

    def upload_file(self, locator: tuple, file_path: str, timeout: int = 10):
        """Upload a file."""
        element = self.find_element(locator, timeout)
        element.send_keys(file_path)

    def download_file(self, file_url: str, destination_folder: str):
        """Download a file (assuming direct URL download)."""
        local_filename = os.path.join(destination_folder, file_url.split('/')[-1])
        with self.driver.get(file_url) as response:
            with open(local_filename, 'wb') as file:
                file.write(response.content)
        return local_filename

    def execute_script(self, script: str, *args):
        """Execute a custom JavaScript script."""
        return self.driver.execute_script(script, *args)

    # Waits
    def wait_for_element_visible(self, locator: tuple, timeout: int = 10):
        """Wait for an element to be visible."""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            return None

    def wait_for_element_invisible(self, locator: tuple, timeout: int = 10):
        """Wait for an element to be invisible."""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            return None

    def wait_for_text_present(self, locator: tuple, text: str, timeout: int = 10):
        """Wait for specific text to be present in an element."""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            return None

    def wait(self, sec: int):
        time.sleep(sec)

    # Assertions
    def assert_element_text(self, locator: tuple, expected_text: str, timeout: int = 10):
        """Assert that an element's text matches the expected text."""
        element = self.find_element(locator, timeout)
        actual_text = element.text
        assert actual_text == expected_text, f"Expected text: '{expected_text}', but got: '{actual_text}'"

    def assert_element_contains_text(self, locator: tuple, expected_text: str, timeout: int = 10):
        """Assert that an element's text contains the expected text."""
        element = self.find_element(locator, timeout)
        actual_text = element.text
        assert expected_text in actual_text, f"Expected text to contain: '{expected_text}', but got: '{actual_text}'"

    def assert_element_visible(self, locator: tuple, timeout: int = 10):
        """Assert that an element is visible."""
        element = self.find_element(locator, timeout)
        assert element.is_displayed(), "Expected element to be visible, but it is not."

    # File Operations
    def read_file(self, file_path: str):
        """Read contents of a file."""
        with open(file_path, 'r') as file:
            return file.read()

    def write_file(self, file_path: str, content: str):
        """Write content to a file."""
        with open(file_path, 'w') as file:
            file.write(content)

    def delete_file(self, file_path: str):
        """Delete a file."""
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"The file {file_path} does not exist.")

    # Logging
    def setup_logger(self, name: str, log_file: str, level: int = logging.INFO):
        """Setup a logger."""
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger