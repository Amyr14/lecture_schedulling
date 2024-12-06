import numpy
from tqdm import tqdm

class Graph():
  def __init__(self, num_vertices):
    self.num_vertices = num_vertices
    self.adj = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
    
  def set_adj(self, adj):
    self.adj = adj  
    
  def is_adjacent(self, v1, v2):
    return self.adj[v1][v2]
    
  def get_neighbours(self, vertex):
    return [n for n, isAdj in enumerate(self.adj[vertex]) if isAdj]
  
  def get_degree(self, vertex):
    return len(self.get_neighbours(vertex))
  
  def get_adj_colors(self, vertex, coloration):
    neighbors = self.get_neighbours(vertex)
    adj_colors = []
    
    for n in neighbors:
      color = coloration[n]
      if color != -1 and color not in adj_colors:
        adj_colors.append(color)
      
    return adj_colors
  
  def get_saturation(self, vertex, coloration):
    adj_colors = self.get_adj_colors(vertex, coloration)
    return len(adj_colors)
  
  def valid_color(self, vertex, color, coloration):
    neighbours = self.get_neighbours(vertex)
    for n in neighbours:
      if coloration[n] == color:
        return False
    return True
  
  def _coloring_aux(self, vertex, coloration, num_colors):
    if vertex == self.num_vertices:
      return True
    
    for color in range(num_colors):
      if not self.valid_color(vertex, color, coloration):
        continue
      
      coloration[vertex] = color

      if not self._coloring_aux(vertex + 1, coloration, num_colors):
        coloration[vertex] = -1
        continue
      
      return True
    
    return False
  
  
  def coloring(self, num_colors):
    coloration = [-1] * self.num_vertices
    found_coloring = self._coloring_aux(0, coloration, num_colors)
    
    if found_coloring:
      return coloration
    
    return None
  
  
  def _coloring_heuristic_aux(self, coloration, num_colors, uncolored):
    if len(uncolored) == 0:
      return True
    
    vertex = uncolored.pop(0)
    
    for color in range(num_colors):
      if not self.valid_color(vertex, color, coloration):
        continue
        
      coloration[vertex] = color
      uncolored.sort(key=lambda v: (self.get_saturation(v, coloration), self.get_degree(v)), reverse=True)
      
      if not self._coloring_heuristic_aux(coloration, num_colors, uncolored):
        coloration[vertex] = -1
        continue
        
      return True
    
    return False
  
  def coloring_heuristic(self, num_colors):
    coloration = [-1] * self.num_vertices
    uncolored = sorted(
      list(range(self.num_vertices)),
      key=lambda v: self.get_degree(v),
      reverse=True
    )
    found_coloring = self._coloring_heuristic_aux(coloration, num_colors, uncolored)
    
    if found_coloring:
      return coloration

    return None