import datetime
import os
import queue
import threading as thrd
import time
import tournament as tnmt
import urllib.request
import warnings

with warnings.catch_warnings():
  warnings.simplefilter('ignore', PendingDeprecationWarning)
  import praw
    
from config_bot import *

class TDaemon:
  '''
    Daemon that takes care of the actual management, eg creating posts,
    creating matchups, etc.
        
    Attributes:
      t: [tournament.Tournament] that we're dealing with.
      r: reddit instance that it's connected to.
      watcher: [threading.Thread] that waits for time-based events and pushes
        tasks to daemon q.
      d: [threading.Thread] that executes tasks placed in its queue by either
        the main thread or the watcher thread.
      q: daemon's [queue.Queue]
      answerQ: [queue.Queue] to pull and return queries from
  '''
  def __init__(self):
    '''
      Initializes the daemon's settings.
    '''
    self.q = queue.Queue()
    self.d = thrd.Thread(target = self._worker)
    self.d.daemon = True
    self.d.start()
    
    self.watcher = thrd.Thread(target = self._eventWatcher)
    self.watcher.daemon = True
    self.watcher.start()
    
    self.answerQ = queue.Queue()
    
    self.r = self._newReddit()
    
    if os.path.isfile(os.path.join('docs', 'status.txt'):
      self.q.put(self._loadTQ())

  ##############################################################################
  ## Callable methods from outside. These put the Q method into daemon's      ##
  ## queue, then waits for the answer to appear in the answerQ and returns it ##
  ##############################################################################
  def initT(self, name, startdt, rlength, maxP = 0, started = False):
    '''
      Initializes a Tournament object.
            
      Arguments:
        name: the name of the tournament as a String
        startdt: start date and time of the tournament as a [datetime.datetime]
        rlength: length of a single round of the tournament as a
          [datetime.timedelta]
        maxP: maximum number of players allowed to join as an
          [int]. 0 means no max.
        started: [bool] flag indicating if the tourny has started.
    '''
    self.q.put(self._initTQ(name, startdt, rlength, maxP, started))
    self.q.put(self._saveTQ())
  
  def saveT(self):
    '''
      Saves the status of the tournament to an external file.
    '''
    self.q.put(self._saveTQ())
  
  def getTName(self):
    '''
      Returns the name of the tournament if one exists, otherwise returns False
      to indicate that there is currently no existing Tournament.
      
      Returns: [String] of the Tournament's name if one exists, else [Bool = F]
    '''
    self.q.put(self._getTNameQ())
    ans = self.answerQ.get(block = True)
    self.answerQ.task_done()
    return ans
    
  def getRoundStr(self):
    '''
      Returns a formatted string indicating which round the tournament is
      currently in. If no tournament is running, returns "No tournament"
      
      Returns: [String] 
    '''
    self.q.put(self.t.getRoundStr())
    ans = self.answerQ.get(block = True)
    self.answerQ.task_done()
    return ans
    
  def startT(self):
    '''
      Starts the tournament by posting a thread with matchups.
    '''
    pass
    
  ##############################################################################
  ## Q methods to be placed in daemon's queue. These perform the actual tasks.##
  ##############################################################################
  def _initTQ(self, name, startdt, rlength, maxP, started):
    '''
      Q method for initT()
    '''
    if self.t == None:
      self.t = tnmt.Tournament(name, startdt, rlength, maxP, started)

  def _saveTQ(self):
    '''
      Q method for saveT()
    '''
    with open.path.j
    
  def _loadTQ(self):
    '''
      Loads up a currently running tournament (e.g. after a crash).
    '''
    with open(os.path.join('docs', 'status.txt'), 'r') as f: s = f.read()
    s = s.split('\n')
    dt = [int(x) for x in s[1].split(' ')]
    tz = datetime.timezone(datetime.timedelta(hours = dt[5]))
    sdate = datetime.datetime(year = dt[0], month = dt[1], day = dt[2],
                              hour = dt[3], minute = dt[4], tzinfo = tz)
    today = datetime.datetime.now(TZ_OFFSET)                          
    self.t =  tnmt.Tournament(s[0], sdate, datetime.timedelta(days = int(s[2])),
                         int(s[3]), today > sdate)

  def _getTNameQ(self):
    '''
      Q method for getTName()
    '''
    if self.t != None: answer = self.t.name
    else: ans = False
    self.answerQ.put(ans)
  
  ##############################################################################
  ## Other initialization methods, mostly used with the object is first init. ##
  ##############################################################################
  def _eventWatcher(self):
    '''
      Waits for datetime-based events to start (i.e. when the starting
      datetime is reached) and passes relevant tasks to the daemon's queue.
    '''
    while True:
      now = datetime.datetime.now(TZ_OFFSET)
      if self.t.startdt >= now and not self.t.started: self.q.put(self.startT)
      
    
  def _worker(self):
    '''
      Worker function put inside of a new Thread and given queue q of tasks.
    '''
    while True:
      task = self.q.get()
      task()
      self.q.task_done()

  def _isLoggedInReddit(self):
    '''
      Tests to see if the tourny_daemon thread is logged into a reddit instance.
      
      Returns: [boolean]
    '''
    try:
      return self.r.is_logged_in()
    except urllib.error.URLError:
      time.sleep(time_delay)
      return isLoggedInReddit()
      
  def _newReddit(self):
    '''
      Creates and returns a new reddit instance, passing the bot's user_agent
      string.
            
      Returns: [praw.__init__.BaseReddit]
    '''
    try:
      return praw.Reddit(user_agent = user_agent)
    except urllib.error.URLError:
      time.sleep(time_delay)
      return self._newReddit()
           
  def _attemptLogin(self):
    '''
      Attempts to login to the passed reddit instance. If a URL error is
      encountered, it tries again.
                
      Returns: [Boolean] indicating success
    '''
    try:
      self.r.login(REDDIT_USERNAME, REDDIT_PASS)
      return True
    except urllib.error.URLError:
      time.sleep(time_delay)
      self._attempt_login()
      return False