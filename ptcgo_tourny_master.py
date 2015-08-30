"""
  Manager for PTCGO tournaments on /r/ptcgo

  @Author: /u/iforgot120
  @Email: www.velocirabbit@gmail.com
"""
import calendar
import curses
import datetime
import formats
import os
import re
import textwrap
import time
import tourny_daemon

from config_bot import TZ_OFFSET

def setShorterEscDelay():
  '''
    Sets the ESCDELAY environment variable of the platform to 25 ms.
    
    Arguments: None
    
    Returns: None
  '''
  try:
    os.environ['ESCDELAY']
  except KeyError:
    os.environ['ESCDELAY'] = '25'
    
def setCursor(echo_visibility = False):
  '''
    Convenience function to turn echo and cursor visibility on/off.
    
    Arguments:
      echo_visibility: True for echo on and cursor visible, false otherwise.
        [Boolean]
    
    Returns: None
  '''
  if echo_visibility:
    curses.echo()
    curses.curs_set(1)
  else:
    curses.noecho()
    curses.curs_set(0)

def initAll():
  '''
    Loads up display strings from an external file, then initializes a currently
    running tournament (if any).
    
    Arguments: None
    
    Returns: None
  '''
  global display_strings, tourny_on, currentT
  
  if not os.path.isfile(os.path.join('docs', 'display_strings.txt')) or \
     not os.path.isfile('config_bot.py'):
    print("Missing config and/or display_strings file(s).")
    exit(1)
  else:
    with open(os.path.join('docs', 'display_strings.txt'), 'r') as f:
      strings = f.read()
      display_strings = strings.split('\n======\n')
  
  if tourny_on: currentT = tournament.load()
    
