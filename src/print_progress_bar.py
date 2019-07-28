import sys
import os
import random

ROWS, COLUMNS = os.popen('stty size', 'r').read().split()

def print_progress_bar(message, current, total, align = 50):
    unfilled_shape = '◌'
    filled_shape = '●'

    fraction_done = float(current) / float(total)
    num_tick_marks = 100 - align - 5 #40
    num_filled_tick_marks = int(num_tick_marks * fraction_done)
    filled = filled_shape*num_filled_tick_marks + unfilled_shape*(num_tick_marks - num_filled_tick_marks)
    percent = int(100 * fraction_done)
    align = max(align, 1+len(message))

    if percent < 10:
        percent = '  ' + str(percent)
    elif percent < 100:
        percent = ' ' + str(percent)
    else:
        percent = str(percent)

    progress_bar = '%s%s%s \033[38;5;155m\033[1m%s%%\033[0m' % (message, (align - len(message))*' ', filled, percent)
    progress_bar = progress_bar[0:int(COLUMNS)]

    sys.stdout.write('%s\r' % (progress_bar))
    sys.stdout.flush()
