from datetime import date


class User():
    def __init__(self):
        pass

    # If firstnane and last name have been provided seperately then use that as the name, otherwise use name
    def __getName(self):
        if (len(self.firstName) > 0 and len(self.lastName) > 0):
            return self.firstName + ' ' + self.lastName
        else:
            return self.__name

    def __setName(self, value):
        return self.__name

    __name: str = ''

    userId: int = None
    membershipId: int = None
    username: str = ''
    name: str = property(__getName, __setName)
    firstName: str = ''
    lastName: str = ''
    phone: str = ''
    email: str = ''
    currentMembershipType: str = ''
    memberCreated: date = None
    userNote: str = ''
    paymentMethod: str = ''
    address1: str = ''
    address2: str = ''
    city: str = ''
    country: str = ''
    postalCode: str = ''
    dateOfBirth: date = None
