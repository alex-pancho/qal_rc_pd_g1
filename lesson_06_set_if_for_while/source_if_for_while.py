age = 25

print(age >= 18)

if age >= 18:
    print("Ти повнолітній!")
else:
    print("ти не можеш це зробити!")


if age < 18:
    print("Ти дитина.")
elif age >= 18 and age < 25:
    # 1 * 0
    print("Ти молодь.")
else:
    print("Ти дорослий.")


# 0 * 0 = 0 
# 0 * 1 = 0
# 1 * 1 = 1
is_student = True
has_experience = False

if age >= 18 and is_student:
    # 1 * 1
    print("1: Ти студент і тобі більше =18 років")


if age < 18 or is_student:
    # 0 + 1
    print("1.2: Ти студент АБО тобі менше 18 років")

# 1 + 1 = 1
# 1 + 0 = 1
# 0 + 0 = 0

age = 17
is_student = True
has_experience = True
if age >= 18 and is_student:
    print("2: Ти студент і тобі більше 18 років.")
elif (age >= 25 and has_experience) and (is_student and has_experience):
    print("2: одна з двох умов вірна")
elif has_experience or is_student:
    print("2: Ти студент АБО з досвідом роботи")
else:
    print("2: Ти не можеш бути студентом або тобі менше 18 років.")

# loops

count = 0
while count <= 5:
    #print("1:", count)
    count += 1 # count = count + 1
    print("2:", count)

word = "Python"
index = 0
while index < len(word):
    print(word[index])
    index += 1

# count_2 = 1
# while count_2 >= 1:
#     count += 1 # count = count + 1
#     print("2:", count)
print(range(5))

for i in range(5):
    print(i)

for char in word:
    print(char)


numbers = [1, 3, 2, 1, 5]
for num in numbers:
    print(num)


age = 25
is_student = True

if age >= 18:
    print("You are an adult.")

    if is_student:
        print("And you are a student.")

        for semester in range(1, 4):
            print("Semester:", semester)
    else:
        print("But you are not a student.")
else:
    print("You are not an adult.")

for i in range(7):
    print("Outer loop, iteration:", i)

    # Вкладена умова
    if i % 2 == 0:
        print("This is an even iteration.")
    else:
        print("This is an odd iteration.")


for i in range(5):
    if i == 3:
        print("Break викликаний на i =", i)
        break
    print(i)


for i in range(5):
    if i == 2:
        print("Continue викликаний на i =", i)
        continue
    print(i)


target_value = 7
for i in range(5, 10):
    if i == target_value:
        print("Знайдено шукане значення:", i)
        break
    print(i)

for i in range(10):
    if i % 2 == 0:
        continue
    print("Непарне число:", i)
