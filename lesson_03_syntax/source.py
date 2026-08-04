# Walthrogout for the Python
one_line_string = "Hello students!"
one_more_line_string = 'Hi students!'
long_text = """Here you can write 
all what you wont.
And one more
and more
more!!!
"""
''' same as before '''
appples = 3
bananas = 4
total = appples + bananas
diff = appples - bananas
multi = appples * bananas
division = appples / bananas
print(total)
print(diff, multi, division)
"""
+       -       *       **      /       //      %      @
<<      >>      &       |       ^       ~       :=
<       >       <=      >=      ==      !=
"""
# Keywords
"""
False      await      else       import     pass
None       break      except     in         raise
True       class      finally    is         return
and        continue   for        lambda     try
as         def        from       nonlocal   while
assert     del        global     not        with
async      elif       if         or         yield
"""

print(1 > 2)
print(2 > 1)
print(1 == 2)

red_apples = True
green_apples = True
result = red_apples and green_apples
print(f"Can we by red and green if green {green_apples} and red {red_apples}: {result}")
red_apples = False
green_apples = True
result = red_apples and green_apples
print(f"Can we by red and green if green {green_apples} and red {red_apples}: {result}")
red_apples = False
green_apples = False
result = red_apples and green_apples
print(f"Can we by red and green if green {green_apples} and red {red_apples}: {result}")

red_apples = True
green_apples = True
result = red_apples or green_apples
print(f"Can we by red or green if green {green_apples} and red {red_apples}: {result}")
red_apples = False
green_apples = True
result = red_apples or green_apples
print(f"Can we by red or green if green {green_apples} and red {red_apples}: {result}")
red_apples = False
green_apples = False
result = red_apples or green_apples
print(f"Can we by red or green if green {green_apples} and red {red_apples}: {result}")

"""
(       )       [       ]       {       }
,       :       .       ;       @
"""
calc = (2 + 3) * 4
print("(2 + 3) * 4 = ", calc)

numbers = [0, 1, 2, 3]
item = numbers[0]
print('list item', item)

dictionary = {"apple": "яблуко", 'ключ': 'значення'}
set_elements = {1, 2, 3, "яблуко", 'ключ'}

if calc >= 20:
    print("Tra ta ta")
    print("Tra ta ta 2")

hello = "Greeeteeeeeeeeeeng!!!!"
print(hello)
print(hello.__len__())
print(len(hello))

a = 2; b = 3

# @decorator


decimal = 42
octal = 0o52
heximal = 0x2A
binar = 0b101010
print("Diff ", decimal, octal, heximal, binar)

long_number = 1_232_312_424_242
print(long_number)
"9_223_372_036_854_775_808"

one_float = 1.23000000000000000000000000000000000000000000000000001
sec_float = 12.3000000000000000000000000000000000000000000000000001
sif_float = 2.0e-3
sif_float2 = 2.0e3
print(sif_float, sif_float2)
if one_float == sec_float/10:  # unexpected result
    print("pass")

hello = "Greeeteeeeeeeeeeng!!!!"
print(hello[0])
print(hello[1])
print(hello[2])
print(hello[2:7])
for letter in hello:
    print(letter)

my_list = [1, 2, 3, 'Привіт']
print(my_list[0])
print("len for list:", len(my_list))

x = min(1, 2, 3)
y = max(1, 2, 3)
print("min and max", x, y)


year = 2016
event = 'Referendum'
print(f'Results of the {year} {event}')

for letter in hello:
    print(letter, end=",")
print()
print("min and max", x, y, sep="\t")

query_sting = "підказка, що буде виведена на екран і повинна пояснити,\
  що ми очікуємо від користувача:"

query_sting_2 = "Введіть ваше ім'я: "


varaiable = input(query_sting)
print(varaiable)
varaiable = input(query_sting_2)
print(varaiable)

out = "Results of the {} text {}".format(year, event)
out2 = "Results of the %i text %s" % (year, event)
print(out)
print(out2)
