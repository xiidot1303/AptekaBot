def change_sort_type(text):
    if text == 'возрастание':
        return 'убывание'
    elif text == 'убывание':
        return 'возрастание'
    elif text == 'цене':
        return 'процентам'
    elif text == 'процентам':
        return 'цене'


def find_percent(text):
    text = str(text)
    try:
        i = text.index('%')
    
        r = ''
        i -= 1
        while True:
            if text[i] == ' ':
                break
            elif text[i] == ',':
                print('yea')
                r = '.' + r
            else:
                r = text[i] + r
            i -= 1
        print(float(r))
        return float(r)
    except:
        return 100
def sort_percent_grow(w):
    all_prices = [find_percent(i[0]) for i in w]

    c_all_prices = [i for i in all_prices]
    
    result = []
    for i in all_prices:
        
        
        result.append(w[c_all_prices.index(min(c_all_prices))])
        w.remove(result[-1])
        c_all_prices.remove(min(c_all_prices))
        
    return result



def sort_percent_wane(w):
    w = w
    all_prices = [find_percent(i[0]) for i in w]

    c_all_prices = [i for i in all_prices]
    
    result = []
    for i in all_prices:
        
        
        result.append(w[c_all_prices.index(max(c_all_prices))])
        w.remove(result[-1])
        c_all_prices.remove(max(c_all_prices))
        
    return result

def sort_price_grow(w):
    all_prices = []
    for i in w:
        if i[4] == str(i[4]):
        
            i[4] = 0
        all_prices.append(i[4])

    c_all_prices = [i for i in all_prices]
    
    result = []
    for i in all_prices:
        
        
        result.append(w[c_all_prices.index(min(c_all_prices))])
        w.remove(result[-1])
        c_all_prices.remove(min(c_all_prices))
        
    return result




def sort_price_wane(w):
    all_prices = []
    for i in w:
        if i[4] == str(i[4]):
        
            i[4] = 0
        all_prices.append(i[4])


    c_all_prices = [i for i in all_prices]
    
    result = []
    for i in all_prices:
        
        
        result.append(w[c_all_prices.index(max(c_all_prices))])
        w.remove(result[-1])
        c_all_prices.remove(max(c_all_prices))
    return result
