import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from graph import Graph, AddNode, AddSegment, Plot, PlotNode, GetClosest, LoadGraphFromFile, FindShortestPath, reachable_nodes
from node import Node, Distance
from path import Path, PlotPath
from airSpace import AirSpace

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Airspace Graph Tool")
        self.graph = Graph()
        self.airspace = None
        self.selected_airspace = tk.StringVar(value="None")

        # GUI elements
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(side=tk.LEFT)

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Airspace selection
        tk.Label(self.control_frame, text="Select Airspace:").pack()
        airspaces = ["None", "Catalunya"]  # Removed España and Europe
        self.airspace_menu = ttk.Combobox(self.control_frame, textvariable=self.selected_airspace, values=airspaces)
        self.airspace_menu.pack()
        self.airspace_menu.bind("<<ComboboxSelected>>", self.load_airspace)

        # Graph operations
        tk.Button(self.control_frame, text="Load Graph from File", command=self.load_graph).pack()
        tk.Button(self.control_frame, text="Show Example Graph", command=self.show_example_graph).pack()
        tk.Button(self.control_frame, text="Show Custom Graph", command=self.show_custom_graph).pack()

        # Node selection
        tk.Label(self.control_frame, text="Select Node:").pack()
        self.node_entry = tk.Entry(self.control_frame)
        self.node_entry.pack()
        tk.Button(self.control_frame, text="Show Neighbors", command=self.show_neighbors).pack()
        tk.Button(self.control_frame, text="Show Reachability", command=self.show_reachability).pack()

        # Shortest path
        tk.Label(self.control_frame, text="Shortest Path:").pack()
        tk.Label(self.control_frame, text="From Node:").pack()
        self.from_entry = tk.Entry(self.control_frame)
        self.from_entry.pack()
        tk.Label(self.control_frame, text="To Node:").pack()
        self.to_entry = tk.Entry(self.control_frame)
        self.to_entry.pack()
        tk.Button(self.control_frame, text="Show Shortest Path", command=self.show_shortest_path).pack()

        # Graph editing
        tk.Button(self.control_frame, text="Add Node", command=self.add_node).pack()
        tk.Button(self.control_frame, text="Add Segment", command=self.add_segment).pack()
        tk.Button(self.control_frame, text="Delete Node", command=self.delete_node).pack()
        tk.Button(self.control_frame, text="Create New Graph", command=self.create_new_graph).pack()
        tk.Button(self.control_frame, text="Save Graph", command=self.save_graph).pack()

    def load_airspace(self, event=None):
        airspace_name = self.selected_airspace.get()
        if airspace_name == "None":
            self.airspace = None
            self.graph = Graph()
            return
        self.airspace = AirSpace()
        success = False
        if airspace_name == "Catalunya":
            success = self.airspace.load_from_files("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
        if success:
            self.graph = self.airspace.graph
            print(f"Graph nodes: {[n.name for n in self.graph.nodes]}")
            print(f"Graph segments: {[s.id for s in self.graph.segments]}")
            Plot(self.graph)
        else:
            messagebox.showerror("Error", f"Failed to load {airspace_name} airspace data. Check console for details.")

    def load_graph(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.graph = LoadGraphFromFile(file_path)
            Plot(self.graph)

    def show_example_graph(self):
        from test_graph import CreateGraph_1
        self.graph = CreateGraph_1()
        Plot(self.graph)

    def show_custom_graph(self):
        from test_graph import CreateGraph_2
        self.graph = CreateGraph_2()
        Plot(self.graph)

    def show_neighbors(self):
        node_name = self.node_entry.get()
        if not node_name:
            messagebox.showerror("Error", "Please enter a node name.")
            return
        if not any(n.name == node_name for n in self.graph.nodes):
            messagebox.showerror("Error", "Invalid node name.")
            return
        PlotNode(self.graph, node_name)

    def show_reachability(self):
        node_name = self.node_entry.get()
        if not node_name:
            messagebox.showerror("Error", "Please enter a node name.")
            return
        if not any(n.name == node_name for n in self.graph.nodes):
            messagebox.showerror("Error", "Invalid node name.")
            return
        reachable = reachable_nodes(self.graph, node_name)
        print(f"Reachable from {node_name}: {[n.name for n in reachable]}")
        plt.clf()
        for segment in self.graph.segments:
            x = [segment.origin.x, segment.destination.x]
            y = [segment.origin.y, segment.destination.y]
            plt.plot(x, y, 'k-')
        for node in self.graph.nodes:
            color = 'ro' if any(n.name == node.name for n in reachable) else 'ko'
            plt.plot(node.x, node.y, color)
            plt.text(node.x, node.y, node.name)
        plt.title(f"Reachability from {node_name}")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.show()

    def show_shortest_path(self):
        from_node = self.from_entry.get()
        to_node = self.to_entry.get()
        if not from_node or not to_node:
            messagebox.showerror("Error", "Please enter both source and destination nodes.")
            return
        if not any(n.name == from_node for n in self.graph.nodes) or not any(n.name == to_node for n in self.graph.nodes):
            messagebox.showerror("Error", "Invalid node names.")
            return
        path = FindShortestPath(self.graph, from_node, to_node)
        if path:
            PlotPath(self.graph, path)
            print(f"Shortest path: {[n.name for n in path.nodes]}")
            print(f"Total cost: {path.TotalCost():.2f}")
        else:
            messagebox.showinfo("Info", "No path found.")

    def add_node(self):
        name = tk.simpledialog.askstring("Input", "Node name:")
        x = tk.simpledialog.askfloat("Input", "X coordinate:")
        y = tk.simpledialog.askfloat("Input", "Y coordinate:")
        if name and x is not None and y is not None:
            node = Node(name, x, y)
            AddNode(self.graph, node)
            Plot(self.graph)

    def add_segment(self):
        origin = tk.simpledialog.askstring("Input", "Origin node:")
        destination = tk.simpledialog.askstring("Input", "Destination node:")
        if origin and destination:
            AddSegment(self.graph, f"{origin}{destination}", origin, destination)
            Plot(self.graph)

    def delete_node(self):
        name = tk.simpledialog.askstring("Input", "Node to delete:")
        if name:
            new_nodes = [n for n in self.graph.nodes if n.name != name]
            new_segments = [s for s in self.graph.segments if s.origin.name != name and s.destination.name != name]
            self.graph.nodes = new_nodes
            self.graph.segments = new_segments
            Plot(self.graph)

    def create_new_graph(self):
        self.graph = Graph()
        Plot(self.graph)

    def save_graph(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                for node in self.graph.nodes:
                    f.write(f"{node.name},{node.x},{node.y}\n")
                for segment in self.graph.segments:
                    f.write(f"{segment.id},{segment.origin.name},{segment.destination.name}\n")
            print(f"Graph saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()