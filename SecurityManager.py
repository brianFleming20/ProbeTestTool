"""
Created on 23 Apr 2017
@author: jackw
@author: Brian F
This module contains the SecurityManager class and its associated classes.
Securitymanager is responsible for managing all of the user profiles as well as hadling who is currently logged in
User data is contained in a pickled dictionary with each key as a username and the item being a two item array containing
the password and the users admin status

DS.write_to_user_file(user_data)
"""
import Datastore
import Ports

DS = Datastore.DataStore()
P = Ports


class SecurityManager(object):
    """
    Handles all interaction with the User functionality.
    Such as: log in/out, add or delete user. Makes use of SecManDB to interact with the pickle file where user data is stored
    As this is now a seperate module, the state needs to stay the same.
    """
    def __init__(self):
        self.editingUser = False
        self.is_admin_status = False

    def logIn(self, user):
        nuser = DS.getUser(user)
        if not nuser:  # is the username a valid username?
            return False
        if nuser.password == user.password:  # is the password correct?
            login_user = P.Users(name=nuser.name, admin=nuser.admin)
            DS.write_user_data(login_user)
            return True
        else:
            return False

    def logOut(self):
        """
        tick
        logs a current user out by setting the loggedInUser attribute to false
        """
        login_user = P.Users("", False)
        DS.write_user_data(login_user)

    def addUser(self, user):
        """
        tick
        checks if the user's name is already in the dict, if not it stores the user object to the users file
        """
        if not DS.getUser(user.name):
            DS.putUser(user)
            return True
        else:
            return False

    def delete_user(self, puser):
        """
        tick
        pass in a user object
        Checks to see if the user exists in the user dict, if so deletes it
        """
        return DS.removeUser(puser)

    def updatePassword(self, password, admin):
        """
        tick
        pass in a new user object
        checks to see if the user is in the user dict and the logged in user has admin privelages. if so, changes the password accordingly
        """
        raw_name = DS.get_reset_password_name()
        if "-->" in raw_name:
            name = raw_name[:-9]
        else:
            name = raw_name
        user = self.GetUserObject(name)
        print(f"name {user.name} : admin before {user.admin} - admin after {admin}")
        user.password = password
        user.admin = admin

        return DS.putUser(user)

    def GetUserObject(self, userName):
        return DS.getUser(userName)

    def GetUserList(self):
        return DS.getUserList()

    def remind_password(self, user):
        user_obj = self.GetUserObject(user)
        return user_obj.password
