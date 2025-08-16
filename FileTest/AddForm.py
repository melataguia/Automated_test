from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import time
import unittest

from selenium import webdriver
from selenium.webdriver.support.color import Color

import Login


#acceder aux differents formulaires
def Form(self, nameForm, role, typeForm):

    driver = self.driver
    #se connecter
    Login.GoLogin(self, role)
    import pandas as pd
    sidebar = pd.read_excel("../DataTest/Sidebar.xlsx")

    #chargement des elements pour arriver jusqu'au formulaire qu'on a choisi d'ouvrir
    for i in range(0, len(sidebar["FormName"])):
        if ((nameForm == sidebar["FormName"][i]) |
            (nameForm in sidebar["FormName"][i])):
            formposition = i
            if (str(sidebar['utilisable'][formposition]) == 'yes'):
                idTests = sidebar["Data-test-id"][formposition].split(';')
                for idTest in idTests:
                    driver.find_element_by_xpath("//*[@data-test-id='" + idTest
                                                 + "']").click()

                if ((typeForm == "EDIT") | (typeForm == "DELETE")):

                    choix = 0
                    if (choix != 0):
                        driver.find_element_by_xpath(
                            "//*[@data-test-id='listview-header-dropdown-arrow']/a"
                        ).click()
                        choix = input('Entrez la position du filtre: ')
                        driver.find_element_by_xpath(
                            "//*[@data-test-id='listview-header-infinite-loader-menu']/div/div/div/div["
                            + str(choix) + "]").click()
                        time.sleep(3)
                    driver.find_element_by_xpath(
                        "//*[@data-test-id='listview-body']/div/div/div/div[1]/div/div/div[2]/div"
                    ).click()

                FieldsEdit = pd.read_excel(
                    "../DataTest/" + sidebar['Fichier Excel'][formposition],
                    sheet_name="fields")
                for i in range(0, len(FieldsEdit["NAME"])):
                    if (FieldsEdit["NAME"][i] == typeForm):
                        action = i

                        act = FieldsEdit["Action"][action].split(';')
                        for a in act:
                            driver.find_element_by_xpath("//*[@data-test-id='"
                                                         + a + "']").click()

                return formposition
            else:
                print("Ce formulaire n'est pas utilisable !!!")
                return -1


class AddFormTest(unittest.TestCase):
    nameForm = "Collegue"
    roleUser = "Admin"
    actionForm = "ADD"

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("-ignore-certificate-errors")
        self.driver = webdriver.Chrome("/usr/bin/chromedriver",
                                       options=options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_AddForm(self):
        nameForm = self.nameForm
        roleUser = self.roleUser
        actionForm = self.actionForm

        driver = self.driver
        import pandas as pd
        position = Form(self, nameForm, roleUser, actionForm)

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

            #verifier la couleur et le titre du formulaire
            self.assertEqual(FieldsEdit['header color'][
                1] == Color.from_string(colorTest).hex, True,
                             "La barre du formulaire n'est pas Orange")
            self.assertEqual("Ajout" in title.text, True,
                             "Ce n'est pas un formulaire d'Ajout")

        else:
            print(
                ".........................................................................................."
            )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        AddFormTest.actionForm = sys.argv.pop()
        AddFormTest.roleUser = sys.argv.pop()
        AddFormTest.nameForm = sys.argv.pop()

    unittest.main()
