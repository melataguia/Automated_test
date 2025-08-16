from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import unittest

from selenium import webdriver

import FieldAddForm
import HadronFieldHandler


class CloseFormTest(unittest.TestCase):
    remplirForm = "False"
    excelRowForm = 0
    actionForm = "ADD"
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

    def test_CloseForm(self):
        remplirForm = self.remplirForm
        excelRowForm = self.excelRowForm
        actionForm = self.actionForm
        roleUser = self.roleUser
        nameForm = self.nameForm

        position = FieldAddForm.Field(self, nameForm, roleUser, excelRowForm,
                                      actionForm, remplirForm)

        driver = self.driver
        if (position != -1):
            import pandas as pd
            config = pd.read_excel("../DataTest/Sidebar.xlsx")
            FieldsEdit = pd.read_excel(
                "../DataTest/" + config['Fichier Excel'][position],
                sheet_name="fields")

            Close = "X"

            if (Close == "X"):
                driver.find_element_by_xpath(
                    "//*[@data-test-id='" + FieldsEdit['Data Test Id'][len(
                        FieldsEdit["Data Test Id"]) - 1] + "']/button").click()
                self.assertEqual(
                    HadronFieldHandler.HadronFieldHandler.check_exists_element(
                        driver, FieldsEdit['Success'][0]), False,
                    "Erreur lors de la Fermeture")
            elif (Close == "Annuler"):
                driver.find_element_by_xpath(
                    "//*[@data-test-id='" + FieldsEdit['Data Test Id'][len(
                        FieldsEdit["Data Test Id"]) - 2] + "']").click()
                self.assertEqual(
                    HadronFieldHandler.HadronFieldHandler.check_exists_element(
                        driver, FieldsEdit['Success'][0]), False,
                    "Erreur lors de la Fermeture")
            else:
                print("Aucune fermeture demande")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        CloseFormTest.remplirForm = sys.argv.pop()
        CloseFormTest.excelRowForm = int(sys.argv.pop())
        CloseFormTest.actionForm = sys.argv.pop()
        CloseFormTest.roleUser = sys.argv.pop()
        CloseFormTest.nameForm = sys.argv.pop()

    unittest.main()
