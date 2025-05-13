from . import term, string
from colorama import Back, Fore

class LineMan:
    """one man, one line, update shit etc without writing spaghetti"""

    def __init__(self, y:int=-1):
        if y == -1: y = term.get_cursor()[1]
        self.y = y;
        self.text :list[str] = []

    def update(self, index:int=-1):

        if index == -1:
            for i in range(0, len(self.text)):
                term.place_cursor(0, self.y + i)
                term.rewrite_line(self.text[i])
            return

        term.place_cursor(0, self.y + index)
        term.rewrite_line(self.text[index])

def bar(now:float, total:float, width:int, inside_text:str=None):
    """sexy progress bar. self-explanatory"""

    now = min(now, total)

    left = int((now/total)*width)
    right = width - left

    text = " "*width
    if inside_text:
        text = string.align_center(inside_text, width)
    
    text = Back.WHITE+Fore.BLACK + text[:left] + Back.LIGHTBLACK_EX+Fore.WHITE + text[left:] + Back.RESET+Fore.RESET

    return text