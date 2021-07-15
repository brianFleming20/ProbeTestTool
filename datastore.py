'''
Created on 3 May 2017

@author: jackw
@amended by Brian F

Naming convention
- Variables = no spaces, capitals for every word except the first : thisIsAVariable
- Local functions = prefixed with _, _ for spaces, no capitals : _a_local_function

Dependencies
-NI VISA Backend
-Non standard python modules
    pyvisa
    pyserial


to do:
-complete button on TPW doesn't work
-TPW freezes if a probe is inserted
-add SQ probe to list

#         s = ttk.Separator(self.root, orient=VERTICAL)
#         s.grid(row=0, column=1, sticky=(N,S))

'''


import pickle




class DataStore():
    def __init__(self):
        load_data = None
        temp_data = None
        admin_load = None
       
        
        ########################
        # Main data file read  #
        ########################
    def get_user(self):
       
        with open('file.user', 'rb') as load_user_file:
            load_data = pickle.load(load_user_file)
        load_user_file.close()
        return load_data
        ###########################
        # Batch control file read #
        ###########################
    def get_batch(self):
        
        with open("file.batch", "rb") as load_batch_file:
            temp_load = pickle.load(load_batch_file)
        load_batch_file.close()
        print("batch = {}".format(temp_load))
        return temp_load
    
        ###########################
        # Admin control file read #
        ###########################
    def get_admin(self):
        with open('file.admin', 'rb') as load_admin_file:
            admin_load = pickle.load(load_admin_file)
        load_admin_file.close()
      
        return admin_load
    
    #######################################
    
    def get_ports(self):
        with open('file.ports', 'rb') as load_ports_file:
            port_load = pickle.load(load_ports_file)
        load_ports_file.close()
     
        return port_load
    
    #######################################
        
    def write_to_user_file(self, user_data):
        with open('file.user', 'wb') as user_file:
            pickle.dump(user_data, user_file)
        user_file.close()
        
    ########################################
    
    def write_to_batch_file(self, batch_data):
        with open('file.batch', 'wb') as batch_file:
            pickle.dump(batch_data, batch_file)
        batch_file.close()
    
    #########################################
    
    def write_to_admin_file(self, admin_data):
        with open('file.admin', 'wb') as file:
            pickle.dump(admin_data, file)
        file.close()
        
    #########################################
    
    def write_to_port_file(self, ports):
   
        with open('file.ports', 'wb') as port_file:
            pickle.dump(ports, port_file)
        port_file.close()
        
    ##########################################
    
    def add_to_user_file(self, user_data):
        user_load = []
        user_load.extend( self.get_user())
        user_load.append(user_data)
        self.write_to_user_file(user_load)
    
    #########################################
    
    def add_to_batch_file(self, batch_data):
        load_data = []
        load_data.extend(self.get_batch())
        load_data.append(batch_data)
        self.write_to_batch_file(load_data)
        
    #########################################
    
    def add_to_admin_file(self, admin_data):
        temp_load = []
        temp_load.append(self.get_admin())
        temp_load.append(admin_data)
        self.write_to_admin_file(temp_load)
        
    #########################################
    
    def get_user_admin_status(self):
        admin = []
        admin.extend(self.get_user())
  
        return admin[1]
    
    #########################################
    
    def get_username(self):
        user = []
        user.extend(self.get_user)
        return user[0]
    
    #########################################
    
    def get_programme_status(self):
        ok = []
        ok.extend(self.get_admin())
        if "1" in ok:
            return True
        else:
            return False
        
    ########################################
    
    def get_serial_num(self):
        sn = ""
        admin_file = self.get_admin()
        sn = admin_file[1]
        return sn
    
    def show_all_data(self):
        print(f"all data = main {self.get_main()}, batch {self.get_batch()}, admin {self.get_admin()}")