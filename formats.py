FORMATS = ('Round robin', 'Single elimination', 'Double elimination')

class Format:
  '''
    Format class that deals with the tournament scheduling.
        
    Attributes:
      format: [Int] indicating the format (match to FORMATS tuple)
      preRobinRounds: [Int] of the number of pre-Round Robin rounds. 0 means
        none.
  '''
    def __init__(self, fCode, preRobinRounds = 0):
      '''
        Initializes the Format.
        
        Arguments:
          fCode: [Int] of the tournament format type (match to FORMATS tuple)
          preRobinRounds: [Int] of the number of pre-Round Robin rounds. 0
            means none.
      '''
      self.format = fCode
      self.preRobinRounds = preRobinRounds
      
    def getRound(self):
      '''
        Returns the round number as a string. If the tournament hasn't
        started yet, it's in preparation.
            
        Arguments: none
            
        Returns: [String]
      '''
      