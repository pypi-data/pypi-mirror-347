from typing import Literal
import os, sys, re, msvcrt
from colorama import Fore, Back, Style
os.system

# --- WRITE

def write(*text, flush=True):
    """Communication is a key fella (print() is ass so use this instead)"""

    text = [str(t) for t in text]
    sys.stdout.write(" ".join(text))
    if flush: sys.stdout.flush()

def rewrite_line(text:str):
    """This quote is ass... Let me rewrite this shit..."""

    raw_text = clear_junk(text)
    term_width = os.get_terminal_size()[0]
    spaces = term_width-len(raw_text)
    hug_wall("left")
    write(text+" "*spaces)

# --- CLEAR

def clear():
    """Gets rid of mess on screen"""
    write("\033[2J")


def clear_line():
    """SOMEONE TRIES TO CENSOR SHIT !!!"""
    write("\033[2K")


# --- CURSOR

def hide_cursor():
    """Let's play hide and seek"""
    write("\033[?25l")

def show_cursor():
    """Show yourself!!!"""
    write("\033[?25h")

def place_cursor(x:int, y:int):
    """teleport cursor wherever you desire"""
    write(f"\033[{y};{x}H")


def move_cursor(x:int=0, y:int=0):
    """You think cursor is a player huh???"""

    # Y Movement
    if y > 0:   write(f"\033[{y}A")  # UP
    elif y < 0: write(f"\033[{-y}B") # DOWN

    # X Movement
    if x > 0:   write(f"\033[{x}C")  # RIGHT
    elif x < 0: write(f"\033[{-x}D") # LEFT


def hug_wall(direction: Literal["up", "down", "left", "right"]):
    """Slaps cursor to touch a wall (it seems like it tries to escape...)"""

    term_size = os.get_terminal_size()

    match direction:
        case "up":    move_cursor(0,  term_size[1])
        case "down":  move_cursor(0, -term_size[1])
        case "left":  move_cursor(-term_size[0], 0)
        case "right": move_cursor( term_size[0], 0)


def get_cursor() -> tuple[int, int]:
    """Where the fuck is my cursor??"""

    # ask for the damn position
    write("\033[6n");

    # read char by char until hits dot in the sentence
    resp = ""
    while True:

        ch = msvcrt.getch().decode("utf-8")
        resp += ch

        if ch == "R": # da do in the sentence
            break
    
    # clean mess to actually read da numbers lol
    pos = resp.split("[")[1].strip("R")
    y, x = pos.split(";")

    return int(x), int(y) # <-- respond with cursor position


# --- UTILITIES

def clear_junk(msg:str):
    """Yeet all characters that you cannot see"""
    return re.sub(r"\033\[[0-9;]*[A-Za-z]", "", msg)