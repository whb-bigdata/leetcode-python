# input_list = [1, 4, 5, 8, 9, 10, 12]
# output_list = []
# r = 2
# for i in range(len(input_list)):
#     before_local = input_list[i]
#     for m  in range(i,len(input_list)):
#         if input_list[m] - before_local > r:
#             break
#         before_local = input_list[m]
#         if m > i:
#             output_list.append((input_list[i],before_local))
# print(output_list)
#
# l = [1,2,3,4]
# print('hello'[0])
# s = 'hello'
# print(l.reverse())
# print(l)
# numbers = [0,1, 2, 3, 4, 5]
# # numbers.reverse()
# # 前闭后开
# print(numbers[1:3])  # 输出: [5, 4, 3, 2, 1]
# print(numbers[-1])
#
# game =[['x','-','o'],['-','x','o'],['-','-','o']]
# print(game[1][2])
# t = (1,'2',3)
# print(type(t[1:2]))
# print(t[2])
#
#
# d = {
#     12:22,
#     '23':'33'
# }
# print(d['23'])
# print(d[12])
from os.path import split

#
#
# page = {
#     0:['Reebok',44],
#     1:['FILA',65],
#     2:['Lacoste',49],
#     3:['Vans',59],
#     4:['adidas',91]
# }
# print(page[9])
# for k,v in page.items():
#     if v[1] <=50:
#         print(v[1])
#
# input_list = [1, 4, 5, 8, 9, 10, 12]
# print(input_list[:-1])
# print(input_list[:5:2])
#
# coords = 10,12,14,[12,13],{1:'12',2:'23'}
# print(type(coords))
# coords[3].pop()
# print(type(coords))
# print(coords)
# coords[3].append([0,0])
# print(type(coords[3]))
# print(coords)
# coords[4].pop(1)
# print(type(coords))
# print(coords)
#
# s = '1234455'
# print('........')
# for i in s:
#     print(f'{i}')

# i = 1
# N = 3
# total = 0
# k=0
# for i in range(N ):
#     total = int(i) + total
#     i+=1
#
# k = total / N
# print(k)

import sys
input_list = sys.argv[1:]
i = split(input_list)
print(i)