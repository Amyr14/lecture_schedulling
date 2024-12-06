from graph import Graph
from pandas import DataFrame
import time

CLASS_DAYS = 5
TIMES_IN_DAY = 5
NUM_OF_TIMES = CLASS_DAYS * TIMES_IN_DAY

SUBJECTS = [
  {
    "name": "MTM",
    "workload": 5,
  },
  {
    "name": "PTG",
    "workload": 5,
  },
  {
    "name": "FIS",
    "workload": 4,
  },
  {
    "name": "GEO",
    "workload": 4,
  },
  {
    "name": "INF",
    "workload": 4,
  }
]

CLASSES = ['T1', 'T2']


def create_lectures(subjects, classes):
  lectures = []
  for subject in subjects:
    workload = subject.get("workload")
    for c in classes:
      lectures.extend([(subject.get("name"), c) for _ in range(workload)])
  return lectures


def create_adj(lectures):
  adj = [[0 for _ in range(len(lectures))] for _ in range(len(lectures))]
  for v1 in range(len(adj)):
    for v2 in range(v1, len(adj)):
      s1, c1 = lectures[v1]
      s2, c2 = lectures[v2]
      hasEdge = v1 != v2 and (s1 == s2 or c1 == c2)
      adj[v1][v2] = int(hasEdge)
      adj[v2][v1] = int(hasEdge)
  return adj


def create_schedule(lectures, coloring):
  if not coloring:
    print("Nenhuma configuração de horários encontrada!")

  schedule = [[[] for _ in range(CLASS_DAYS)] for _ in range(TIMES_IN_DAY)]
      
  for i in range(CLASS_DAYS):
    for j in range(TIMES_IN_DAY):
      for vertex, lecture in enumerate(lectures):
        if coloring[vertex] == j*5+i:
          schedule[i][j].append(lecture)
  
  return schedule
          
def print_schedule(schedule):
  week_days = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex']
  print(DataFrame(data=schedule, columns=week_days))


if __name__ == '__main__':
  
  # Criando aulas e matriz de adjacência
  lectures = create_lectures(SUBJECTS, CLASSES)
  adj = create_adj(lectures)
  
  # Criando grafo
  graph = Graph(len(lectures))
  graph.set_adj(adj)
  
  # Colorindo sem a heurística
  start_1 = time.time()
  coloring_1 = graph.coloring(num_colors=25)
  end_1 = time.time()
  
  # Colorindo com a heurística
  start_2 = time.time()
  coloring_2 = graph.coloring_heuristic(num_colors=25)
  end_2 = time.time()
  
  # Imprimindo os horários
  schedule_1 = create_schedule(lectures, coloring_1)
  schedule_2 = create_schedule(lectures, coloring_2)
  
  print('========== Solução sem heurística ==========')
  print_schedule(schedule_1)
  print(f'\nTempo: {end_1 - start_1}')
  
  print("\n\n")
  
  print('========== Solução com heurística ==========')
  print_schedule(schedule_2)
  print(f'\nTempo: {end_2 - start_2}')