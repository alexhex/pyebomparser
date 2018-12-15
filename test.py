import sys

print (sys.version)


def convert(typ):
    func_name = 'convert_' + '_'.join(typ.lower().split(' '))
    return func_name


a = 'Item NUmber'
b = 'Qty'


print (convert(a))
print (convert(b))