__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *
from lorem import *
from difflib import SequenceMatcher
import peewee
from peewee import IntegrityError
import random
from playhouse.shortcuts import model_to_dict
from typing import List


def create_user(name, address, email, billing): 
    try:
        user = User.create(name = name, address = address, email = email, billing = billing)
        return user
    except IntegrityError:
        print('username already in use')

def search(term) -> List[Product]:
    products = Product.select()

    def simil(word,name):
        name_words = name.split()
        for n in name_words:
            if SequenceMatcher(None, word, n.lower()).ratio() > 0.66:
                return True
        return False

    def simil_t(word,product):
        tag_list = []
        for tag in product.tags:
            tag_list.append(tag.name)
        if word in tag_list:
            return True
        else:
            for tag in tag_list:
                if SequenceMatcher(None, word, tag).ratio() >= 0.66:
                    return True
        return False
        
    def simil_d(word,desc):
        desc = desc.lower()
        if word in desc:
            return True
        else:
            for d_w in desc.split():
                if SequenceMatcher(None, word, d_w).ratio() >= 0.66:
                    return True
        return False

    p_0 = list(products.where(Product.name == term)) 
    p_0 += [i for i in list(products.where(Product.name.contains(term))) if i not in p_0] 
    p_0 += [i for i in list(products.where(Product.description.contains(term))) if i not in p_0] 

    term = term.lower().split()#declared after the first few selections so it first grabs exact matches, the simil functions will still return the item if it matches on a case insensitive basis.

    for p in products.objects(): #iterator() raised a StopIteration so I could not use it, at first it worked and then stopped working on the exact same code, but objects seemed to work well
        if p in p_0:
            pass #so it skips anything already in the list
        else:
            if all([simil(w, p.name) for w in term]):
                p_0.append(p)
            elif all([simil_t(w, p) for w in term]):
                p_0.append(p)
            elif all([simil_d(w, p.description) for w in term]):
                p_0.append(p)
            else:
                pass
                
    return p_0
    
    
def list_user_products(user_id) -> List[Product]:
    user = User.get(User.id == user_id)
    return list(user.products)


def list_products_per_tag(tag_id) -> List[Product]:
    tag = Tag.get_by_id(tag_id)
    return list(tag.tag_p)
        

def add_product_to_catalog(user_id, product, tags, description, price, stock) -> None:

    if len(list_user_products(user_id)) < 20:
        t_list = []
        for t in tags:
            Tag.get_or_create(name = t)
            made_tag = Tag.get(Tag.name == t)
            t_list.append(made_tag.id)
        item = Product.create(name = product, user = user_id, description = description, price = price, stock = stock)
        item.tags.add(t_list)
    else:
        print('You have exceded your product limit')


def update_stock(product_id, new_quantity) -> Product.stock:
    Product.update(stock = new_quantity).where(Product.id == product_id).execute()
    return Product.get_by_id(product_id).stock


def purchase_product(product_id, buyer_id, quantity):
    item = Product.get_by_id(product_id)
    if item.stock >= quantity:
        try:
            #print(f'{item.name} stock was: {item.stock}')
            Transaction.create(seller = item.user, buyer = buyer_id, product = product_id, amount = quantity)
            update_stock(product_id= product_id, new_quantity= item.stock-quantity)
            item = Product.get_by_id(product_id)
            #print(f"""
            #{quantity} was bought 
            #{item.name} stock is: {item.stock}""")
        except IntegrityError:
            print('You cannot purchase from yourself')
    else:
        stock_message = 'it is out of stock.' if item.stock == 0 else f'only {item.stock} are left.'
        raise ValueError(f'The amount of {item.name} requested is not in stock, you requested {quantity} but {stock_message}')

def remove_product(product_id) -> None:
    item = Product.get(Product.id == product_id)
    item.delete_instance()


def populate_test_database(user_number,product_number,transaction_number) -> None:
    names = ['adil','asimar','bety','beto','carla','coro','carmilla','dante','evero','fabio','gaby','homer','idal','jovir','kalim','lome','mike','naomi','olive','pedro','quilos','roberto','samuel','toron','uva','vali','wombat','xandra','yovis','zilos']
    
    product_n_0 = ['pink','wool','red','potato','blue','orange','acrylic','cloth','fleece','metal','hand-dyed','hand-painted', 'hand-made']

    product_n_1 = ['bench','cushion','doll','board','sweater','ball','cosplay','blanket','glass','plate','toy','train','chair','table','carpet','t-shirt','yarn']

    tags = ['local', 'diy', 'natural', 'eco', 'recycle', 'upcycle', 'art', 'small bussiness']

    with db.atomic():
        for i in range(user_number):
            n = random.choice(names) + ' ' + random.choice(names)
            e = n.split()[0] + n.split()[1] + '@mail.com'
            a = random.choice(names) + ' road ' + str(random.choice(range(1, 100)))
            b = random.choice(range(1111111111111111,9999999999999999))
            create_user(name= n, address= a,  email= e, billing= b)
        for pn in range(product_number):
            u = User.select().order_by(peewee.fn.Random()).get()
            n = random.choice(product_n_0) + ' ' + random.choice(product_n_1)
            t = [n.split()[0],n.split()[1]] + random.sample(tags, 2)
            lorem = lorem_i(2) #random lorem ipsum selector for descriptions
            d= lorem[0] + ' ' + t[0] + ' ' + lorem[1] + ' ' + t[1] + ' ' + t[2] + ' ' + t[3]
            p = round((random.choice(range(150,40000))/100),2)
            s = random.choice(range(1,25))
            add_product_to_catalog(user_id = u.id,product= n, tags= t, description= d, price= p,stock= s)
        for t in range(transaction_number):
            p = Product.select().order_by(peewee.fn.Random()).get() #not checking owner so we can test errors
            b = User.select().order_by(peewee.fn.Random()).get()
            amount = Product.get_by_id(p.id).stock
            a = random.choice(range(1,amount+1)) #this allows for errors on purpose, tot est error responses
            purchase_product(product_id= p, buyer_id= b.id, quantity= a)


#some additional functions to test the workings of the file
    

def try_search():
    search_t = search('pink dol')
    print([i.name for i in search_t])

def delprods():
    for i in Product.select():
        remove_product(i.id)

def deltras():
    for i in Transaction.select():
        i.delete_instance()

def deltags():
    for i in Tag.select():
        i.delete_instance()

def printprods():
    for i in Product.select().objects():
        print(f"""Prod id: {i.id}
        user: {i.user.name}
        prod name: {i.name}
        prog_tags: {[t.name for t in i.tags]}""")

def printtags():
    for t in Tag.select().objects():
        print(f"""Tag id: {t.id}
        tag name: {t.name}""")

def printtras():
    for t in Transaction.select().objects():
        print(f"""Transaction id: {t.id}
        amount: {t.amount}
        prod name: {t.product.name}""")

def ppt(tag_id):
    for i in list_products_per_tag(tag_id):
        print(f"""Prod id: {i.id}
        user: {i.user.name}
        prod name: {i.name}
        prog_tags: {[t.name for t in i.tags]}""")

def ppu(user_id):
    for i in list_user_products(user_id):
        print(f"""Prod id: {i.id}
        user: {i.user.name}
        prod name: {i.name}
        prog_tags: {[t.name for t in i.tags]}""")


#populate_test_database(0,0,0)

#delpords()
#deltras()
#deltags()

#printprods()
#printtags()
#printtras()

#ppt(2)
#ppu(2)
