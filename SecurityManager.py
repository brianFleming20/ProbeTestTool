'''
Created on 23 Apr 2017
@author: jackw
This module contains the SecurityManager class and its associated classes.
Securitymanager is responsible for managing all of the user profiles as well as hadling who is currently logged in
User data is contained in a pickled dictionary with each key as a username and the item being a two item array containing
the password and the users admin status
SecurityManager can:
Add a user
Delete a User
Change a users password
set a user to be logged in or out
For testing purposes comment out the following lines
to avoid pickle file errors
DS.write_to_user_file(user_data)
'''
import Datastore
import pickle

DS = Datastore.Data_Store()


class SecurityManager(object):
    """
    Handles all interaction with the User functionality.
    Such as: log in/out, add or delete user. Makes use of SecManDB to interact with the pickle file where user data is stored
    As this is now a seperate module, the state needs to stay the same.
    """

    def __init__(self):
        '''
        '''

        self.editingUser = False
        self.SMDB = SecManDB()
        self.is_admin_status = False

    def logIn(self, user):
        self.SMDB = SecManDB()
        '''
        tick
        call getUSer on secmanDB, check password with the user object returned by getUser
        if login sucessful store user object as SecurityManagers logedinuser attribute

                try:
            print(nuser.name, nuser.password, nuser.admin)
        except:
            print('user not found in dict')
        '''
        nuser = False

        if len(user.name) > 0 or len(user.password) > 0:
            nuser = self.SMDB.getUser(user)

        if nuser == False:  # is the username a valid username?
            return False

        if nuser.password == user.password:  # is the password correct?

            # DS.write_to_user_file([nuser.name, nuser.admin])
            login_user = Users(name=nuser.name,admin=nuser.admin)
            DS.write_user_data(login_user)

            return True
        else:
            return False

    def logOut(self):
        '''
        tick
        logs a current user out by setting the loggedInUser attribute to false
        '''
        self.loggedInUser = False

    def addUser(self, user):
        '''
        tick
        checks if the user's name is already in the dict, if not it stores the user object to the users file
        '''
        if self.SMDB.getUser(user.name) == False:
            self.SMDB.putUser(user)
            return True
        else:
            return False

    def delete_user(self, user):
        '''
        tick
        pass in a user object
        Checks to see if the user exists in the user dict, if so deletes it
        '''
        if self.SMDB.getUser(user.name):
            self.SMDB.removeUser(user)
            return True
        else:
            return False

    def updatePassword(self, password):
        """
        tick
        pass in a new user object
        checks to see if the user is in the user dict and the logged in user has admin privelages. if so, changes the password accordingly
        """

        name = DS.get_change_password_user()
        user = self.GetUserObject(name)
        user_details = user.password
        user.password = password

        self.SMDB.putUser(user)
        return True

    def GetUserObject(self, userName):
        self.SMDB = SecManDB()
        user = self.SMDB.getUser(userName)
        return user

    def GetUserList(self):
        userList = []
        userlist = self.SMDB.getUserList()
        return userlist

    def remind_password(self, user):
        user_obj = self.GetUserObject(user)
        return user_obj.password


class SecManDB(object):
    '''This class handles all of the opening and closing of the CSV'''

    def __init__(self):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.empty = None

    def getUser(self, user):
        '''
        tick
        pass in a username looks for given user in file
        if found, create a user object, fill it with the users data and return the object
        if not found, return False
        '''
        thisUser = False

        if type(user) == str:
            name = user
            user = User(name, "*")
        try:
            with open('userfile.pickle', 'rb') as handle:
                userDict = pickle.load(handle)

        except FileExistsError as e:
            with open('userfile.pickle', 'w') as handle:
                pickle.dump(handle, self.empty)
                thisUser = False
        else:
            for u in userDict:
                if u == user.name:
                    item = userDict[u]
                    password = item[0]
                    admin = item[1]
                    thisUser = User(u, password, admin)
        return thisUser

    def getUserList(self, ):
        '''
        tick
        returns a list of all the user objects
        '''
        userList = []
        try:
            with open('userfile.pickle', 'rb') as handle:
                userDict = pickle.load(handle)
        except FileNotFoundError:
            with open('userfile.pickle', 'wb') as handle:
                pickle.dump(handle, self.empty)
                return False
        else:
            for user in userDict:
                password = userDict[user][0]
                admin = userDict[user][1]
                thisUser = User(user, password, admin)
                userList.append(thisUser)

        return userList

    def putUser(self, user):
        '''
        tick
        Pass in a user object and update the CSV file with it
        '''

        # create details array
        details = ['', False]
        details[0] = user.password
        details[1] = user.admin

        try:
            with open('userfile.pickle', 'rb') as handle:
                userDict = pickle.load(handle)

        except FileNotFoundError:
            with open('userfile.pickle', 'wb') as handle:
                userDict = {user.name: details}
                pickle.dump(userDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            userDict[user.name] = details
            with open('userfile.pickle', 'wb') as handle:
                pickle.dump(userDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
            return True

    def removeUser(self, user):
        '''
        pass in a user object
        removes a given user from the user list
        '''

        with open('userfile.pickle', 'rb') as handle:
            userDict = pickle.load(handle)

        if user in userDict:
            userDict.pop(user)

        with open('userfile.pickle', 'wb') as handle:
            pickle.dump(userDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return True


class User(object):
    '''
    Used to create a user object, containing all the user`s info (username, password, admin status).
    '''

    def __init__(self, name, password, admin=False):
        self.name = name
        self.password = password
        self.admin = admin

# SM = SecurityManager()

# with open('filename.pickle', 'rb') as handle:
# userDict = pickle.load(handle)
# print(userDict)

class Users():

    def __init__(self, name, admin, plot=False, over_right=False, pw_user=""):
        self.Name = name
        self.Admin = admin
        self.Plot = plot
        self.Over_rite = over_right
        self.Change_password = pw_user
