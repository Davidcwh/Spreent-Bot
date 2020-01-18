class MySpree:

    def __init__(self, spree_name, min_amount, current_amount):
        self.spree_name = spree_name
        self.min_amount = min_amount
        self.current_amount = current_amount
        self.total_people = []

    def add_to_list(self, name_id):
        self.total_people.append(name_id)

    def to_dict(self):
        return {
            'Spree_name': self.spree_name,
            'min_amount': self.min_amount,
            'current_amount': self.current_amount,
            'remaining_amount': float(self.min_amount) - float(self.current_amount),
            'people_num': len(self.total_people),
            'total_people': self.total_people
        }

    def set_spree_name(self, input):
        self.spree_name = input

    def set_min_amount(self, input):
        self.min_amount = input

    def set_current_amount(self, input):
        self.current_amount = input
        
    def reset_values(self):
        self.spree_name = None
        self.min_amount = None
        self.current_amount = None
        self.total_people = None

