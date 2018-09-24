from selenium import webdriver
import time

driver = None
wait_time = 5


def init():
    global driver
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options) if driver is None else driver


def load_page(page):
    driver.get(page)


def submit_form(element):
    element.submit()


def get_element_id(id):
    return driver.find_element_by_id(id)


def get_element_xpath(xpath):
    return driver.find_element_by_xpath(xpath)


def get_element_class_name(class_name):
    return driver.find_element_by_class_name(class_name)


def get_elements_class_name(class_name):
    return driver.find_elements_by_class_name(class_name)


def get_child_tag_name(element, tag_name):
    return element.find_element_by_tag_name(tag_name)


def get_childs_tag_name(element, tag_name):
    return element.find_elements_by_tag_name(tag_name)


def set_text_input(input, text):
    input.send_keys(text)


def save_screenshoot(filePath='/tmp/capture.png'):
    driver.save_screenshot(filePath)


def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(wait_time)


def scrolling_down_facebook(limit, main_element):
    old_page = driver.page_source
    while True:
        scroll_down()
        try:
            if limit and limit <= len(driver.find_elements_by_class_name(main_element)):
                return True
            new_page = driver.page_source
            if new_page != old_page:
                old_page = new_page
            else:
                return False
        except Exception:
            continue


def click(element):
    element.click()
    time.sleep(wait_time + 5)


def close():
    global driver
    driver.quit()
    driver = None


def get_current_url():
    return driver.current_url
