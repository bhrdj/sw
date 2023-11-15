import curses as c, random, sys, os, pandas as pd
from a import *
def main(my_screen):
    c.curs_set(0)
    avatar = '*'
    hgt, wdt = my_screen.getmaxyx()

    # player_names = os.listdir('./player_data')
    pname = 'steven' # presume this was entered by user
    words = get_words(pname)

    yx = [hgt//2, wdt//2]
    yx_words = get_yx_words(words, hgt, wdt)

    hgt, wdt = my_screen.getmaxyx()
    while True:

        # CHALLENGE PROMPT
        my_screen.clear()
        correct = None
        if yx in yx_words.values(): # if I hit the challenge, get the challenge prompt
            words_yx = {str(v):k for k,v in yx_words.items()}
            w = words_yx[str(yx)]
            ans = words[w]
            response = quiz_box(w, ans, hgt, wdt, my_screen)
            my_screen.clear()
            yx_words = {k:v for k, v in yx_words.items() if v!=yx}

        # DRAW THE CURRENT GAME BOARD
        for w in yx_words:         # draw the word constellation
            my_screen.addstr(*yx_words[w], w)
        my_screen.addstr(*yx, avatar) # show the cursor/avatar
        if correct is not None:     # draw the celebration message
            my_screen.addstr(*yx, "CORRECT" if correct else f"{response}_shouldbe_{ans}")
        my_screen.refresh()
        k = my_screen.getkey()

        # MOVE AND ITERATE
        yx = move(k, yx, hgt, wdt)
        if k=='q': return None







# TODOS
#   - Check and reset screen size during each loop so I can zoom during the game.
#       - This will require recalculating/rescaling obstacle and cursor locations

#if pname in player_names:
#    ods = pd.ExcelFile(f'./player_data/{pname}')
#    history = ods.parse(sheet_name='history')
#else:
#    history = pd.DataFrame(columns=['sw','en','dtime','result'])
#scores = pd.DataFrame(swen, columns=['hr','day','week','month','year'])
