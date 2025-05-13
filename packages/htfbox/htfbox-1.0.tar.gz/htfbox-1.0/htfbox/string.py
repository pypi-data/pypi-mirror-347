import os, re
from . import term

def align_center(text:str, width:int=-1) -> str:
    if width == -1: width = os.get_terminal_size()[0]
    text_len = len(term.clear_junk(text))
    text_gap = int(width/2 - text_len/2)
    result = " "*text_gap + text + " "*text_gap
    return result

def put_sticker(original:str, sticker:str, start:int) -> str:

    result = original[:start]
    result += sticker
    result += original[start+len(sticker):]
    
    return result