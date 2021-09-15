import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

from src.core.config import MICROSOFT_OIDC_URL
from src.services.oidc.utils import (
    click_on_btn,
    is_active_login,
    is_active_pwd,
    wait_is_active,
    wait_is_clickable_submit_btn,
    wait_load_of_element,
)

logger = logging.getLogger(__name__)


def login(username: str, password: str) -> str:
    """
    Login to astana it university's moodle system
    :param username: Email of user
    :param password: Password of user
    """
    with webdriver.Firefox() as driver:
        driver.get(MICROSOFT_OIDC_URL)

        delay = 30  # seconds

        wait_load_of_element(driver, delay, By.NAME, "loginfmt")
        wait_is_active(driver, delay, is_active_login)
        driver.find_element_by_name("loginfmt").send_keys(username)

        wait_is_clickable_submit_btn(driver, delay)
        click_on_btn(driver, delay, "idSIButton9")

        wait_load_of_element(driver, delay, By.NAME, "passwd")
        wait_is_active(driver, delay, is_active_pwd)
        driver.find_element_by_name("passwd").send_keys(password)

        wait_is_clickable_submit_btn(driver, delay)
        click_on_btn(driver, delay, "idSIButton9")
        click_on_btn(driver, delay, "idSIButton9")

        cookies = driver.get_cookies()
        moodle_session_hash = [
            item["value"] for item in cookies if item["name"] == "MoodleSession"
        ]
        return moodle_session_hash[0] if len(moodle_session_hash) else None
