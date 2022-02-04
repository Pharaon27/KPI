import string

s = ('hello')
a = string.ascii_lowercase
b = [letter in s for letter in string.ascii_lowercase]
if any([letter in s for letter in string.ascii_lowercase]):
    print('yes')
else:

    print('no')
a=1