
# a function that returns an integer is written as follows
# def function_name(parameter: type) -> return_type:

# for documentation purposes, you can add a docstring to the function
# def function_name(parameter: type) -> return_type:
#   """docstring""" 
#   function_body

# the @ symbol is used to add a decorator to a function
# decorators are used to modify the behavior of a function or method
# for example, the @staticmethod decorator is used to define a static method in a class
#  the @classmethod decorator is used to define a class method in a class
# the @property decorator is used to define a property in a class
# the @abstractmethod decorator is used to define an abstract method in a class

# for the case of the firebase function, the @https_fn.on_request() decorator is used to define an http function
# the on_request_example function is the function that is called when the http function is triggered

# More documentation is in Guide.txt file

def my_function(name: str) -> int:
  """This function takes a name and prints a greeting"""
  print("Hello "+ name+ " from a function")
  return 2

print(my_function("Cephas"))

# the function above takes a string parameter and returns an integer

# a function can have a parameter that can either be a string or an integer
def my_function1(name: str| int) -> None:
  """This function takes a name and age and prints a greeting"""
  print("Hello "+ str(name)+ " you are years old")

my_function1("Cephas")
my_function1(23)


# the function can also return a string or an integer
def my_function2(name: str, age: int) -> str:
  """This function takes a name and age and returns a greeting"""
  return "Hello "+ name+ " you are "+ str(age)+ " years old"