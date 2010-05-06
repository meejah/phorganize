import string

def WordWrap( text, indent ):
    """
    Word-wraps text at around 70 characters wide and
    optionally includes an indent (in spaces).
    """
    
    if len(text) <= 70:
        return text
    rtn = ''
    prefix = string.center( '', indent )
    while len(text) > 70:
        i = 70
        line = text[:70]
        while not text[i] in string.whitespace:
            line = line + text[i]
            i = i + 1
            if i >= len(text):
                break
        rtn = rtn + prefix + string.lstrip(str(line)) + '\n'
        text = text[i:]
    rtn = rtn + prefix + string.lstrip(text)

    return rtn.rstrip()
