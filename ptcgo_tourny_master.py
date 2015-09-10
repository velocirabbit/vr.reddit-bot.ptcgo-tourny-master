"""
  Manager for PTCGO tournaments on /r/ptcgo

  @Author: /u/iforgot120
  @Email: www.velocirabbit@gmail.com
"""
import curses
import datetime
import os
import tourny_daemon

from ptcgoTMDisplayStr import *
from config_bot import TZ_OFFSET

def setShorterEscDelay():
  '''
    Sets the ESCDELAY environment variable of the platform to 25 ms if it hasn't
    been set before.
  '''
  try:
    os.environ['ESCDELAY']
  except KeyError:
    os.environ['ESCDELAY'] = '25'

def setCursor(echo_visibility = False):
  '''
    Convenience function to turn echo and cursor visibility on/off.
    
    Arguments:
      echo_visibility: [Boolean] True for echo on/cursor visible, false
        otherwise.
  '''
  if echo_visibility:
    curses.echo()
    curses.curs_set(1)
  else:
    curses.noecho()
    curses.curs_set(0)

def printLong(long_string, width):
  '''
    Parsing and textwrapping a long string.
    
    Arguments:
      long_string: string to be wrapped [String]
      width: max width of each line of the string after wrapping [Int]
      
    Returns: [String]
  '''
  string = ''
  paragraphs = long_string.split('\n')
  _indentRe = re.compile('^(\W+)')  # Match all forms of indents
  for paragraph in paragraphs:
    line = textwrap.fill(paragraph, width = width)
    string += line + '\n'
  return string

def returnToMain():
  '''
    Convenience function for returning to the main menu.
  '''
  setCursor(0)
  mainMenu()
  
def yesnoConfirm():
  '''
    Curses input for "yes or no" input.
    
    Returns: [Boolean]
  '''
  setCursor(0)
  confirm = body.getkey()
  if confirm.lower() == 'y':
    return True
  elif confirm.lower() == 'n':
    return False
  elif confirm == chr(27):
    returnToMain()
    return
  
def mainMenu():
  '''
    Displays the main menu in the body.
  '''
  paintHeader()
  body.clear()
  n = daemon.getTName()
  if n:
    body.addstr(0, (curses.COLS - len(strStatusTourny.format(n))) // 2 - 1,
                strStatusTourny.format(n))
    body.addstr(2, 0, strMenuTourny)
  else:
    body.addstr(0, (curses.COLS - len(strStatusNoTourny)) // 2 - 1,
                strStatusNoTourny)
    body.addstr(2, 0, strMenuNoTourny)
    
  while True:
    c = body.getkey()
    if c.lower() == 'n':
      newTournament()
    elif c.lower() == 'q':
      exit(1)
    
def paintHeader():
  '''
    Displays the header in the header.
  '''
  today = datetime.date.today().isoformat() + ', ' + daemon.getRoundStr()
  header.clear()
  header.addstr(1, (curses.COLS - len(strHeader)) // 2 - 1, strHeader + '\n')
  header.addstr(2, (curses.COLS - len(strHeaderAuth)) // 2 - 1,
                strHeaderAuth + '\n')
  header.addstr(4, (curses.COLS - len(today)) // 2 - 1, today)
  header.hline(5, (curses.COLS - 25) // 2 - 1, '-', 25)
  header.refresh()
  
def inputText(strConfirm = "", num_only = False):
  '''
    Allows for typing in text and returning that string.
    
    
    Arguments:
      strConfirm: Confirmation [String] to display before returning it.
      num_only: [Boolean] indicating only numeral digits are allowed
      
    Returns: [String] (or [Int] if num_only)
  '''
  s = ""
  setCursor(1)
  curs = body.getyx()
  y = curs[0]
  x = curs[1]
  while True:
    c = body.getkey()
    if c == chr(27):  # 'Esc'
      returnToMain()
      return
    elif c == '\b':
      if s > '': s = s[:-1]
      if body.getyx()[1] == x: body.addstr(' ')
      else:
        body.clrtoeol()
    elif c == '\n' and s > '':
      body.addstr('\n\n' + printLong(strConfirm.format(s), width = curses.COLS))
      if yesnoConfirm(): break
      else:
        body.move(y, x)
        body.clrtobot()
        setCursor(1)
        s = ''
        continue
    elif c == '\n' and s == '':  # Prevents user from entering new lines
      body.move(getyx()[0] - 1, x)
      body.clrtobot()
    else:
      if num_only:
        try:
          if int(c) in range(10): s += c
        except ValueError:
          ncurs = body.getyx()
          body.move(ncurs[0], ncurs[1] - 1)
          body.clrtoeol()
      else:
        s += c

def newTournament():
  '''
    Creates and displays the new tournament wizard.
  '''
  today = datetime.datetime.now(TZ_OFFSET)
  body.clear()
  
  # Set tourname name
  body.addstr(printLong(strCreateTournyName, width = curses.COLS))
  new_name = inputText(strCreateTournyNameConfirm) + " Tournament"
  
def main(stdscr):
  global daemon, header, body
  
  stdscr = curses.initscr()
  stdscr.clear()
  header = curses.newwin(6, curses.COLS, 0, 0)
  body = curses.newwin(curses.LINES - 7, curses.COLS, 7, 0)
  
  stdscr.keypad(1)
  header.keypad(1)
  body.keypad(1)
  setCursor(0)
  curses.cbreak()
  
  daemon = tourny_daemon.TDaemon()
  mainMenu()  #TODO: Add dropdown menus to the body (or header?)
  
  curses.nocbreak()
  stdscr.keypad(0)
  setCursor(1)
  curses.endwin()
  daemon.answerQ.join()
  daemon.q.join()
    
if __name__ == '__main__':
  setShorterEscDelay()
  curses.wrapper(main)