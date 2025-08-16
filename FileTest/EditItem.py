from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import unittest

from selenium import webdriver
from selenium.webdriver.support.color import Color

import FieldAddForm


class EditItemTest(unittest.TestCase):
    remplirForm = "False"
    excelRowForm = 0
    actionForm = "EDIT"
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

    def test_EditItem(self):
        remplirForm = self.remplirForm
        excelRowForm = self.excelRowForm
        actionForm = self.actionForm
        roleUser = self.roleUser
        nameForm = self.nameForm

        position = FieldAddForm.Field(self, nameForm, roleUser, excelRowForm,
                                      actionForm, remplirForm)

        import pandas as pd
        driver = self.driver
        if (position != -1):
            config = pd.read_excel("../DataTest/Sidebar.xlsx")
            FieldsEdit = pd.read_excel(
                "../DataTest/" + config['Fichier Excel'][position],
                sheet_name="fields")

            title = driver.find_element_by_xpath(
                "//*[@data-test-id='" + FieldsEdit['header title'][0] + "']")
            colorTest = driver.find_element_by_xpath(
                "//*[@data-test-id='" + FieldsEdit['header color'][
                    0] + "']").value_of_css_property('background-color')

            self.assertEqual("#01d36b" == Color.from_string(colorTest).hex,
                             True, "La barre du formulaire n'est pas Verte")
            self.assertEqual("Modif" in title.text, True,
                             "Ce n'est pas un formulaire de Modification")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        EditItemTest.remplirForm = sys.argv.pop()
        EditItemTest.excelRowForm = int(sys.argv.pop())
        EditItemTest.actionForm = sys.argv.pop()
        EditItemTest.roleUser = sys.argv.pop()
        EditItemTest.nameForm = sys.argv.pop()

    unittest.main()
