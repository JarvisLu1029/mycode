# 計算幾次方
def pow(x, y):
    return x ** y

# 簡單斷句
def segment_sentence(text):
    list_sentences = text.split(' ')

    return list_sentences

# class Car:
#     wheel = 4
#     year = 2023

#     def __init__(self, brand, model, price):
#         self.brand = brand
#         self.model = model
#         self.price = price

#         print('You create a Car Object')

#     def info(self, door=4):
        
#         return f'In {self.year}, {self.brand} has a car named {self.model} with {door} doors'
    
#     def get_discounted_price(self, discount):
#         discounted_price = self.price * discount
        
#         return int(discounted_price)


# if __name__ == '__main__':

    # 測試模組
    print(f'In myModule.py :{pow(7, 2)}')

