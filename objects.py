from  deck_manager import *

deck = Deck("turkish.json")

data = {"key0":"şu", "key1":"that", "test":"test"}

card = deck.get_card("7")

print(card.__dict__)

lst = [1, 2, 3, 3, 3, 4]

for item in lst:
    if item == 3:
        lst.remove(item)

print(lst)