def paintHeader(stdscr):
  '''
    Displays the header in the passed Curses screen.
    
    Arguments:
      stdscr: [curses.WindowObject] screen to display the header in.
    
    Returns: None
  '''
  t = datetime.date.today().isoformat() + (', ' + currentT.getRoundStr() + \
      '\n' if tourny_on else '\n')
  stdscr.clear()
  stdscr.addstr(1, (curses.COLS - len(display_strings[0])) // 2 - 1,
                display_strings[0] + '\n')
  stdscr.addstr(2, (curses.COLS - len(display_strings[1])) // 2 - 1,
                display_strings[1] + '\n\n')
  stdscr.addstr(4, (curses.COLS - len(t)) // 2 - 1, t)
  stdscr.hline(5, (curses.COLS - 25) // 2 - 1, '-', 25)
  stdscr.refresh()
    
def returnToMain(stdscr):
  '''
    Convenience function for returning to the main menu.
    
    Arguments:
      stdscr: [curses.WindowObject]
      
    Returns: None
  '''
  setCursor(0)
  mainMenu(stdscr)
    
def printLong(long_string, width):
  '''
    Parsing and textwrapping a long string.
    
    Arguments:
      long_string: string to be wrapper [String]
      width: max width of each line of the string after wraping [Int]
    
    Returns: [string]
  '''
  string = ''
  paragraphs = long_string.split('\n')
  _indentRe = re.compile('^(\W+)') # Match all forms of indents
  for paragraph in paragraphs:
    line = textwrap.fill(paragraph, width = width)
    string += line + '\n'
  return string
    
def yesnoConfirm(stdscr):
  '''
    Curses input for yes or no input.
    
    Arguments:
      stdscr: [curses.WindowObject] screen to type in.
    
    Returns: [Boolean]
  '''
  setCursor(0)
  confirm = stdscr.getkey()
  if confirm.lower() == 'y':
    return True
  elif confirm.lower() == 'n':
    return False
  elif confirm == chr(27):
    returnToMain(stdscr)
    return
    
def inputText(stdscr, y = 0, x = 0, pre = "", post = "", num_only = False):
  '''
    Curses screen for typing in text and returning that string.
    
    Arguments:
      stdscr: [curses.WindowObject] screen to type in.
      y: y-coordinate of the screen to start display. Defaults to 0. [Int]
      x: x-coordinate of the screen to start display. Defaults to 0. [Int]
      pre: Confirmation [String] pt 1
      post: Confirmation [String] pt 25
      num_only: [Boolean] indicating only numeral digits are allowed
     
    Returns: [String] (or [Int] if num_only)
  '''
  s = ""
  setCursor(1)
  while True:
    c = stdscr.getkey()
    if c == chr(27): # 'Esc'
      returnToMain(stdscr)
      return
    elif c == '\b':
      if s > '': s = s[:-1]
      if stdscr.getyx()[1] == x: stdscr.addstr(' ')
      else:
        stdscr.clrtoeol()
    elif c == '\n' and s > '':
      stdscr.addstr('\n\n' + printLong(pre + s + post, width = curses.COLS))
      if yesnoConfirm(stdscr): break
      else:
        stdscr.move(y, x)
        stdscr.clrtobot()
        setCursor(1)
        s = ''
        continue
    elif c == '\n' and s == '': # Prevents user from entering new lines
      stdscr.move(getyx()[0] - 1, 8)
      stdscr.clrtobot()
    else:
      if num_only:
        try:
          if int(c) in range(10): s += c
        except ValueError:
          curs = stdscr.getyx()
          stdscr.move(curs[0], curs[1] - 1)
          stdscr.clrtoeol()
      else:
        s += c
  return s if not num_only else int(s)

def printCalendar(stdscr, y = 0, x = 0, date = today, highlight_arrow = 0):
  '''
    Creates and displays a calendar showing the given month in the given year.
    By default, displays this month's calendar in the center of the screen.
    
    Arguments:
      stdscr: [curses.WindowObject] screen to display the calendar in.
      y: y-coordinate of the screen to start display. Defaults to 0. [Int]
      x: x-coordinate of the screen to start display. Defaults to 0. [Int]
      date: [datetime.datetime] object of the date you want the cursor to
        initially highlight. Defaults to today.
      highlight_arrow: 0 (default) if cursor not on either arrow, 1 if on left,
        2 if on right. [Int]
    
    Returns: None
  '''
  stdscr.move(y, x)
  stdscr.clrtobot()
  dow_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
  margin = ' ' * x
  monthrange = calendar.monthrange(date.year, date.month)
  
  standout_1 = curses.A_STANDOUT if highlight_arrow == 1 else curses.A_NORMAL
  standout_2 = curses.A_STANDOUT if highlight_arrow == 2 else curses.A_NORMAL
  l_arrow_true = date.year > today.year or (date.year == today.year and \
                 date.month > today.month)
  l_arrow = '<' if l_arrow_true else ' '
  if l_arrow_true: stdscr.addstr(y, x, l_arrow, standout_1)
  stdscr.addstr(y, x + (27 - len(calendar.month_name[date.month]) - 5) // 2,
                calendar.month_name[date.month] + ' ' + str(date.year))
  stdscr.addstr(y, x + 26, '>', standout_2)
  stdscr.addstr('\n\n' + margin)
  
  for dow in dow_names:
    print_type = curses.A_STANDOUT if (date.weekday() + 1) % 7 == \
                 dow_names.index(dow) and highlight_arrow == 0 else \
                 curses.A_NORMAL
    stdscr.addstr(dow, print_type)
    if dow != 'Sat': stdscr.addstr(' ')
  stdscr.addstr('\n' + margin)
  
  dow_count = (monthrange[0] + 1) % 7
  for day in range(1, monthrange[1] + 1):
    if day == 1: stdscr.addstr(' ' * (dow_count * 4))
    date_str = (' ' if day >= 10 else '  ') + str(day)
    old = day < today.day and date.month == today.month and \
          date.year == today.year
    date_cursor = curses.A_STANDOUT if day == date.day and \
                  highlight_arrow == 0 else (curses.A_BOLD if not old \
                  else curses.A_DIM)
    stdscr.addstr(date_str, date_cursor)
    dow_count = (dow_count + 1) % 7
    next_str = '\n' + margin if dow_count == 0 else ' '
    stdscr.addstr(next_str)
  stdscr.addstr('\n\n')
  
def datePicker(stdscr, y = 0, x = 0, date = datetime.datetime.now(TZ_OFFSET)):
  '''
    Wrapper class to handle displaying a calendar and choosing a date.
    
    Arguments:
      stdscr: [curses.WindowObject] screen to display the calendar in.
      y: y-coordinate of the screen to start display. Defaults to 0. [Int]
      x: x-coordinate of the screen to start display. Defaults to 0. [Int]
      date: [datetime.datetime] object of the date to highlight. Defaults to
        today.
    
    Returns: Selected date as a [datetime.datetime] object
  '''
  highlight_arrow = 0
  printCalendar(stdscr, y, x, date)
  while True:
    c = stdscr.getkey()
    monthrange = calendar.monthrange(date.year, date.month)
    l_arrow = date.year > today.year or (date.year == today.year and \
              date.month > today.month)
    dow_num = (monthrange[0] + 1) % 7
    if c == '\n':
      if highlight_arrow != 0:
        mr = calendar.monthrange(date.year, (date.month - 2) % 12 + 1 if \
             highlight_arrow == 1 else date.month % 12 + 1)
        td = datetime.timedelta(days = mr[1])
        date = date - td if highlight_arrow == 1 else date + td
        l_arrow = date.year > today.year or (date.year == today.year and \
                  date.month > today.month)
        highlight_arrow = highlight_arrow if l_arrow else 2
        printCalendar(stdscr, y, x, date, highlight_arrow)
      else:
        if date >= today: return date
        else: stdscr.addstr('\n\n' + (' ' * x) + \
              "Great Scott! The start date\n" + (' ' * x) + \
              'can\'t be before today!')
    elif c == 't':
      date = today
      printCalendar(stdscr, y, x, date)
    elif c == 'KEY_UP':
      if date.day <= 7 - dow_num:
        highlight_arrow = 1 if l_arrow else 2
      elif date.day > 7 - dow_num and date.day <= 7:
        date = date.replace(day = 1)
        highlight_arrow = 0
      else:
        td = datetime.timedelta(days = 7)
        date -= td
      printCalendar(stdscr, y, x, date, highlight_arrow)
    elif c == 'KEY_DOWN':
      if date.day >= monthrange[1] - 6:
        date = date.replace(day = monthrange[1])
      elif highlight_arrow != 0:
        highlight_arrow = 0
        date = date.replace(day = 1)
      else:
        td = datetime.timedelta(days = 7)
        date += td
      printCalendar(stdscr, y, x, date)
    elif c == 'KEY_LEFT':
      if highlight_arrow != 0 and l_arrow:
        highlight_arrow = 1
      elif date.day > 1:
        td = datetime.timedelta(days = 1)
        date -= td
        highlight_arrow = 0
      printCalendar(stdscr, y, x, date, highlight_arrow)
    elif c == 'KEY_RIGHT':
      if highlight_arrow != 0:
        highlight_arrow = 2
      elif date.day < monthrange[1]:
        td = datetime.timedelta(days = 1)
        date += td
        highlight_arrow = 0
      printCalendar(stdscr, y, x, date, highlight_arrow)
    elif c == chr(27):
      returnToMain(stdscr)
      return

def timePicker(stdscr, y = 0, x = 0, mode = 1):
  '''
    Function to pick a time. 12-hr mode (maybe make it a settings option to
    switch between 12-hr and 24-hr modes).
    
    Arguments:
      stdscr: [curses.WindowObject] scren to display this in.
      y: y-coordinate to start display. Defaults to 0. [Int]
      x: x-coordinate to start display. Defaults to 0. [Int]
      mode: Determines 24-hr mode (mode == 1) or 12-hr mode (mode == 0).
        [Boolean]
    
    Returns: [datetime.time]
  '''
  t = datetime.time(tzinfo = TZ_OFFSET)
  s = 0 # To determine what the cursor is on. 0 = hr, 1 = min, 2 = AM/PM
  typed = time.time()
  f = 0
  while True:
    hr_curs = curses.A_STANDOUT if s == 0 else curses.A_NORMAL
    min_curs = curses.A_STANDOUT if s == 1 else curses.A_NORMAL
    ampm_curs = curses.A_STANDOUT if s == 2 else curses.A_NORMAL
    h = t.hour - 12 if mode == 1 and t.hour > 12 else t.hour
    stdscr.addstr(y, x, '{}{}'.format('' if h > 9 else '0', str(h)), hr_curs)
    stdscr.addstr(':')
    stdscr.addstr('{}{}'.format('' if t.minute > 9 else '0', str(t.minute)),
                  min_curs)
    if mode == 1:
      stdscr.addstr(' {}'.format('AM' if t.hour < 12 else 'PM'), ampm_curs)
    c = stdscr.getkey()
    if c == '\n':
      return t
    elif c == chr(27):
      returnToMain(stdscr)
      return
    elif str(c) == 'KEY_RIGHT':
      s = (s + 1) % 3 if mode == 1 else (s + 1) % 2
      f = 0
    elif str(c) == 'KEY_LEFT':
      s = (s - 1) % 3 if mode == 1 else (s + 1) % 2
      f = 0
    elif str(c) == 'KEY_UP' or str(c) == 'KEY_DOWN':
      f = 0
      sign = 1 if str(c) == 'KEY_UP' else -1
      if s == 0: t = t.replace(hour = (t.hour + sign) % 24)
      elif s == 1: t = t.replace(minute = (t.minute + sign) % 60)
      elif s == 2: t = t.replace(hour = (t.hour + (12 * sign)) % 24)
    else:
      try:
        if int(c) in range(10):
          since_typed = time.time() - typed
          if f == 0 or (f == 1 and since_typed > 5):
            if s == 0:
              t = t.replace(hour = int(c) + 12 if t.hour >= 12 and mode == 1 \
                  else int(c))
            elif s == 1: t = t.replace(minute = int(c))
            f = 1
            typed = time.time()
          else:
            if s == 0: # This is a bit wonky, but still usable.
              h = (h % 10) * 10 + int(c)
              h = (h if h <= 12 else (0 if t.hour < 12 else 12)) if mode == 1 \
                  else (h if h <= 24 else 24)
              t = t.replace(hour = h + 12 if t.hour >= 12 and mode == 1 else h)
            elif s == 1:
              m = (t.minute % 10) * 10 + int(c)
              m = m if m < 60 else 59
              t = t.replace(minute = m)
      except ValueError:
        continue

def listPicker(stdscr, y = 0, x = 0, l = []):
  '''
    Curses screen for picking from a list.
    
    Arguments:
      stdscr: [curses.WindowObject] screen to display in
      y: y-coordinate to start display. Defaults to 0. [Int]
      x: x-coordinate to start display. Defaults to 0. [Int]
      l: [List] or tuple with the possible choices
      
    Returns: index number as [Int] of selected item in list
  '''
  s = 0
  stdscr.addstr(y, x, '< ')
  while True:
    stdscr.move(y, x + 2)
    stdscr.clrtoeol()
    stdscr.addstr(l[s], curses.A_STANDOUT)
    stdscr.addstr(' >')
    c = stdscr.getkey()
    if c == chr(27):
      returnToMain(stdscr)
      return
    elif c == 'KEY_RIGHT' or c == 'KEY_LEFT':
      sign = 1 if c == 'KEY_RIGHT' else -1
      s = (s + sign) % len(l)
    elif c == '\n':
      break
  return s

#TODO: Tuple of custom rules should be pulled from Rules module
def rulesPicker(stdscr, y = 0, x = 0):
  '''
    Select custom rules.
    
    Arguments:
      stdscr: [curses.WindowObject] screen to display in.
      y: y-coordinate to start display. Defaults to 0. [Int]
      x: x-coordinate to start display. Defaults to 0. [Int]
      
    Returns: [List[Boolean]] of rules chosen.
  '''
  x = x + 2
  rules = ('No Pokemon-EX', 'Basics Only', 'No Supporters')
  l = len(rules)
  f = [False] * l
  for r in range(1, l + 1):
    h = curses.A_STANDOUT if f[r - 1] else curses.A_NORMAL
    stdscr.addstr(y + r - 1, x + 2, rules[r - 1], h)
  
  s = 0
  while True:
    stdscr.move(y + s, x)
    stdscr.addstr('>')
    stdscr.move(y + s, x + 3 + len(rules[s]))
    stdscr.addstr('<')
    c = stdscr.getkey()
    if c == chr(27):
      returnToMain(stdscr)
      return
    elif c == 'KEY_DOWN':
      stdscr.addstr(y + s, x, ' ')
      stdscr.addstr(y + s, x + 3 + len(rules[s]), ' ')
      s = (s + 1) % l
    elif c == 'KEY_UP':
      stdscr.addstr(y + s, x, ' ')
      stdscr.addstr(y + s, x + 3 + len(rules[s]), ' ')
      s = (s - 1) % 1
    elif c == ' ':
      f[s] = not f[s]
      stdscr.move(y + s, x + 2)
      h = curses.A_STANDOUT if f[s] else curses.A_NORMAL
      stdscr.addstr(rules[s], h)
    elif c == '\n':
      stdscr.move(y + l, 0)
      stdscr.addstr('\n\n' + printLong(display_strings[19],
                    width = curses.COLS))
      if yesnoConfirm(stdscr): break
      else:
        stdscr.move(y + l, 0)
        stdscr.clrtobot()
        continue
  
def newTournament(stdscr):
  '''
    Creates and displays the new tournament wizard in stdscr.
    
    Arguments:
      stdscr: [curses.WindowObject] screen to display this in.
    
    Returns: None
  '''
  global today, tourny_on, currentT
  today = datetime.datetime.now(TZ_OFFSET)
  stdscr.clear()
  
  # Set tournament name
  stdscr.addstr(printLong(display_strings[6], width = curses.COLS) + \
                '\n\n        ')
  curs = stdscr.getyx()
  new_name = inputText(stdscr, curs[0], curs[1], display_strings[7],
                       " Tournament? (y/n)") + " Tournament"
  stdscr.clear()
  
  # Set tournament start time and date
  stdscr.addstr(printLong('    ' + new_name + display_strings[8],
                width = curses.COLS) + ('\n' * 4))
  curs = stdscr.getyx()
  start_date = datePicker(stdscr, curs[0], (curses.COLS - 27) // 2 - 1)
  stdscr.addstr(printLong('\n' + display_strings[16], width = curses.COLS) + \
                '\n\n        ')
  curs = stdscr.getyx()
  start_time = timePicker(stdscr, curs[0], (curses.COLS - 8) // 2 - 1)
  startdt = datetime.datetime.combine(start_date, start_time)
  
  # Set the length of each round and max number of players
  stdscr.clear()
  stdscr.addstr(printLong(display_strings[9] + str(start_date)[:10] + ' at ' + \
                str(start_time)[:8] + display_strings[10],
                width = curses.COLS) + '\n\n        ')
  curs = stdscr.getyx()
  rl = inputText(stdscr, curs[0], curs[1], display_strings[11], ' days? (y/n)',
                 True)
  rlength = datetime.timedelta(days = rl)
  stdscr.addstr('\n    ' + printLong(display_strings[12],
                width = curses.COLS) + '\n\n        ')
  curs = stdscr.getyx()
  maxplayers = inputText(stdscr, curs[0], curs[1], display_strings[13],
                          " players? (y/n)", True)
  
  # Set the format. If single or double elim, option to have round robin too
  stdscr.addstr(printLong('\n' + display_strings[14],
                width = curses.COLS) + '\n\n    ')
  curs = stdscr.getyx()
  format = listPicker(stdscr, curs[0], 8, tournament.formats)
  if format == 1 or format == 2:
    stdscr.addstr(printLong('\n\n\n' + display_strings[15],
                  width = curses.COLS))
    if yesnoConfirm(stdscr):
      stdscr.addstr(printLong('\n' + display_strings[21],
                    width = curses.COLS) + '\n\n        ')
      curs = stdscr.getyx()
      pre_rrobin = inputText(stdscr, curs[0], curs[1], '    ', " rounds? (y/n)",
                             True)
    else:
      stdscr.addstr(printLong('\n\n\n' + display_strings[22],
                    width = curses.COLS))
      if not yesnoConfirm(stdscr):
        stdscr.addstr(printLong('\n' + display_strings[23] + ' ' + \
                      str(maxplayers) + '.', width = curses.COLS) + \
                      '\n\n        ')
        curs = stdscr.getyx()
        num_rrobin = inputText(stdscr, curs[0], curs[1], '    ',
                               "rounds? (y/n)", True)
    # Set some house r00lzzz
    stdscr.clear()
    stdscr.addstr(printLong(display_strings[17], width = curses.COLS) + \
                  '\n\n        ')
    curs = stdscr.getyx()
    basef = listPicker(stdscr, curs[0], curs[1],
                       ('Theme', 'Standard', 'Expanded', 'Unlimited'))
    stdscr.addstr(printLong('\n\n' + display_strings[18],
                  width = curses.COLS) + '\n\n    ')
    curs = stdscr.getyx()
    rules = rulesPicker(stdscr, curs[0], curs[1])
    
    today = datetime.datetime.now(TZ_OFFSET)
    if startdt < today:
      startdt = today + datetime.timedelta(minutes = 1)
    
    # Create the tournament!
    currentT = tournament.Tournament(new_name, startdt, rlength, maxplayers)
    tourny_on = True
    stdscr.clear()
    stdscr.addstr(printLong(display_strings[20], width = curses.COLS))
    stdscr.getkey()
    returnToMain(stdscr)
    
def mainMenu(stdscr):
  '''
    Creates and displays the main menu in stdscr.
    
    Arguments:
      stdscr: [curses.WindowObject] to display the main menu in.
      
    Returns: None
  '''
  stdscr.clear()
  if tourny_on:
    stdscr.addstr(0, (curses.COLS - len(display_strings[3]) - \
                  len(currentT.name)) // 2 - 1, display_strings[3] + \
                  currentT.name)
    stdscr.addstr(2, 0, display_strings[5])
  else:
    stdscr.addstr(0, (curses.COLS - len(display_strings[2])) // 2 - 1,
                  display_strings[2])
    stdscr.addstr(2, 0, display_strings[4])
  
  while True:
    c = stdscr.getkey()
    if c.lower() == 'n':
      newTournament(stdscr)
    elif c.lower() == 'q':
      exit(1)
    
def main(stdscr):
  stdscr = curses.initscr()
  stdscr.clear()
  header = curses.newwin(6, curses.COLS, 0, 0)
  body = curses.newwin(curses.LINES - 7, curses.COLS, 7, 0)
  
  stdscr.keypad(1)
  header.keypad(1)
  body.keypad(1)
  setCursor(0)
  curses.cbreak()
  
  initAll()
  paintHeader(header)
  mainMenu(body) #TODO: Add menus to the body or maybe the header
  
  curses.nocbreak()
  stdscr.keypad(0)
  setCursor(1)
  curses.endwin()

if __name__ == '__main__':
  setShorterEscDelay()
  curses.wrapper(main)