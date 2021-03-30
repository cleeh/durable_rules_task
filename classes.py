class Product:
  def __init__(self, name, price):
    self.name = name
    self.price = price
  
  def get_name(self):
    return self.name
  
  def get_price(self):
    return self.price

class Products(Product):
  def __init__(self, product, ea):
    super().__init__(product.name, product.price)
    self.ea = ea
  
  def get_ea(self):
    return self.ea
  
  def get_total_price(self):
    return self.price * self.ea

class ProductsList:
  def __init__(self, products_tuple):
    self.products_tuple = list(products_tuple) if isinstance(products_tuple, (tuple, list)) else list()
  
  def get_total_price(self):
    total_price = 0
    for products in self.products_tuple:
      total_price += products.get_total_price()
    
    return total_price

class Member:
  def __init__(self, name, mileage, addressee_no_list):
    self.name = name
    self.mileage = mileage
    self.addressee_no_list = addressee_no_list
  
  def get_name(self):
    return self.name

  def get_mileage(self):
    return self.mileage
  
  def get_addressee_no_list(self):
    return self.addressee_no_list
  
class Addressee:
  def __init__(self, no, name, area_no):
    self.no = no
    self.name = name
    self.area_no = area_no
  
  def get_no(self):
    return self.no
  
  def get_name(self):
    return self.name
  
  def get_area_no(self):
    return self.area_no

class Order:
  def __init__(self, products_list, payment_price, using_mileage, member, addressee):
    self.products_list = products_list
    self.payment_price = payment_price
    self.using_mileage = using_mileage
    self.member = member
    self.addressee = addressee
  
  def get_products_price(self):
    return self.products_list.get_total_price()
  
  def get_using_mileage(self):
    return self.using_mileage
  
  def get_payment_price(self):
    return self.payment_price
  
  def get_member(self):
    return self.member
  
  def get_addressee(self):
    return self.addressee
