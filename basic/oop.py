#class consist of 2 things 
    #methods and properties

class computer:

    def __init__(self, cpu, ram):
        self.cpu = cpu
        self.ram = ram

    def config(self):
        print(self.cpu, self.ram)


com1=computer('ryzen5', '16gb')
com2=computer('i5', '8gb')

com1.config()
com2.config()


#init use
# Think of __init__() as the setup function for an object.

# When a new object is created:

# 1.Python creates an empty object.
# 2.__init__() automatically runs.
# 3.It fills the object with the initial data you want it to have.