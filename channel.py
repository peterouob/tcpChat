import client


def setName():
    name = client.user.name
    password = client.user.password
    print(name,password)

setName()