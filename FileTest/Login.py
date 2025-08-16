from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import unittest

from selenium import webdriver


#Se connecter en specifiant juste le role du l'utilisateur a connecter
def GoLogin(self, roleUser):

    import pandas as pd
    logindata = pd.read_excel("../DataTest/LoginTestData.xlsx")

    numUser = -1
    for i in range(0, len(logindata["UserRole"])):
        if (logindata["UserRole"][i] == roleUser):
            numUser = i
    if (numUser != -1):
        driver = self.driver
        driver.get("https://localhost/dashboard/#/login")
        driver.find_element_by_xpath(
            "//*[@data-test-id='loginPage-email-matricule']").clear()
        driver.find_element_by_xpath(
            "//*[@data-test-id='loginPage-email-matricule']").send_keys(
                logindata["Email"][numUser])
        driver.find_element_by_xpath(
            "//*[@data-test-id='loginPage-password']").clear()
        driver.find_element_by_xpath(
            "//*[@data-test-id='loginPage-password']").send_keys(
                logindata["Password"][numUser])
        driver.find_element_by_xpath(
            "//*[@data-test-id='loginPage-submit-btn']").click()

    else:
        print('................')


class Login(unittest.TestCase):
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

    def test_Login(self):
        roleUser = self.roleUser
        GoLogin(self, roleUser)
        driver = self.driver
        role = driver.find_element_by_xpath(
            "//*[@data-test-id='detailview-empty-dv-span']")

        self.assertEqual("Plexus" in self.driver.title, True,
                         "ERREUR Le titre de la page de Contient Pas Plexus")
        self.assertEqual(roleUser in role.text, True,
                         "Le Role n'a pas ete bien defini")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        Login.roleUser = sys.argv.pop()
    unittest.main()
