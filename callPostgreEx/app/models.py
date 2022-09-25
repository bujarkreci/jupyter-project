import json
import locale

locale.setlocale(locale.LC_ALL, 'en_US')

class Datas:
    def __init__(self, firstname, lastname, address, city, state, country, title, price, qnt, total):
        self.firstname = firstname
        self.lastname = lastname       
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.title = title
        self.price = price
        self.qnt = qnt
        self.total = total
       
    def __iter__(self):
        yield from {
            "firstname": self.firstname, 
            "lastname" : self.lastname, 
            "address" : self.address, 
            "city": self.city, 
            "state" : self.state, 
            "country" : self.country, 
            "title" : self.title, 
            "price" : self.price, 
            "quantity" : self.qnt, 
            "total" : self.total
        }.items()
    
    def __str__(self):           
        return json.dumps(self.to_json())
        # return json.dumps(dict(self), default=default, ensure_ascii=False)
    
    def __repr__(self):
        return self.__str__()
    
    def to_json(self):
        to_return = {"firstname": self.firstname, "lastname" : self.lastname, "address" : self.address, "city": self.city,
                    "state" : self.state, "country" : self.country, "title" : self.title, "price" : self.price,
                    "quantity" : self.qnt, "total" : self.total}
        return to_return