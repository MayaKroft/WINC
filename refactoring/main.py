__winc_id__ = "9920545368b24a06babf1b57cee44171"
__human_name__ = "refactoring"


from audioop import add
from plistlib import PlistFormat
from turtle import title
import weakref

from pyparsing import null_debug_action


class Homeowner:
    def __init__(self, name, address, needs):
        self.name = name
        self.address = address
        self.needs = needs

class Specialist:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Painter(Specialist):
    instances = []
    def __init__(self, name , price):
        super().__init__(name , price)
        self.__class__.instances.append(weakref.proxy(self))
        self.profession = 'painter'
        self.name = name
        self.price = price

class Plumber(Specialist):
    instances = []
    def __init__(self, name, price):
        super().__init__(name, price)
        self.__class__.instances.append(weakref.proxy(self))
        self.profession = 'plumber'
        self.name = name
        self.price = price

class Electrician(Specialist):
    instances = []
    def __init__(self, name, price):
        super().__init__(name, price)
        self.__class__.instances.append(weakref.proxy(self))
        self.profession = 'electrician'
        self.name = name
        self.price = price

prof_alice = Electrician('Alice Aliceville', 200)
prof_bob = Painter('Bob Bobsville', 250)
prof_craig = Plumber('Craig Cgraigsville', 180)
prof_craige = Plumber('Craige Cgraigesville', 170)

homeowner_alfred = Homeowner('Alfred Alfredson', 'Alfredslane 123', ['painter', 'plumber'])
homeowner_bert = Homeowner('Bert Bertson', 'Bertslane 231', ['plumber'])
homeowner_candice = Homeowner('Candice Candicedottir', 'Candicelane 312', ["electrician", "painter"])

def get_lowest(profession):
    class_name = profession.title()
    inst_list = globals()[f'{class_name}'].instances
    lowest_price = 0
    lowest_price_index = 0
    lowest_price_name = inst_list[0].name

    for i in range (len(inst_list)):
        if i == 0:
            lowest_price = inst_list[i].price
            lowest_price_index = i
            lowest_price_name = inst_list[i].name
        else:
            if inst_list[i].price > lowest_price:
                continue
            elif inst_list[i].price < lowest_price:
                lowest_price = inst_list[i].price
                lowest_price_index = i
                lowest_price_name = inst_list[i].name
            else:
                continue

    return lowest_price_name


def contracts(name):
    needs = globals()[f'homeowner_{name.lower()}'].needs
    contract_list = []
    for need in needs:
        if need == 'plumber':
            contract_list.append(get_lowest(need))
        if need == 'electrician':
            contract_list.append(get_lowest(need))
        if need == 'painter':
            contract_list.append(get_lowest(need))
    return contract_list



print(f"Alfred's contracts: {contracts('Alfred')}",)
print(f"Bert's contracts:, {contracts('Bert')}")
print(f"Candice's contracts: {contracts('Candice')}", )
