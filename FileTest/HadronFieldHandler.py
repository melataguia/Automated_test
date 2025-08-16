from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


class HadronFieldHandler:

    FormInputField = "FIF"
    PhoneNumberInput = "PNI"
    AutoComplete = "A"
    GStoreAutoComplete = "GSA"
    GStoreAutoCompleteMulti = "GSAM"
    GMAPField = "GF"
    FileChooser = "FC"
    DatePicker = "DP"

    LabelT = "L"
    CheckBox = "CB"
    RadioButton = "RB"
    ButtonC = "B"
    SAVE = "SAVE"
    SAVEADD = "SAVEADD"
    ANN = "ANN"

    AllPath = {}
    SubPath = {}
    AllFileExel = ""

    FIELDS_TO_HANDLE = [
        FormInputField, PhoneNumberInput, AutoComplete, GStoreAutoComplete,
        GStoreAutoCompleteMulti, LabelT, CheckBox, RadioButton, ButtonC, ANN,
        SAVEADD, SAVE
    ]

    #verifier si le champs est remplissable
    @staticmethod
    def canHandleField(s):
        return s in HadronFieldHandler.FIELDS_TO_HANDLE

    #verifier si un element un present sur la page du navigateur
    @staticmethod
    def check_exists_element(driver, dataTestId):
        try:
            driver.implicitly_wait(5)
            driver.find_element_by_xpath("//*[@data-test-id='" + dataTestId +
                                         "']")
        except:
            return False
        return True

    #remplir les champs du formulaire
    @staticmethod
    def clickGoButtonOrValue(driver, dataTestId, fieldT, value):
        if (str(value) != 'nan'):
            if ((fieldT == "FIF") | (fieldT == "PNI")):
                driver.find_element_by_xpath("//*[@data-test-id='" + dataTestId
                                             + "']").clear()
                driver.find_element_by_xpath("//*[@data-test-id='" + dataTestId
                                             + "']").send_keys(value)
            if ((fieldT == "GSA") | (fieldT == "A")):
                driver.find_element_by_xpath("//*[@data-test-id='" + dataTestId
                                             + "']/div/div/span/div").click()
                driver.find_element_by_xpath(
                    "//*[@data-test-id='" + dataTestId +
                    "']/div[1]/div[1]/span[1]/div[2]/input[@class=\"Select-input\"]"
                ).send_keys(value + "\n")
            if ((fieldT == "SAVE") | (fieldT == "SAVEADD") |
                (fieldT == "ANN") | (fieldT == "B")):
                driver.find_element_by_xpath("//*[@data-test-id='" + dataTestId
                                             + "']").click()
            if ((fieldT == "RB") | (fieldT == "CB")):
                driver.find_element_by_xpath("//*[@data-test-id='" + dataTestId
                                             + "']/following::label").click()

    #retourne le contenu d'un champs du formulaire
    @staticmethod
    def GetContentField(driver, dataTestId, fieldT, value):
        if (str(value) != 'nan'):
            if ((fieldT == "FIF") | (fieldT == "PNI")):
                cont = driver.find_element_by_xpath(
                    "//*[@data-test-id='" + dataTestId + "']").get_attribute(
                        "value")
                label = driver.find_element_by_xpath(
                    "//*[@data-test-id='" + dataTestId +
                    "']/following::label").text
            elif ((fieldT == "GSA") | (fieldT == "A")):

                cont = driver.find_element_by_xpath(
                    "//*[@data-test-id='" + dataTestId +
                    "']/div[1]/div[1]/span[1]/div[1]/span").text
                label = driver.find_element_by_xpath(
                    "//*[@data-test-id='" + dataTestId + "']/label").text
            elif (fieldT == "CB"):
                cont = driver.find_element_by_xpath(
                    "//*[@data-test-id='" + dataTestId + "']").get_attribute(
                        "value")
                label = driver.find_element_by_xpath(
                    "//*[@data-test-id='" + dataTestId +
                    "']/following::label").text
            else:
                label = "BOUTON"
                cont = "OK"

            return label + " : " + cont
        else:
            return "Field Non Utilise: Sans Valeur"
