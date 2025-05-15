from node import Node
from segment import Segment
import matplotlib.pyplot as plt




class Graph:
   def __init__(self):
       self.nodes = []
       self.segments = []


   def GetNodeByName(self, name):
       """Obtiene un nodo por su nombre"""
       for node in self.nodes:
           if node.name == name:
               return node
       return None


   def connect(self, name1, name2):
       """Conecta dos nodos existentes"""
       n1 = self.GetNodeByName(name1)
       n2 = self.GetNodeByName(name2)
       if n1 and n2:
           n1.neighbors.append(n2)
           return True
       return False




def AddNode(g, n):
   """Añade un nodo al grafo si no existe"""
   if n in g.nodes:
       return False
   g.nodes.append(n)
   return True




def AddSegment(g, segment_id, name1, name2):
   """Añade un segmento entre dos nodos"""
   n1 = g.GetNodeByName(name1)
   n2 = g.GetNodeByName(name2)


   if not n1 or not n2:
       return False


   s = Segment(n1, n2)
   s.id = segment_id
   g.segments.append(s)
   n1.neighbors.append(n2)
   return True




def DeleteNode(g, name):
   """Elimina un nodo y todos sus segmentos conectados"""
   node_to_remove = g.GetNodeByName(name)
   if not node_to_remove:
       return False


   # Eliminar segmentos relacionados
   g.segments = [s for s in g.segments
                 if s.origin != node_to_remove
                 and s.destination != node_to_remove]


   # Eliminar de las listas de vecinos
   for node in g.nodes:
       if node_to_remove in node.neighbors:
           node.neighbors.remove(node_to_remove)


   # Eliminar el nodo
   g.nodes.remove(node_to_remove)
   return True




def DeleteSegment(g, segment_id):
   """Elimina un segmento por su ID"""
   for segment in g.segments:
       if segment.id == segment_id:
           # Eliminar de la lista de vecinos
           if segment.destination in segment.origin.neighbors:
               segment.origin.neighbors.remove(segment.destination)
           # Eliminar el segmento
           g.segments.remove(segment)
           return True
   return False




def GetClosest(g, x, y):
   """Encuentra el nodo más cercano a unas coordenadas"""
   if not g.nodes:
       return None


   closest_node = None
   min_distance = float('inf')


   for node in g.nodes:
       distance = ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5
       if distance < min_distance:
           min_distance = distance
           closest_node = node


   return closest_node




def SaveGraphToFile(graph, filename):
   """Guarda el grafo en un archivo con formato legible"""
   try:
       with open(filename, 'w') as f:
           # Escribir nodos
           f.write("Nodes:\n")
           for node in graph.nodes:
               f.write(f"{node.name},{node.x},{node.y}\n")


           # Escribir segmentos
           f.write("Segments:\n")
           for segment in graph.segments:
               f.write(f"{segment.id},{segment.origin.name},{segment.destination.name}\n")
       return True
   except Exception as e:
       print(f"Error saving graph: {e}")
       return False




def LoadGraphFromFile(file_path):
   """Carga un grafo desde un archivo"""
   g = Graph()
   try:
       with open(file_path, 'r') as file:
           mode = None
           for line in file:
               line = line.strip()
               if not line:
                   continue


               if line == "Nodes:":
                   mode = "nodes"
                   continue
               elif line == "Segments:":
                   mode = "segments"
                   continue


               if mode == "nodes":
                   name, x, y = line.split(',')
                   AddNode(g, Node(name, float(x), float(y)))
               elif mode == "segments":
                   parts = line.split(',')
                   if len(parts) == 3:
                       seg_id, origin, dest = parts
                       AddSegment(g, seg_id, origin, dest)
       return g
   except Exception as e:
       print(f"Error loading graph: {e}")
       return None




