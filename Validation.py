from MySpree import MySpree
from math import *

INVALID_AMOUNT_ERROR = "Your minimum amount for the spree exceeds the current amount. Please check again"
EMPTY_SPREE_ERROR = "spree_name cannot be empty"
INVALID_VALUE = "You have entered an invalid value for your minimum and current amount"


class Validation:

    def __init__(self, myspree):
        self.mySpree = myspree

    def validation_check(self):
        if len(self.mySpree.spree_name) == 0:
            return EMPTY_SPREE_ERROR
        if str(self.mySpree.current_amount).isdigit() and str(self.mySpree.min_amount).isdigit():
            return INVALID_VALUE
        elif float(self.mySpree.min_amount) <= float(self.mySpree.current_amount):
            return INVALID_AMOUNT_ERROR
        else:
            str(round(float(self.mySpree.min_amount), 2))
            str(round(float(self.mySpree.current_amount), 2))
