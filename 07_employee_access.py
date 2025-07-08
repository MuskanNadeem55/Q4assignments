class Employee:
    def __init__(self, name, salary, ssn):
        self.name = name         
        self._salary = salary     
        self.__ssn = ssn          

# Test
emp = Employee("aryan", 75000, "124-65-8745")
print(emp.name)           
print(emp._salary)      
# print(emp.__ssn)        
print(emp._Employee__ssn) 