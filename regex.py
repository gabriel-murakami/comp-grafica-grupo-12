import re

regex = re.compile(r'(?<=#)(\d{3}\,\d{1})\;(L:ON|L:OFF)\;(S:ON|S:OFF)')

while(True):
    x = input("Insira a entrada:\n")

    # result_search = regex.search(x)
    
    try:
        result_findall = re.findall(r'(\d{3}\,\d{1})\;(L:ON|L:OFF)\;(S:ON|S:OFF)', x)
        print(result_findall if len(result_findall) > 0 else False)

        # print(result_search.groups())
    except:
        continue
