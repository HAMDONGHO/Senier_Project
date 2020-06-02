print('Hello')
#a,b=intput().split()
a=1
while a<10:
    print(a)
    a+=1

b=3.14
print(b)

c='Hello World'
print(c)

#LIST == Array in C
mathList=[37, 93, 59, 87]
print(sum(mathList))
print(max(mathList))
print(min(mathList))
print((mathList[1]+mathList[2]+mathList[3]+mathList[0])/4)
list1=[1.1, 2.2, 3.3, [4.4, 5.5]]
print(list1)
print(list1[3])
print(list1[-1][0])
print(list1[1:2]) 


strPrac ='I love python'
print(strPrac[4])
print(strPrac[-9])
print(strPrac[0:]);
print(strPrac[0:5]);


strPrac1=' heLLo worlD'
strPrac2=' worldo'
print((strPrac1+strPrac2)*3)
print(len(strPrac1+strPrac2))
print(strPrac2.find('w'))
print(strPrac1.upper())
print(strPrac1.lower())
print(strPrac1.title())
print(strPrac1[7:12])


tuple_data=(1,2,3)
print(tuple_data[0])

list_varyType=[1,'hello',3.14]
print(list_varyType[1])

num=[1,2,3,4]
fruit=['banana', 'apple', 'melon']
fruit.append('pineapple')
print(fruit)
fruit.pop()
print(fruit)
fruit.remove('apple')
print(fruit)
fruit.append('strPracawberry')
fruit.reverse()
print(fruit)
fruit.sort()
print(fruit)
print(len(fruit))
print(fruit.count('melon'))

tupNum=(1,2,3,4)
print(tupNum)
           
dic={'name':'AI MAKERS KIT', 'phone':92844239, 'list':[1,2,3]}
print(dic)
print(dic['name'])
print(dic['phone'])
dic['phone']=34087901
print(dic['phone'])
print(dic)
del dic['list']
print(dic)
print(dic['name'].lower())

text='3.14'
num=3
value_text = float(text)+num
print(value_text)
print('%.4f' %value_text)
newVal=text+str(num)
print(newVal)

xnum=1
ynum=[10,20,30]
if(xnum in ynum):
    print('xnum in ynum')
else:
    print('xnum not in ynum')

grade = 30
if grade>10 and grade<35:
    print(grade)
