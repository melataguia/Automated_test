from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import time
import unittest

from selenium import webdriver

import HadronFieldHandler
import Login


class Logout(unittest.TestCase):
    roleUser = "Admin"

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("-ignore-certificate-errors")
        self.driver = webdriver.Chrome("/usr/bin/chromedriver",
                                       options=options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_Logout(self):
        roleUser = self.roleUser
        Login.GoLogin(self, roleUser)
        driver = self.driver

        driver.find_element_by_xpath(
            "//*[@data-test-id='headerContent-profile-icon']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@data-test-id='logout']").click()

        self.assertEqual(
            HadronFieldHandler.HadronFieldHandler.check_exists_element(
                driver, 'logout-successful-notification'), True,
            "Erreur lors du Logout")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        Logout.roleUser = sys.argv.pop()
    unittest.main()
