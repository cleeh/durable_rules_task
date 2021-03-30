#-*- coding:utf-8 -*-

from durable.lang import *
from classes import *

products_tuple = (
    Products(Product('웨하스', 3900), 4),
    Products(Product('단백질 보충제', 18900), 2),
    Products(Product('커피믹스 60개', 8000), 3)
)
products_list = ProductsList(products_tuple)
member = Member('강형욱', 6900, [10, 25, 59, 103])
addressee = Addressee(59, '성서동 OO 아파트', 3)
order = Order(products_list, 76900, 500, member, addressee)

with ruleset('Product Validation'):
  @when_all(+m.name)
  def name(c):
    print('product has name "{}"'.format(c.m.name))
  
  @when_all(m.price > 0)
  def price(c):
    print('product price has no probelm: {} > 0'.format(c.m.price))
  
  @when_all(m.ea > 0)
  def ea(c):
    print('product at least one ({})'.format(c.m.ea))
  
  @when_all(m.total_price > 0)
  def products_price(c):
    print('products price has no problem: {} > 0'.format(c.m.total_price))

with ruleset('Member Validation'):
  @when_all(+m.name)
  def name(c):
    print('member has name "{}"'.format(c.m.name))
    
  @when_all(m.mileage >= 0)
  def mileage(c):
    print('mileage has no error {} > 0'.format(c.m.mileage))
    
  @when_all(m.addressee_no_list_length > 0)
  def addressee_no_list_length(c):
    print('member has addressee at least 1 ({})'.format(c.m.addressee_no_list_length))

with ruleset('Addressee Validation'):
  @when_all(+m.no)
  def addressee_no(c):
    print('addressee has serial no: {}'.format(c.m.no))
  
  @when_all(+m.name)
  def addressee_name(c):
    print('addressee has name: {}'.format(c.m.name))
  
  @when_all(m.area_no > 0)
  def addressee_no(c):
    print('addressee matches specific area: {}'.format(c.m.area_no))

with ruleset('Order Validation'):
  @when_all(
    (m.products_price > 0) &
      (m.payment_price >= 0) &
      (m.using_mileage >= 0))
  def parameters(c):
    print('parameters have no problem')

  @when_all(m.calculated_price == m.products_price)
  def payment(c):
    print('payment is correct')
    
  @when_all(m.member_mileage >= m.using_mileage)
  def mileage(c):
    print('using mileage is correct')

with ruleset('Delivery'):
  @when_all((m.delivery == DELIVERY_IMMEDIATE) & (-m.delivery_start_datetime) & (-m.delivery_courier_company))
  def delivery_immeidate(c):
    c.assert_fact({'delivery': '즉시배송', 'service': 'our company'})
  
  @when_all((m.delivery == DELIVERY_RESERVATION) & (+m.delivery_start_datetime) & (-m.delivery_courier_company))
  def delivery_reservation(c):
    c.assert_fact({'delivery': '예약배송', 'delivery_start_datetime': c.m.delivery_start_datetime, 'service': 'our company'})

  @when_all((m.delivery == DELIVERY_COURIER) & (-m.delivery_start_date) & (+m.delivery_courier_company))
  def delivery_courier(c):
    c.assert_fact({'delivery': '택배배송', 'delivery_courier_company': c.m.delivery_courier_company, 'service': 'other company'})
  
  @when_all((+m.delivery) & (m.service == 'our company'))
  def our_service(c):
    print('자사 배송건 추가')
    dictionary = {'delivery': c.m.delivery}
    if c.m.delivery_start_datetime: dictionary['delivery_start_datetime'] = c.m.delivery_start_datetime
    if c.m.delivery_courier_company: dictionary['delivery_courier_company'] = c.m.delivery_courier_company
    c.assert_fact(dictionary)
  
  @when_all((+m.delivery) & (m.service == 'other company'))
  def others_service(c):
    print('타사 배송건 추가')
    dictionary = {'delivery': c.m.delivery}
    if c.m.delivery_start_datetime: dictionary['delivery_start_datetime'] = c.m.delivery_start_datetime
    if c.m.delivery_courier_company: dictionary['delivery_courier_company'] = c.m.delivery_courier_company
    c.assert_fact(dictionary)
  
  @when_all((+m.delivery) & (-m.service))
  def output(c):
    start_datetime = c.m.delivery_start_datetime if c.m.delivery_start_datetime else '시간: X'
    courier_company = c.m.delivery_courier_company if c.m.delivery_courier_company else '택배회사: X'
    print('{}이 있습니다. ({}, {})'.format(c.m.delivery, start_datetime, courier_company))


# 규칙 적용
for products in products_tuple:
  post('Product Validation', {'name': products.get_name()})
  post('Product Validation', {'price': products.get_price()})
  post('Product Validation', {'ea': products.get_ea()})
  post('Product Validation', {'total_price': products.get_total_price()})

post('Member Validation', {'name': member.get_name()})
post('Member Validation', {'mileage': member.get_mileage()})
post('Member Validation', {'addressee_no_list_length': len(member.get_addressee_no_list())})

post('Addressee Validation', {'no': addressee.get_no()})
post('Addressee Validation', {'name': addressee.get_name()})
post('Addressee Validation', {'area_no': addressee.get_area_no()})

post('Order Validation', {
    'products_price': order.get_products_price(),
    'payment_price': order.get_payment_price(),
    'using_mileage': order.get_using_mileage()
    })
post('Order Validation', {
    'products_price': order.get_products_price(),
    'calculated_price': order.get_payment_price() + order.get_using_mileage()
    })
post('Order Validation', {
    'member_mileage': order.get_member().get_mileage(),
    'using_mileage': order.get_using_mileage()
    })

post('Delivery', {'delivery': DELIVERY_IMMEDIATE})
post('Delivery', {'delivery': DELIVERY_RESERVATION, 'delivery_start_datetime': '2021-03-30 16:00:00'})
post('Delivery', {'delivery': DELIVERY_COURIER, 'delivery_courier_company': '라떼택배'})
