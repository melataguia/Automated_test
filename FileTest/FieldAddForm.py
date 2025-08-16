from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import unittest

from selenium import webdriver
from selenium.webdriver.support.color import Color

import AddForm
import HadronFieldHandler


#Remplir les champs du formulaire si l'agrument "Remplir"=="True"
def Field(self, formName, role, excelRow, typeForm, Remplir):

    driver = self.driver
    position = AddForm.Form(self, formName, role, typeForm)
    if ((position != -1) & (Remplir == "True")):
        import pandas as pd
        config = pd.read_excel("../DataTest/Sidebar.xlsx")
        FieldsEdit = pd.read_excel(
            "../DataTest/" + config['Fichier Excel'][position],
            sheet_name="fields")
        DataEdit = pd.read_excel(
            "../DataTest/" + config['Fichier Excel'][position],
            sheet_name="data")

        for i in range(0, len(FieldsEdit["Field Name"])):
            if ((HadronFieldHandler.HadronFieldHandler.canHandleField(
                    FieldsEdit["Field Type"][i]))):
                HadronFieldHandler.HadronFieldHandler.clickGoButtonOrValue(
                    driver, FieldsEdit["Data Test Id"][i],
                    FieldsEdit["Field Type"][i],
                    DataEdit[FieldsEdit["Field Name"][i]][excelRow])
                #print(HadronFieldHandler.HadronFieldHandler.GetContentField(driver, FieldsEdit["Data Test Id"][i], FieldsEdit["Field Type"][i] , DataEdit[FieldsEdit["Field Name"][i]][excelRow]))

    else:
        print("...")

    return position


class EditFormTest(unittest.TestCase):
    remplirForm = "True"
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

    def test_EditForm(self):
        remplirForm = self.remplirForm
        excelRowForm = self.excelRowForm
        actionForm = self.actionForm
        roleUser = self.roleUser
        nameForm = self.nameForm

        driver = self.driver
        import pandas as pd
        position = Field(self, nameForm, roleUser, excelRowForm, actionForm,
                         remplirForm)

        if (position != -1):
            config = pd.read_excel("../DataTest/Sidebar.xlsx")
            FieldsEdit = pd.read_excel(
                "../DataTest/" + config['Fichier Excel'][position],
                sheet_name="fields")

            colorProgress = driver.find_element_by_xpath(
                "//*[@data-test-id='" + FieldsEdit['Progress'][
                    0] + "']").value_of_css_property('color')
            colorSucces = driver.find_element_by_xpath(
                "//*[@data-test-id='" + FieldsEdit['Success'][
                    0] + "']").value_of_css_property('color')
            SuccessNotif = driver.find_element_by_xpath(
                "//*[@data-test-id='" + FieldsEdit['Success'][0] + "']").text

            self.assertEqual(
                HadronFieldHandler.HadronFieldHandler.check_exists_element(
                    driver, FieldsEdit['Progress'][0]), True,
                "Erreur sur la notification en cours")
            self.assertEqual(
                "#31708f" == Color.from_string(colorProgress).hex, True,
                "La notification de la progression n'est pas bleue")
            self.assertEqual("avec" in SuccessNotif, True,
                             "Aucun message de succes")
            self.assertEqual("#01d36b" == Color.from_string(colorSucces).hex,
                             True, "La notification du Succes n'est pas Verte")

        else:
            print("...")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        EditFormTest.remplirForm = sys.argv.pop()
        EditFormTest.excelRowForm = int(sys.argv.pop())
        EditFormTest.actionForm = sys.argv.pop()
        EditFormTest.roleUser = sys.argv.pop()
        EditFormTest.nameForm = sys.argv.pop()

    unittest.main()
