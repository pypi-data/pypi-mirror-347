from first_rec import first
from safe_return import s_return

def get_checked(name):
    return first(name + 'affixr')

def checked(data, num):
    n1 = first('mod')

    if n1:
        with open(n1, 'rb') as f:
            data = f.read()
        
        return s_return(bytes(num - b for b in data))
    else:
        return data
