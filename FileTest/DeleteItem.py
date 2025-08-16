from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import unittest

from selenium import webdriver

import FieldAddForm


class DeletItemTest(unittest.TestCase):
    remplirForm = "False"
    excelRowForm = 0
    actionForm = "DELETE"
    roleUser = "Admin"
    nameForm = "Collegue"

    def setUp(self):

        options = webdriver.ChromeOptions()
        options.add_argument("-ignore-certificate-errors")
        self.driver = webdriver.Chrome("/usr/bin/chromedriver",
                                       options=options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_DeletItem(self):
        remplirForm = self.remplirForm
        excelRowForm = self.excelRowForm
        actionForm = self.actionForm
        roleUser = self.roleUser
        nameForm = self.nameForm

        position = FieldAddForm.Field(self, nameForm, roleUser, excelRowForm,
                                      actionForm, remplirForm)

        if (position != -1):
            import pandas as pd
            config = pd.read_excel("../DataTest/Sidebar.xlsx")
            FieldsEdit = pd.read_excel(
                "../DataTest/" + config['Fichier Excel'][position],
                sheet_name="fields")

            driver = self.driver

            driver.find_element_by_xpath(
                "//*[@data-test-id='" + FieldsEdit["DeleteReasonId"][0] +
                "']/div[1]/div[1]/span[1]/div[2]/input[@class=\"Select-input\"]"
            ).send_keys(" ")
            element = driver.find_element_by_xpath(
                "//*[@data-test-id='deleteModal-reason']/div/div[2]/div/div/div/div"
            )
            all_options = element.find_elements_by_tag_name("div")
            i = 0
            for option in all_options:
                i = i + 1
                self.assertEqual(
                    FieldsEdit["DeleteReasonId"][i] == option.text, True,
                    "Erreur au niveau des raisons de suppressions")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        DeletItemTest.remplirForm = sys.argv.pop()
        DeletItemTest.excelRowForm = int(sys.argv.pop())
        DeletItemTest.actionForm = sys.argv.pop()
        DeletItemTest.roleUser = sys.argv.pop()
        DeletItemTest.nameForm = sys.argv.pop()

    unittest.main()
