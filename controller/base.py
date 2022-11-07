from pyroborobo import Controller
import globals
from controller.dog import DogController
from controller.sheep import SheepController
import util.categorise as categorise


class BaseController(Controller):

  def __init__(self, world_model):
    Controller.__init__(self, world_model) # mandatory call to super constructor
    if categorise.is_dog(self.get_id()):
      self.controller = DogController(self)
    else:
      self.controller = SheepController(self)

  def reset(self):
    self.controller.reset()

  def step(self):  # step is called at each time step
    if self.get_id() == 1:
      globals.swarm_fitness_monitor.track()
    self.controller.step()