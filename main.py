import json
from menu_generator import Menu

print('Парсер проксей приветствует тебя комрад!')
need_to_parse = Menu('Нужно ли парсить прокси с сайта?', 'Да', 'Нет').res

if need_to_parse:
    import free_proxy_parser

    x = Menu('С какой страницы парсить?', listens_cusom_user_input=True, input_check_function=int).res
    y = Menu('По какую?', listens_cusom_user_input=True, input_check_function=int).res
    x, y = map(int, (x, y))

    print('\nОк...')

    free_proxy_parser.parse(x, y)

    print('Готово -> parsed.json')

need_to_sort = Menu('Нужно ли сортировать прокси?', 'Да', 'Нет').res
if need_to_sort:
    import sorter

    s = """Введи json теги для проверки, например: 
 {'protocol':'SOCKS5', 'response':'<100'}
    
Что это значит:
 "'protocol':'SOCKS5'" значит, что протокол обязательно SOCKS5,
 ">100" значит, что значение должно быть int который больше 100,
 ">" и "<"- единственные знаки, которые поддерживаются для int значений(Еще есть == если значение записать в конкретном int),
 весь список свойств можно найти в parsed.json
"""
    def try_to_dump(val):
        a = json.loads(val.replace("'",'"'))
        return 1

    criteria_dict = json.loads(Menu(s, listens_cusom_user_input=True, input_check_function=try_to_dump).res.replace("'",'"'))
            
    ip_and_port_to_array_mode = Menu('Выводить отсортированные данные в формате массива вида "ip:port"', 'Да', 'Нет').res

    print('\nОк...')

    sorter.sort_proxies_by_criteria(criteria_dict, ip_and_port_to_array_mode)

    print('Готово -> sorted.json')