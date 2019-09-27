from utils import getch
from termcolor import colored

def menu(items, prompt='', on_exit=None):
    if not on_exit: on_exit = exit
    items = list(items)
    if prompt: print(prompt)
    for index, item in enumerate(items):
        print('{}: {}'.format(index, item))
    choice = None
    while not choice:
        try:
            choice = getch()
            items[int(choice)]
        except (ValueError, IndexError):
            if ord(choice) == 3 or ord(choice) == 4 or choice.lower() == 'q':
                print('exiting...')
                on_exit()
            print('"{}" is an invalid choice.'.format(choice))
            choice = None

    return int(choice)
def show_fn(card, remaining, total):
    cur_num = total - remaining
    print("[{}/{}] ".format(cur_num, total) + colored(card.description, 'yellow', attrs=['bold', 'underline']))
    getch()
     
def rate_fn(card):
    print(colored(card.response, 'red', attrs=['bold']))
    return menu(["No idea", "Almost remembered", "Remembered", "Remembered well"])


