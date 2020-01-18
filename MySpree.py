class MySpree:

    def __init__(self, spree_name, min_amount, current_amount, id_name):
        self.spree_name = spree_name
        self.min_amount = min_amount
        self.current_amount = current_amount
        self.remaining_amount = min_amount - current_amount
        self.total_people = [id_name]

    def add_to_list(self, name_id):
        self.total_people.append(name_id)

    def to_dict(self):
        return {
            'Spree_name': self.spree_name,
            'min_amount': self.min_amount,
            'current_amount': self.current_amount,
            'remaining_amount': self.remaining_amount,
            'people_num': len(self.total_people),
            'total_people': self.total_people
        }
