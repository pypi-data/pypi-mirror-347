# ability to import module from relative path
import sys; sys.path.insert(0,'./src'); sys.path.insert(0,'../src')

# determine 1st line of the address
import pandas as pd
from vipro_python.ai.address import simple_record, series_concat_addr1

def expect(the_test, expected):
  got = simple_record(the_test)
  if got != expected:
    print('expected={}, got={}'.format(expected, got))
  assert got == expected

def test_series_concat_addr1():
  # single line
  res = series_concat_addr1(pd.Series(['4 Penny Lane'], index=['address_1']))
  assert res == '4 Penny Lane'
  # two lines
  res = series_concat_addr1(pd.Series(['4 Penny Lane', 'Essex'], index=['address_1', 'address_2']))
  assert res == '4 Penny Lane, Essex'
  # three lines
  res = series_concat_addr1(pd.Series(['Flat 1', '4 Penny Lane', 'Essex'], index=['address_1', 'address_2', 'address_3']))
  assert res == 'Flat 1, 4 Penny Lane, Essex'
  # ignore NaN
  res = series_concat_addr1(pd.Series(['4 Penny Lane', None, 'Essex'], index=['address_1', 'address_2', 'address_3']))
  assert res == '4 Penny Lane, Essex'
  # wrong way around
  res = series_concat_addr1(pd.Series(['Flat 1', '4 Penny Lane', 'Essex'], index=['address_3', 'address_2', 'address_1']), ['address_3', 'address_2', 'address_1'])
  assert res == 'Flat 1, 4 Penny Lane, Essex'

# TODO: get working
# def test_broken():
#   expect(['36', 'The Pinnacle', 'Victoria Avenue'],
#     '36 The Pinnacle Victoria Avenue')

#   expect(['Flat 2', '34', 'Elderton Road'],
#     'Flat 2, 34 Elderton Road')

#   expect(['43', '12', 'Fairfax Drive'],
#     'Flat 43, 12 Fairfax Drive')

#   expect(['23 FLAT', 'The Plaza', 'Royal Mews'],
#     'Flat 23, The Plaza Royal Mews')

#   expect(['41', '9 Chartwell Plaza', 'Southchurch Road'],
#     'Flat 41 9 Chartwell Plaza Southchurch Road')

#   expect(['22b', '15', 'Ashburnham Road'],
#     'Flat 22b 15 Ashburnham Road')

#   expect(['22', '15a', 'Ashburnham Road'],
#     'Flat 22 15a Ashburnham Road')

#   expect(['(Flat 10)', '15a', 'Ashburnham Road'],
#     'Flat 10 15a Ashburnham Road')

def test_address2():
  expect(['1 Glendaurel Court', 'Milton Road', 'SS0 7JU'],
    '1 Glendaurel Court Milton Road')

  expect(['1', 'Glendaurel Court', 'Milton Road', 'SS0 7JU'],
    '1 Glendaurel Court Milton Road')

  expect(['Suite 20a', 'Thamesgate House', '33/41', 'Victoria Avenue'],
    'Suite 20a Thamesgate House 33/41 Victoria Avenue')

  expect(['(Lower) 104 Shaftesbury Avenue', 'Essex', 'TT1 7LP'],
    '104 Shaftesbury Avenue')

  expect(['1 (Upper) Princes Court 25C Princes Street', 'Southend-On-Sea', 'Essex', 'Ss1 1Qa'],
    '1 Upper Princes Court 25C Princes Street')

  expect(['Southend Ymca (Flat 9 F/F) Newlands', '85 Ambleside Drive', 'Southend-On-Sea', 'Ss1 2Fy'],
    'Southend Ymca Flat 9 F/F Newlands, 85 Ambleside Drive')

  expect(['(Unit 7) 495A London Road', 'Westcliff-On-Sea', 'Ss0 9Lg'],
    'Unit 7 495A London Road')

  expect(['(FIRST FLOOR)', '19 ROYAL TERRACE', 'SOUTHEND-ON-SEA'],
    'FIRST FLOOR 19 ROYAL TERRACE')