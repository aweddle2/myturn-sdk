# MyTurn SDK
A Selenium based SDK written in Python for the [My Turn](https://myturn.com/) Lending Library Software.

# Prerequisites
[Google Chrome](https://www.google.com/chrome/) must be running on the machine this library runs on.

## Installation 
`pip install myturn-sdk`

## Usage

### Instantiate Library

```python
myturnSubdomain = 'mylibrary'
myTurnUsername = 'testuser'
myturnPassword = 'Password!'

myTurnClient = MyTurnClient(
            myturnSubdomain, myTurnUsername, myturnPassword, False)
```

### Search for a User

```python
request = UserSearchRequest()
request.email = 'homer@simpsons.com'
response = myTurnClient.users.searchUsers(request)

for user in response.users:
    print(user.firstName+' '+user.lastName)
```

Other functionality follows a similar pattern:
* myTurnClient.users.getUser()
* myTurnClient.users.getUserIdForMembershipId()
* myTurnClient.users.getRequestsToJoin()
* myTurnClient.users.appendNote()
* myTurnClient.users.setNote()
* myTurnClient.users.getNote()
* myTurnClient.users.deleteUser()

See unit tests for examples.