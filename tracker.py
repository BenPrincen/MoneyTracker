# imports
import pyrebase
import datetime

# functions
def getInput():
    """
    """
    money = float(input("Enter money spent: "))
    person = input("Enter who spent it: ")
    entry = input("Short description: ")
    money_owed = money / 4
    return (person, money_owed, entry, money)

def update(money_dictionary, person, money_owed):
    """
    """
    if not person in money_dictionary.keys():
        print("%s is not part of the household. Exiting...", person)
        return False

    for key in money_dictionary[person].keys():
        money_dictionary[person][key] += money_owed
    return True

def normalize(money_dictionary):
    """
    """
    for key in money_dictionary.keys():
        for ower in money_dictionary[key].keys():
            if money_dictionary[key][ower] > money_dictionary[ower][key]:
                money_dictionary[key][ower] -= money_dictionary[ower][key]
                money_dictionary[ower][key] = 0.0
            else:
                money_dictionary[ower][key] -= money_dictionary[key][ower]
                money_dictionary[key][ower] = 0.0

def createChangelogEntry(money, person, description):
    """
    """
    entry = [{   
        "person" : person, 
        "money paid" : money, 
        "description" : description, 
        "date" : datetime.date.today().strftime("%m/%d/%Y")
    }]
    return entry

# globals
config = {
    'apiKey': "AIzaSyBUdSgznu5I5MWppXJtEtNRISWlhaRGiy4",
    'authDomain': "money-tracker-4d9bc.firebaseapp.com",
    'projectId': "money-tracker-4d9bc",
    'storageBucket': "money-tracker-4d9bc.appspot.com",
    'databaseURL': 'https://money-tracker-4d9bc-default-rtdb.firebaseio.com/'
}


# main
def main():
    firebase = pyrebase.initialize_app(config)

    db = firebase.database()

    info = getInput()

    users = db.child().get()
    money_dictionary = users.val()['users']

    update(money_dictionary, info[0], info[1])
    normalize(money_dictionary)

    db.child("users").update(money_dictionary)

    changelog = users.val()['changelog']
    entry = createChangelogEntry(info[3], info[0], info[2])
    changelog += entry

    temp = {"changelog" : changelog}

    db.child().update(temp)


if __name__ == '__main__':
    main()