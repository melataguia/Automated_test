from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

loginTestCase = 'python Login.py Admin'
logoutTestCase = 'python Logout.py Admin'
formTestCase = 'python AddForm.py Collegue Admin ADD'
fieldTestCase = 'python FieldAddForm.py Collegue Admin ADD 0 True'
editTestCase = 'python EditItem.py Collegue Admin EDIT 0 False'
deleteTestCase = 'python DeleteItem.py Collegue Admin DELETE 0 False'

os.system(loginTestCase)
os.system(logoutTestCase)
os.system(formTestCase)
os.system(editTestCase)
os.system(deleteTestCase)
os.system(fieldTestCase)
