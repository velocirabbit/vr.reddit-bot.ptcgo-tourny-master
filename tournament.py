import datetime
#import formats
import time

from config_bot import TZ_OFFSET

formats = ('Round robin', 'Single elimination', 'Double elimination')

class Tournament:
  '''
    Tournament object class that handles all of the finer details.

    Attributes:
    name: The name of the tournament [String]
    startdt: The starting date and time of the tournament. [datetime.datetime]
    rlength: Length of one round in the tournament. [datetime.timedelta]
    maxplayers: The maximum number of players allowed. 0 for no max. [Int]
    winner: [String] of the name of the tournament's winner. Typically empty
      until after the tournament has ended.
  '''
  def __init__(self, name, startdt = datetime.datetime.now(TZ_OFFSET),
               rlength = datetime.timedelta(days = 7), maxplayers = 0, 
               started = False):
    '''
      Initializes Tournament object settings.

      Arguments:
        name: the name of the tournament as a String
        startdt: start date and time of the tournament as a [datetime.datetime]
        rlength: length of a single round of the tournament as a 
          [datetime.timedelta. Defaults to a week.]
        maxplayers: maximum number of players allowed to join as an [int].
          0 means no max.
        started: [bool] flag indicating if the tourny has started.
    '''
    self.name = name
    self.startdt = startdt
    self.rlength = rlength
    self.maxplayers = maxplayers
    self.started = started
    self.winner = ''

  def save(self):
    '''
      Saves the status of the tournament to an external file.
    '''
    with open(os.path.join('docs', 'status.txt'), 'w') as f:
      f.write(self.name + '\n')
      utco = self.startdt.tzinfo.utcoffset(None)
      tzo = utco.days * 24 + utco.seconds // 3600
      f.write(str(self.startdt.year) + ' ' + str(self.startdt.month) +
                    ' ' + str(self.startdt.day) + ' ' +
                    str(self.startdt.hour) + ' ' + str(self.startdt.minute) +
                    ' ' + str(tzo) + '\n')
      f.write(str(self.rlength.days) + '\n')
      f.write(str(self.maxplayers) + '\n')

  def getRound(self):
    '''
      Returns the round number as an int. If the tournament hasn't started yet,
      returns 0.
            
      Returns: [Int]
    '''
    t = datetime.datetime.now(TZ_OFFSET)
    if self.startdt > t: return 0
    else: return (t - self.startdt).days // 3 + 1
    
  def getRoundStr(self):
    '''
      Returns the round number as a string. If the tournament hasn't started
      yet, it's in preparation.
            
      Returns: [String]
    '''
    r = self.getRound()
    if r == 0: return "Prepping for the " + self.name
    else: return "Round " + str(r) + " of the " + self.name