en_ua = {"hello": "привіт", "good": "добре", "day": "день", "nice": "приємно", "you": "ти",}

en_text = "Good day! Nice to see you!"

means_1 = en_ua["good"]
print(means_1)

# str, int, float, bool, tuple, None, byte
with_tuple_dict =  {(1, 2, 3): 'значення1', 10: 'значення2'}
print(with_tuple_dict[(1, 2, 3)])

# used_params = {'name': 'Василь', 'age': 25, 'city': 'Київ',} 

used_params = {
    'name': 'Василь', 
    'age': 25, 
    'city': 'Київ',
} # "job": "IT spec",
user_age = used_params["age"]
print("user age", user_age)

# print(used_params["job"]) #KeyError

print("has job key", "job" in used_params)
print("has age key", "age" in used_params)
print("use get")
print("get job key", used_params.get("job", "Worker"))
print("get age key", used_params.get("age"))

all_keys = used_params.keys()
print(all_keys)
all_vals = used_params.values()
print(all_vals)
all_pairs = used_params.items()
print(all_pairs)

for i in used_params:
    print(i)

for i in used_params:
    print(i, used_params[i])

for v in used_params.values():
    print(v)

for k, v in used_params.items():
    print(k, v)

cleared_dict = {"k": "v1"}
cleared_dict.clear()
print(cleared_dict)

sec_dict = {"k1":"v1", "k2":"v2"}
new_dict = sec_dict.copy() #sec_dict # 
sec_dict.update({"k3": 123})
print(new_dict)

vals_1 = new_dict.get('ключ4', 'значення за замовчуванням')

vals_2 = new_dict.pop('k2', 'значення за замовчуванням')
print(new_dict)

sec_dict.update({1: 1})
print(sec_dict)

sec_dict["k1"] = "lskalskal"
sec_dict["k4"] = "hoho-hoh-ho"

print(sec_dict)
del sec_dict["k1"]
print("del k1", sec_dict)
list_tuple = (('ключ1', 'значення1'), ('ключ2', 'значення2'), ('ключ3', 'значення3'))
dict_from_tuple = dict(list_tuple)
print(dict_from_tuple)

list_lists = [['ключ4', 'значення4'], ['ключ5', 'значення5']]
dict_from_lists = dict(list_lists)
print(dict_from_lists)


some_keys = ('ключA', 'ключB', 'ключC', "a")
some_vals = ("valA", "valB", "valC", "ssd")
dict_from_pairs = dict(zip(some_keys, some_vals))
print(dict_from_pairs)


gen_dict = {x: x**2 for x in range(11) if x % 2 == 0}
print(gen_dict)
