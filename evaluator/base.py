from evaluator.homogenous import HomogenousEvaluator
from evaluator.heterogenous import HeterogenousEvaluator
from monitor.progress import ProgressMonitor
import multiprocessing
from util.config_reader import ConfigReader

def evaluator(population: list, config_filename: str, run_id: int, nb_generations: int, start_generation: int, current_generation: int):
  manager = multiprocessing.Manager()
  config = ConfigReader(config_filename)
  nb_processes = multiprocessing.cpu_count()
  processes = []
  process_output = manager.dict()
  process_output.clear()
  portions = apportion(population, nb_processes)
  for i in range(nb_processes):
    if config.get("pEvolutionAlgorithm", "str").endswith("HET"):
      process = HeterogenousEvaluator(i, config_filename, run_id, start_generation, portions[i], process_output)
    else:
      process = HomogenousEvaluator(i, config_filename, run_id, start_generation, portions[i], process_output)
    processes.append(process)
    process.start()
  if config.get("pDynamicProgressOutput", "bool"):
    process = ProgressMonitor(nb_processes, len(population), nb_generations, current_generation, process_output)
    processes.append(process)
    process.start()
  for p in processes:
    p.join()
  fitnesses = []
  for i in range(nb_processes):
    fitnesses.extend(process_output[i])
  return fitnesses
  
# helper function to distribute individual evaluation to different processes
def apportion(population: list, nb_processes: int):
  allocation = len(population) // nb_processes
  overflow = len(population) % nb_processes
  portions = []
  total = 0
  for i in range(nb_processes):
    portion = population[total : total + allocation]
    total += allocation
    if i < overflow:
      portion.append(population[total])
      total += 1
    portions.append(portion)
  return portions