
        
d = {'key1': [1,2,3,4,5], 'key2': [2], 'key3': [3]}
l = list(d.values())
f =[]
for i in l:
    for item in i:
        f.append(item)
# print(f)