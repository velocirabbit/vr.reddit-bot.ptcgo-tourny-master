import datetime
import os
import queue
import threading
import time
import tournament
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
      tournament: [tournament.Tournament] that we're dealing with.
      reddit: reddit instance that it's connected to.
      watcher: [threading.Thread] that waits for time-based events and pushes
        tasks to daemon q.
      daemon: [threading.Thread] that executes tasks placed in its queue by
        either the main thread or the watcher thread.
      q: daemon's [queue.Queue]
      answerQ: [queue.Queue] to pull and return queries from
  '''
  
  def __init__(self):
    '''
      Initializes the daemon's settings.
    '''
    self.q = queue.Queue()
    self.daemon = threading.Thread(target = self.worker)
    self.daemon.daemon = True
    self.daemon.start()
    
    self.watcher = threading.Thread(target = self.eventWatcher)
    self.watcher.daemon = True
    self.watcher.start()
    
    self.answerQ = queue.Queue()
    
    self.reddit = self.newReddit()
    
    if os.path.isfile(os.path.join('docs', 'status.txt'):
      self.q.put(self.loadTournament())
      self.q.put(self.tournament.save())
    
  def initTournament(self, name, startdt, rlength, maxP = 0, started = False):
    '''
      Puts initTournamentQ function into q for the worker to perform.
            
      Arguments:
        name: the name of the tournament as a String
        startdt: start date and time of the tournament as a [datetime.datetime]
        rlength: length of a single round of the tournament as a
          [datetime.timedelta]
        maxP: maximum number of players allowed to join as an
          [int]. 0 means no max.
        started: [bool] flag indicating if the tourny has started.
    '''
    self.q.put(self.initTournamentQ(name, startdt, rlength, maxP, started))
                                            
  def initTournamentQ(self, name, startdt, rlength, maxP = 0, started = False):
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
    self.tournament = tournament.Tournament(name, startdt, rlength, maxP,
                                            started)

  def checkTournament(self):
    '''
      Puts checkTournamentQ() into q, then gets it from answerQ to return.
      
      Returns: [String] of the Tournament's name if one exists, else [Bool = F]
    '''
    self.q.put(self.checkTournamentQ())
    ans = self.answerQ.get(block = True)
    self.answerQ.task_done()
    return ans
    
  def checkTournamentQ(self):
    '''
      Returns the name of the tournament if one exists, otherwise returns False
      to indicate that there is currently no existing Tournament.
    '''
    if self.tournament != None: answer = self.tournament.name
    else: ans = False
    
    self.answerQ.put(ans)
  
  def loadTournament(self):
    '''
      Loads up a currently running tournament (e.g. after a crash or
      something).
      
      Arguments: None
      
      Returns: [tournament.Tournament]
    '''
    with open(os.path.join('docs', 'status.txt'), 'r') as f: s = f.read()
    s = s.split('\n')
    dt = [int(x) for x in s[1].split(' ')]
    tz = datetime.timezone(datetime.timedelta(hours = dt[5]))
    sdate = datetime.datetime(year = dt[0], month = dt[1], day = dt[2],
                              hour = dt[3], minute = dt[4], tzinfo = tz)
    today = datetime.datetime.now(TZ_OFFSET)                          
    self.tournament =  Tournament(s[0], sdate,
                                  datetime.timedelta(days = int(s[2])),
                                  int(s[3]), today > sdate)

  def eventWatcher(self):
    '''
      Waits for datetime-based events to start (i.e. when the starting
      datetime is reached) and passes relevant tasks to the daemon's queue.
    '''
    while True:
      now = datetime.datetime.now(TZ_OFFSET)
      if self.tournament.startdt >= now and not self.tournament.started:
        self.q.put(self.startTournament)
        
    
  def worker(self):
    '''
      Worker function put inside of a new Thread and given queue q of tasks.
    '''
    while True:
      i = self.q.get()
      i()
      self.q.task_done()

  def startTournament(self):
    '''
      Starts the tournament by posting a thread with matchups.
    '''
    pass

  def isLoggedInReddit(self):
    '''
      Tests to see if the tourny_daemon thread is logged into a reddit instance.
      
      Arguments: None
      
      Returns [boolean]
    '''
    try:
      return self.reddit.is_logged_in()
    except urllib.error.URLError:
      time.sleep(time_delay)
      return isLoggedInReddit()
      
  def newReddit(self):
    '''
      Creates and returns a new reddit instance, passing the bot's user_agent
      string.
            
      Arguments: None
            
      Returns: [praw.__init__.BaseReddit]
    '''
    try:
      return praw.Reddit(user_agent = user_agent)
    except urllib.error.URLError:
      time.sleep(time_delay)
      return self.new_reddit()
           
  def attemptLogin(self):
    '''
      Attempts to login to the passed reddit instance. If a URL error is
      encountered, it tries again.
            
      Arguments: None
                
      Returns: [Boolean] indicating success
    '''
    try:
      self.reddit.login(REDDIT_USERNAME, REDDIT_PASS)
      return True
    except urllib.error.URLError:
      time.sleep(time_delay)
      self.attempt_login()
      return False