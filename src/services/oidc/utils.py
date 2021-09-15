import logging
import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


def is_active_login(driver):
    try:
        element = driver.find_element_by_name("loginfmt")
    except (StaleElementReferenceException, NoSuchElementException):
        return False
    return element.get_attribute("type") != "hidden"


def is_active_pwd(driver):
    try:
        element = driver.find_element_by_name("passwd")
    except (StaleElementReferenceException, NoSuchElementException):
        return False
    return element.get_attribute("type") != "hidden"


def is_clickable(driver):
    try:
        driver.find_element_by_id("idSIButton9").click()
    except (StaleElementReferenceException, ElementClickInterceptedException):
        return False
    return True


def wait_load_of_element(driver, delay, attr, name):
    try:
        WebDriverWait(driver, delay).until(
            expected_conditions.presence_of_element_located((attr, name))
        )
    except (StaleElementReferenceException, TimeoutException):
        logger.warning("FAIL")
        wait_load_of_element(driver, delay, attr, name)


def wait_is_active(driver, delay, check_func):
    try:
        WebDriverWait(driver, delay).until(check_func)
    except (StaleElementReferenceException, TimeoutException):
        logger.warning("FAIL")
        wait_is_active(driver, delay, check_func)


def wait_is_clickable_submit_btn(driver, delay):
    try:
        WebDriverWait(driver, delay).until(
            expected_conditions.element_to_be_clickable((By.ID, "idSIButton9"))
        )
    except (StaleElementReferenceException, TimeoutException):
        logger.warning("FAIL")
        wait_is_clickable_submit_btn(driver, delay)


def click_on_btn(driver, delay, _id):
    try:
        driver.find_element_by_id(_id).click()
    except (StaleElementReferenceException, ElementClickInterceptedException):
        time.sleep(3)
        click_on_btn(driver, delay, _id)
