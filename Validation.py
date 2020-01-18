from MySpree import MySpree
from math import *

INVALID_AMOUNT_ERROR = "Your minimum amount for the spree exceeds the current amount. Please check again"
EMPTY_SPREE_ERROR = "spree_name cannot be empty"
INVALID_VALUE_MIN = "You have entered an invalid value for your minimum amount. Please enter digits only for minimum amount."
INVALID_VALUE_CURR = "You have entered an invalid value for your current amount. Please enter digits only for minimum amount."
INVALID_VALUE_SPENDING = "You have entered an invalid value for your spending amount. \nOnly digits are valid for the amount.\n\nPlease enter your spending amount again:"

class Validation:

    def __init__(self, myspree):
        self.mySpree = myspree
    
    def isFloat(self, input):
        try:
            float(input)
            return True
        except ValueError:
            return False

    def isValidAmount(self, input):
        if not(self.isFloat(str(input))):
            return INVALID_VALUE_SPENDING
        else:
            return ""

    def validation_check(self):
        if len(str(self.mySpree.spree_name).strip()) == 0:
            return EMPTY_SPREE_ERROR
        if not(self.isFloat(str(self.mySpree.min_amount))):
            return INVALID_VALUE_MIN
        elif not(self.isFloat(str(self.mySpree.current_amount))):
            return INVALID_VALUE_CURR
        elif float(self.mySpree.min_amount) <= float(self.mySpree.current_amount):
            return INVALID_AMOUNT_ERROR
        else:
            self.mySpree.min_amount = "%.2f" % (float(self.mySpree.min_amount))
            self.mySpree.current_amount = "%.2f" % (float(self.mySpree.current_amount))
            return ""
