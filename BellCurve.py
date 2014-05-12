import math

class BellCurve(object):

  def __init__(self, mean, var):
    self.mean = mean
    self.var = var
    self.sd = pow(var, 0.5)


  def probability(self, x):
    return (1/(self.sd*pow(2*math.pi, .5)))*math.exp(-(pow(x-self.mean, 2))/(2*self.var))

  def stdev(self, x):
    sd = (x - self.mean)/self.sd
    return sd

if __name__ == "__main__":
  
  bc = BellCurve(.5,.01)
  
  print bc.probability(.45)
  print bc.sdAway(0.45)

