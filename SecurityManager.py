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

'''
import pickle



class SecurityManager(object):
    """
    Handles all interaction with the User functionality. 
    Such as: log in/out, add or delete user. Makes use of SecManDB to interact with the pickle file where user data is stored
    As this is now a seperate module, the state needs to stay the same.
    """
    
    def __init__(self):
        '''
        '''
        self.loggedInUser = False
        self.editingUser = False
        self.SMDB = SecManDB()
        self.is_admin_status = False
        

    
    def logIn(self, user):
        '''
        tick
        call getUSer on secmanDB, check password with the user object returned by getUser
        if login sucessful store user object as SecurityManagers logedinuser attribute
        
                try:
            print(nuser.name, nuser.password, nuser.admin)
        except:
            print('user not found in dict')
        '''
        nuser = self.SMDB.getUser(user.name)
        
        
      
        if nuser == False: #is the username a valid username?
            return False
        else:
            if nuser.password == user.password: #is the password correct?
                self.loggedInUser = nuser.admin
               
                print(nuser.name, self.loggedInUser)
                myvar = [nuser.name, nuser.admin]
  
                # Open a file and use dump()
                with open('file.ptt', 'wb') as file:
      
                # A new file will be created
                    pickle.dump(myvar, file)
            
                file.close()
                
                
                return True

    def set_user_admin_status(self, status=False):
        pass
        
    def get_user_admin_status(self):
        pass
    
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

    def deleteUser(self, user):
        '''
        tick
        pass in a user object
        Checks to see if the user exists in the user dict, if so deletes it
        '''
        if self.SMDB.getUser(user.name):
            self.SMDB.removeUser(user)
        else:
            return False

    
    def updatePassword(self, user):
        """
        tick
        pass in a new user object
        checks to see if the user is in the user dict and the logged in user has admin privelages. if so, changes the password accordingly
        """
        if self.SMDB.getUser(user.name) and self.loggedInUser.admin == True:
            self.SMDB.removeUser(user)
            self.SMDB.putUser(user)
    
    def GetUserObject(self, userName):
        user = self.SMDB.getUser(userName)
        return user
    
    def GetUserList (self):
        userList = []
        userlist = self.SMDB.getUserList()
        return userlist
        
        
    
class SecManDB(object):
    '''This class handles all of the opening and closing of the CSV'''
    
    
    def __init__(self):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        pass
        
    def getUser(self, user):
        '''
        tick
        pass in a username looks for given user in file
        if found, create a user object, fill it with the users data and return the object
        if not found, return False
        '''
        
        with open('filename.pickle', 'rb') as handle:
            userDict = pickle.load(handle)
        if user in userDict:
            password = userDict[user][0]
            admin = userDict[user][1]
            thisUser = User(user, password, admin)
        else:
            thisUser = False
        
        return thisUser
    
    def getUserList(self,):
        '''
        tick
        returns a list of all the user objects
        '''
        userList = []
        with open('filename.pickle', 'rb') as handle:
            userDict = pickle.load(handle)
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

        #create details array
        details = ['',False]
        details[0] = user.password
        details[1] = user.admin

        
        with open('filename.pickle', 'rb') as handle:
            userDict = pickle.load(handle)
        userDict[user.name] = details
        with open('filename.pickle', 'wb') as handle:
            pickle.dump(userDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def removeUser(self,user):
        '''
        pass in a user object
        removes a given user from the user list
        '''
        with open('filename.pickle', 'rb') as handle:
            userDict = pickle.load(handle)
        userDict.pop(user.name, None)
        with open('filename.pickle', 'wb') as handle:
            pickle.dump(userDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
class User(object):
    '''
    Used to create a user object, containing all the user`s info (username, password, admin status).
    '''
	
    def __init__(self, name, password, admin = False):
        self.name = name
        self.password = password
        self.admin = admin

    def get_user_status(self):
        return admin
#SM = SecurityManager()
         
#with open('filename.pickle', 'rb') as handle:
    #userDict = pickle.load(handle)
#print(userDict)





    
    
