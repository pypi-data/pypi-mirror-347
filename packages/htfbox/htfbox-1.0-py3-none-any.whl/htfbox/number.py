def human_readable(value:float, scale:float, prefixes:str|list[str], round_digits:int=0) -> str:

    index = -1
    while value >= scale:
        if index >= len(prefixes): break
        value /= scale
        index += 1
    
    if index == -1: return str(round(value, round_digits))
    return f"{round(value, round_digits)} {prefixes[index]}"