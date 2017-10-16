class Student:
    def __init__(self, name, email, contact, skills, ug=None, pg=None):
        self.email = email
        self.contact = contact
        self.name = name
        self.skills = [skills]

        self.edu = {"ug": [ug], "pg": [pg]}

        self.__private = 1
        self.__dict__.pop('_{}{}'.format(self.__class__.__name__, '__private'))

james = Student("James", "j@j.com", "", "+1 7789990007", "Python", "CS")

print(vars(james))


import json
print(json.dumps(vars(james),sort_keys=True, indent=4))