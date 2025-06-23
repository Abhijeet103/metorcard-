from collections import defaultdict
class MetroCard :
    def __init__(self , id ,  balance):
        self.id  =  id
        self.src = None
        self.balance  =  balance


    def add_balance(self , ammount):
        self.balance+=ammount

    def update_src(self ,  src):
        self.src =  src


from collections import defaultdict

class Station:
    def __init__(self, name):
        self._name = name
        self._total_amount = 0
        self._discount = 0
        self._passenger_history = defaultdict(int)

    @property
    def name(self):
        return self._name

    @property
    def total_amount(self):
        return self._total_amount

    @property
    def discount(self):
        return self._discount

    @property
    def passenger_history(self):
        # Return a copy to avoid external modification
        return dict(self._passenger_history)

    def add_amount(self, x):
        self._total_amount += x

    def add_discount(self, x):
        self._discount += x

    def add_passenger(self, passenger_type):
        self._passenger_history[passenger_type] += 1


class Fare :
    rates = {
        "ADULT": 200,
        "SENIOR_CITIZEN": 100,
        "KID": 50
    }

    @classmethod
    def get_fare(cls ,  type ,  is_round_trip):
        base =  cls.rates[type]
        if is_round_trip :
            base /=2
        return  base

