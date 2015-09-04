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

def mainMenu():
  '''
    Displays the main menu in the body.
  '''
  paintHeader()
    
def paintHeader():
  '''
    Displays the header in the header.
  '''
  s = daemon.getRoundStr() if n else "No tournament"
  t = datetime.date.today().isoformat() + ', ' + s
    
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
    
if __name__ == '__main__':
  setShorterEscDelay()
  curses.wrapper(main)