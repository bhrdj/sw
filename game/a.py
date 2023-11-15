import curses as c, random, sys, os, pandas as pd
from typing import Dict

def remove_quietly(lst,element):
    try:
        lst.remove(element)
    except:
        pass

def move(k, yx, hgt, wdt):
    if k=='KEY_UP':
        yx[0] = yx[0] - 1
    elif k=='KEY_DOWN':
        yx[0] = yx[0] + 1
    elif k=='KEY_LEFT':
        yx[1] = yx[1] - 1
    elif k=='KEY_RIGHT':
        yx[1] = yx[1] + 1
    if yx[0] >= hgt: yx[0] = 1
    elif yx[0] <= 0: yx[0] = hgt-1
    if yx[1] >= wdt: yx[1] = 1
    elif yx[1] <= 0: yx[1] = wdt-1
    return yx

def get_words(pname):
    "will ask for user input, returns dictionary of words qn's and an's"
    path = '../ss/ss05_nouns.txt'  # i should use the pname to get the path
    df = (
        ss_to_dict_of_dfs(path, index_col='singular')
        .popitem()
        [1]
        )
    return df.english.to_dict()

def ss_to_dict_of_dfs(path:str, index_col=0) -> Dict[str, list]:
    """
    Read a formatted vocabulary textfile into a dataframe.
    Parameter "index_col" chooses which textfile column will be the index.
        Default is the first column. (Typically Swahili, singular...)

    Example of format:
    ***
        ss03_verbs.txt

        REGULAR VERBS
        infinitive;     english
        kuanguka;       fall
        kufanya;        do, make
        kufika;         arrive
    ***
    """
    [fname, ext] = path.split('/')[-1].split('.')   # get filename without extension
    out = {}
    df = pd.read_csv(path, sep=';', skiprows=3, on_bad_lines='skip').dropna()
    df.columns = df.columns.str.strip()
    df = df.apply(lambda x: x.str.strip())
    if type(index_col)==int: # if index_col is an integer column-number, reassign it to that column name
        index_col = df.columns.tolist()[index_col]
    out[fname] = df.set_index(index_col)
    return out

def get_yx_words(words, hgt, wdt):
    board0 = [[i,j] for i in range(2,hgt-1) for j in range(2,wdt-2)]
    yx_words = {}
    for w in words:
        yx_words[w] = random.choice(board0)
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                remove_quietly(board0,(i,j))
    return yx_words

def quiz_box(w, check_ans, hgt, wdt, my_screen):
    prompt = (
        f"Answer the question, then press [ENTER]:\n"
        f"\n"
        f"Type the English translation of {w}"
        )
    response = prompt_box(prompt, hgt, wdt, my_screen)
    return response

def prompt_box(prompt, hgt, wdt, my_screen, options_dct=None):
    if options_dct is not None:
        raise Exception("I haven't programmed in the multiple choice concept yet")
    my_screen.clear()
    box1 = c.newwin((hgt*5)//6,wdt//2,hgt//12,wdt//4)
    box1.box()
    promptlines = prompt.split('\n')
    n = len(promptlines)
    while promptlines:
        box1.addstr(3-n+len(promptlines), 3, promptlines.pop())
    my_screen.refresh()
    box1.refresh()
    k = my_screen.getstr()
    return k
