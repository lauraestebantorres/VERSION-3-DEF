import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from airSpace import AirSpace
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from math import sqrt
from collections import deque
from queue import PriorityQueue


class AirSpaceGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualizador de Espacio Aéreo")

        self.airspace = AirSpace()
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        self.toolbar.update()
        self.toolbar.grid(row=6, column=0, columnspan=3)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=3)

        self.canvas.draw()
        self.canvas.mpl_connect('button_press_event', self.on_click)

        ttk.Label(master, text="Zona de vuelo:").grid(row=0, column=0, padx=5, pady=5)
        self.dataset_selector = ttk.Combobox(master, values=["Catalunya", "España", "Europa"], state="readonly")
        self.dataset_selector.grid(row=0, column=1, padx=5, pady=5)
        self.dataset_selector.current(0)
        ttk.Button(master, text="Cargar espacio aéreo", command=self.load_selected_data).grid(row=0, column=2, padx=5,
                                                                                              pady=5)

        ttk.Label(master, text="Nombre del punto:").grid(row=1, column=0, sticky="e")
        self.point_entry = ttk.Entry(master)
        self.point_entry.grid(row=1, column=1, sticky="w")
        ttk.Button(master, text="Mostrar vecinos", command=self.plot_neighbors).grid(row=3, column=2, padx=5, pady=5)

        ttk.Label(master, text="Origen:").grid(row=3, column=0, sticky="e")
        self.origin_entry = ttk.Entry(master)
        self.origin_entry.grid(row=3, column=1, sticky="w")
        ttk.Label(master, text="Destino:").grid(row=4, column=0, sticky="e")
        self.dest_entry = ttk.Entry(master)
        self.dest_entry.grid(row=4, column=1, sticky="w")
        ttk.Button(master, text="Camino más corto", command=self.plot_shortest_path).grid(row=4, column=2, padx=5,
                                                                                          pady=5)



        ttk.Button(master, text="Zoom al punto", command=self.zoom_to_point).grid(row=5, column=2, padx=5, pady=5)
        ttk.Button(master, text="Puntos Alcanzables", command=self.show_reachable_points).grid(row=1, column=2, padx=5,
                                                                                               pady=5)

        self.info_label = ttk.Label(master, text="")
        self.info_label.grid(row=5, column=0, columnspan=2)

    def load_selected_data(self):
        zona = self.dataset_selector.get()
        nav_file = seg_file = aer_file = None
        if zona == "Catalunya":
            nav_file, seg_file, aer_file = "Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt"
        elif zona == "España":
            nav_file, seg_file, aer_file = "Esp_nav.txt", "Esp_seg.txt", "Esp_aer.txt"
        elif zona == "Europa":
            nav_file, seg_file, aer_file = "Eur_nav.txt", "Eur_seg.txt", "Eur_aer.txt"

        if not all(os.path.exists(f) for f in [nav_file, seg_file, aer_file]):
            messagebox.showerror("Error", f"No se han encontrado todos los archivos para {zona}.")
            return

        self.airspace.load_all(nav_file, seg_file, aer_file)
        self.plot_graph()
        self.info_label.config(text=f"Datos de {zona} cargados correctamente")

    def on_click(self, event):
        """Maneja el clic: selecciona punto, lo muestra, lo propone como origen/destino y aplica zoom automático."""
        if event.inaxes:
            clicked_lon = event.xdata
            clicked_lat = event.ydata
            closest = min(self.airspace.nav_points,
                          key=lambda p: self.euclidean_distance_coords(clicked_lat, clicked_lon, p.latitude,
                                                                       p.longitude))
            self.ax.plot(clicked_lon, clicked_lat, marker='x', color='purple', markersize=10)
            # Zoom automático al punto seleccionado
            delta = 0.1
            self.ax.set_xlim(closest.longitude - delta, closest.longitude + delta)
            self.ax.set_ylim(closest.latitude - delta, closest.latitude + delta)
            self.canvas.draw_idle()
            self.point_entry.delete(0, tk.END)
            self.point_entry.insert(0, closest.name)
            texto = (f"¿Usar '{closest.name}' como:\n"
                     f"Sí → Origen\n"
                     f"No → Destino\n"
                     f"Cancelar para ignorar.")
            respuesta = messagebox.askyesnocancel("Seleccionar punto", texto)
            if respuesta is True:
                self.origin_entry.delete(0, tk.END)
                self.origin_entry.insert(0, closest.name)
                self.info_label.config(text=f"Origen seleccionado: {closest.name}")
            elif respuesta is False:
                self.dest_entry.delete(0, tk.END)
                self.dest_entry.insert(0, closest.name)
                self.info_label.config(text=f"Destino seleccionado: {closest.name}")
            else:
                self.info_label.config(text="Selección cancelada")


    def show_reachable_points(self):
        point_name = self.point_entry.get().strip()
        point = self.airspace.get_point_by_name(point_name)

        if not point:
            self.info_label.config(text="Punto no encontrado.")
            return

        reached = set()
        queue = deque([point])

        while queue:
            current = queue.popleft()
            if current.number not in reached:
                reached.add(current.number)
                for segment in self.airspace.nav_segments:
                    # Verificar que el segmento es dirigido desde el nodo actual
                    if segment.origin_number == current.number:
                        neighbor = self.airspace.get_point_by_number(segment.destination_number)
                        if neighbor and neighbor.number not in reached:
                            queue.append(neighbor)

        self.plot_graph()  # Limpiar y redibujar
        for p in self.airspace.nav_points:
            if p.number in reached:
                self.ax.scatter(p.longitude, p.latitude, s=20, color='green')  # Puntos alcanzables en verde

        self.ax.scatter(point.longitude, point.latitude, s=40, color='blue')  # Origen en azul
        self.canvas.draw()

        # Mostrar ventana emergente con los nombres de los puntos alcanzables
        reachable_names = [p.name for p in self.airspace.nav_points if p.number in reached]
        messagebox.showinfo("Puntos Alcanzables", "\n".join(reachable_names))
        self.info_label.config(text=f"Puntos alcanzables desde {point.name}: {len(reached)}")


    def plot_graph(self):
        self.ax.clear()
        x = [p.longitude for p in self.airspace.nav_points]
        y = [p.latitude for p in self.airspace.nav_points]
        self.ax.scatter(x, y, s=5, color='grey', label='NavPoints')
        for s in self.airspace.nav_segments:
            p1 = self.airspace.get_point_by_number(s.origin_number)
            p2 = self.airspace.get_point_by_number(s.destination_number)
            if p1 and p2:
                self.ax.plot([p1.longitude, p2.longitude], [p1.latitude, p2.latitude], 'k-', linewidth=0.5)
        for p in self.airspace.nav_points:
            self.ax.text(p.longitude, p.latitude, p.name, fontsize=6, color='black', alpha=0.6)
        for airport in self.airspace.nav_airports:
            if airport.sids:
                sid = airport.sids[0]
                self.ax.scatter(sid.longitude, sid.latitude, s=50, color='red')
                self.ax.text(sid.longitude, sid.latitude, airport.name, fontsize=8, color='red')
        self.ax.set_title("Espacio Aéreo Catalunya con Nombres de Puntos")
        self.ax.set_xlabel("Longitud")
        self.ax.set_ylabel("Latitud")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()


    def zoom_to_point(self):
        name = self.point_entry.get().strip()
        point = self.airspace.get_point_by_name(name)
        if not point:
            self.info_label.config(text=f"Punto '{name}' no encontrado")
            return
        delta = 0.1  # Zoom factor
        self.ax.set_xlim(point.longitude - delta, point.longitude + delta)
        self.ax.set_ylim(point.latitude - delta, point.latitude + delta)
        self.ax.set_title(f"Zoom a {point.name}")
        self.canvas.draw_idle()
        self.info_label.config(text=f"Zoom centrado en {point.name}")


    def on_click(self, event):
        """Maneja el clic: selecciona punto, lo muestra, lo propone como origen/destino y aplica zoom automático."""
        if event.inaxes:
            clicked_lon = event.xdata
            clicked_lat = event.ydata
            closest = min(self.airspace.nav_points,
                          key=lambda p: self.euclidean_distance_coords(clicked_lat, clicked_lon, p.latitude, p.longitude))
            self.ax.plot(clicked_lon, clicked_lat, marker='x', color='purple', markersize=10)
            # Zoom automático al punto seleccion


    def load_cat_data(self):
        self.airspace.load_all("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
        self.info_label.config(
            text=f"Datos cargados: {len(self.airspace.nav_points)} puntos, {len(self.airspace.nav_segments)} segmentos, {len(self.airspace.nav_airports)} aeropuertos")
        self.plot_graph()


    def plot_graph(self):
        self.ax.clear()
        self.ax.set_title("Espacio Aéreo Catalunya - Puntos de Navegación y Segmentos")
        self.ax.set_xlabel("Longitud")
        self.ax.set_ylabel("Latitud")

        # Dibujar puntos de navegación
        for point in self.airspace.nav_points:
            self.ax.scatter(point.longitude, point.latitude, s=20, color='black')
            self.ax.text(point.longitude, point.latitude, point.name, fontsize=6, color='black')

        # Dibujar segmentos
        for segment in self.airspace.nav_segments:
            origin = self.airspace.get_point_by_number(segment.origin_number)
            destination = self.airspace.get_point_by_number(segment.destination_number)
            if origin and destination:
                self.ax.plot([origin.longitude, destination.longitude],
                             [origin.latitude, destination.latitude],
                             '#40E0D0', linewidth=0.5)

        # Dibujar aeropuertos
        for airport in self.airspace.nav_airports:
            if airport.sids:
                for sid in airport.sids:
                    self.ax.scatter(sid.longitude, sid.latitude, s=100, color='red')
                    self.ax.text(sid.longitude, sid.latitude, airport.name, fontsize=8, color='red')

        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.canvas.draw()


    def on_click(self, event):
        if event.inaxes:
            clicked_lon = event.xdata
            clicked_lat = event.ydata
            closest = min(self.airspace.nav_points,
                          key=lambda p: self.euclidean_distance_coords(clicked_lat, clicked_lon, p.latitude,
                                                                       p.longitude))
            self.ax.plot(clicked_lon, clicked_lat, marker='x', color='purple', markersize=10)
            self.canvas.draw_idle()
            self.point_entry.delete(0, tk.END)
            self.point_entry.insert(0, closest.name)
            texto = (f"¿Usar '{closest.name}' como:\n"
                     f"Sí → Origen\n"
                     f"No → Destino\n"
                     f"Cancelar para ignorar.")
            respuesta = messagebox.askyesnocancel("Seleccionar punto", texto)
            if respuesta is True:
                self.origin_entry.delete(0, tk.END)
                self.origin_entry.insert(0, closest.name)
                self.info_label.config(text=f"Origen seleccionado: {closest.name}")
            elif respuesta is False:
                self.dest_entry.delete(0, tk.END)
                self.dest_entry.insert(0, closest.name)
                self.info_label.config(text=f"Destino seleccionado: {closest.name}")
            else:
                self.info_label.config(text="Selección cancelada")


    def zoom_to_point(self):
        name = self.point_entry.get().strip()
        point = self.airspace.get_point_by_name(name)
        if not point:
            self.info_label.config(text=f"Punto '{name}' no encontrado")
            return
        delta = 0.1  # Zoom factor
        self.ax.set_xlim(point.longitude - delta, point.longitude + delta)
        self.ax.set_ylim(point.latitude - delta, point.latitude + delta)
        self.ax.set_title(f"Zoom a {point.name}")
        self.canvas.draw_idle()
        self.info_label.config(text=f"Zoom centrado en {point.name}")


    def plot_neighbors(self):
        name = self.point_entry.get().strip()
        point = self.airspace.get_point_by_name(name)
        if not point:
            self.info_label.config(text=f"No se ha encontrado el punto {name}")
            return
        self.plot_graph()
        for s in self.airspace.nav_segments:
            if s.origin_number == point.number:
                neighbor = self.airspace.get_point_by_number(s.destination_number)
                if neighbor:
                    self.ax.plot([point.longitude, neighbor.longitude], [point.latitude, neighbor.latitude], 'r-')
                    self.ax.scatter(neighbor.longitude, neighbor.latitude, color='green', s=20)
        self.ax.scatter(point.longitude, point.latitude, color='blue', s=40)
        self.canvas.draw()


    def plot_shortest_path(self):
        origin_name = self.origin_entry.get().strip()
        dest_name = self.dest_entry.get().strip()
        origin = self.airspace.get_point_by_name(origin_name)
        dest = self.airspace.get_point_by_name(dest_name)
        if not origin or not dest:
            self.info_label.config(text="Origen o destino no encontrado")
            return
        open_set = PriorityQueue()
        open_set.put((0, [origin]))
        visited = set()
        while not open_set.empty():
            _, path = open_set.get()
            current = path[-1]
            if current.number == dest.number:
                self.draw_path(path)
                return
            if current.number in visited:
                continue
            visited.add(current.number)
            for s in self.airspace.nav_segments:
                if s.origin_number == current.number:
                    neighbor = self.airspace.get_point_by_number(s.destination_number)
                    if neighbor and neighbor.number not in visited:
                        new_path = list(path)
                        new_path.append(neighbor)
                        cost = self.path_cost(new_path) + self.euclidean_distance(neighbor, dest)
                        open_set.put((cost, new_path))
        self.info_label.config(text="No se encontró camino")


    def draw_path(self, path):
        self.plot_graph()
        for i in range(len(path) - 1):
            p1, p2 = path[i], path[i + 1]
            self.ax.plot([p1.longitude, p2.longitude], [p1.latitude, p2.latitude], 'b-', linewidth=2)
        for p in path:
            self.ax.scatter(p.longitude, p.latitude, color='orange', s=30)
        self.canvas.draw()


    def path_cost(self, path):
        total = 0
        for i in range(len(path) - 1):
            for seg in self.airspace.nav_segments:
                if seg.origin_number == path[i].number and seg.destination_number == path[i + 1].number:
                    total += seg.distance
                    break
        return total


    def euclidean_distance(self, p1, p2):
        return sqrt((p1.latitude - p2.latitude) ** 2 + (p1.longitude - p2.longitude) ** 2)


    def euclidean_distance_coords(self, lat1, lon1, lat2, lon2):
        return sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


if __name__ == "__main__":
    root = tk.Tk()
    app = AirSpaceGUI(root)
    root.mainloop()