def Plot(g):
   """Visualiza el grafo completo"""
   plt.figure(figsize=(10, 8))


   # Dibujar segmentos
   for segment in g.segments:
       plt.plot([segment.origin.x, segment.destination.x],
                [segment.origin.y, segment.destination.y], 'blue')


       # Flecha y costo
       plt.arrow(segment.origin.x, segment.origin.y,
                 segment.destination.x - segment.origin.x,
                 segment.destination.y - segment.origin.y,
                 head_width=0.3, head_length=0.5, fc='blue', ec='blue',
                 length_includes_head=True)


       midpoint_x = (segment.origin.x + segment.destination.x) / 2
       midpoint_y = (segment.origin.y + segment.destination.y) / 2
       plt.text(midpoint_x, midpoint_y, f"{segment.cost:.1f}",
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))


   # Dibujar nodos
   for node in g.nodes:
       plt.plot(node.x, node.y, 'ko', markersize=10)
       plt.text(node.x, node.y, node.name,
                horizontalalignment='center',
                verticalalignment='center',
                color='white',
                fontsize=8,
                weight='bold')


   plt.xlabel('X')
   plt.ylabel('Y')
   plt.title("Graph Visualization")
   plt.grid(True)
   plt.show()




def PlotNode(g, name):
   """Visualiza un nodo y sus conexiones"""
   target_node = g.GetNodeByName(name)
   if not target_node:
       print(f"Node '{name}' not found")
       return


   plt.figure(figsize=(8, 6))


   # Dibujar todos los nodos (en gris)
   for node in g.nodes:
       plt.plot(node.x, node.y, 'o', color='gray', markersize=8)
       plt.text(node.x, node.y, node.name,
                horizontalalignment='center',
                verticalalignment='center',
                color='black')


   # Resaltar el nodo objetivo (en rojo)
   plt.plot(target_node.x, target_node.y, 'o', color='red', markersize=10)
   plt.text(target_node.x, target_node.y, target_node.name,
            horizontalalignment='center',
            verticalalignment='center',
            color='white',
            weight='bold')


   # Dibujar conexiones del nodo objetivo
   for neighbor in target_node.neighbors:
       for segment in g.segments:
           if (segment.origin == target_node and segment.destination == neighbor) or \
                   (segment.origin == neighbor and segment.destination == target_node):
               plt.plot([segment.origin.x, segment.destination.x],
                        [segment.origin.y, segment.destination.y], 'blue')


               plt.arrow(segment.origin.x, segment.origin.y,
                         segment.destination.x - segment.origin.x,
                         segment.destination.y - segment.origin.y,
                         head_width=0.3, head_length=0.5, fc='blue', ec='blue',


                         length_includes_head=True)


               midpoint_x = (segment.origin.x + segment.destination.x) / 2
               midpoint_y = (segment.origin.y + segment.destination.y) / 2
               plt.text(midpoint_x, midpoint_y, f"{segment.cost:.1f}",
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))


   plt.xlabel('X')
   plt.ylabel('Y')
   plt.title(f"Connections of node '{name}'")
   plt.grid(True)
   plt.show()




def reachable_nodes(graph, start_node):
   visited = set()
   to_visit = [start_node]


   while to_visit:
       current = to_visit.pop()
       if current not in visited:
           visited.add(current)
           to_visit.extend([n for n in current.neighbors if n not in visited])


   return list(visited)
from path import Path
from node import Distance


from path import Path
from node import Distance


from path import Path
from node import Distance


from path import Path
from node import Distance


def FindShortestPath(graph, origin_name, dest_name):
   import heapq


   origin = graph.GetNodeByName(origin_name)
   destination = graph.GetNodeByName(dest_name)


   if not origin or not destination:
       return None


   # Lista de caminos a evaluar
   current_paths = []
   start_path = Path([origin])
   heapq.heappush(current_paths, (Distance(origin, destination), start_path))


   # Diccionario para registrar el menor coste real conocido a cada nodo
   best_costs = {origin: 0}


   while current_paths:
       _, current_path = heapq.heappop(current_paths)
       current_node = current_path.LastNode()
       current_cost = current_path.TotalCost()


       # Si ya encontramos un camino mejor antes, ignoramos este
       if current_cost > best_costs.get(current_node, float("inf")):
           continue


       # Llegamos al destino
       if current_node == destination:
           return current_path


       for neighbor in current_node.neighbors:
           if current_path.ContainsNode(neighbor):
               continue  # evita ciclos


           new_path = Path(current_path.nodes + [neighbor])
           new_real_cost = new_path.TotalCost()


           if new_real_cost < best_costs.get(neighbor, float("inf")):
               best_costs[neighbor] = new_real_cost
               estimated_remaining = Distance(neighbor, destination)
               heapq.heappush(current_paths, (new_real_cost + estimated_remaining, new_path))


   return None

