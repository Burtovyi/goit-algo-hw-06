import networkx as nx
import matplotlib.pyplot as plt

# Створення графа
G = nx.Graph()

# Додавання станцій метро (вузлів)
stations = [
    'Central', 'North', 'South', 'East', 'West', 
    'North-East', 'South-East', 'South-West', 'North-West', 'Airport'
]

G.add_nodes_from(stations)

# Додавання ліній метро (ребер) з вагами
connections = [
    ('Central', 'North', 5), ('Central', 'South', 7), ('Central', 'East', 3), ('Central', 'West', 4),
    ('North', 'North-East', 4), ('East', 'North-East', 6),
    ('South', 'South-East', 5), ('East', 'South-East', 8),
    ('South', 'South-West', 6), ('West', 'South-West', 7),
    ('North', 'North-West', 5), ('West', 'North-West', 6),
    ('Airport', 'North-East', 10), ('Airport', 'South-East', 9)
]

G.add_weighted_edges_from(connections)

# Візуалізація графа
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, seed=42)  # Автоматичне розташування вузлів
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=12, font_weight='bold', edge_color='gray')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title('Транспортна мережа міста з вагами')
plt.show()

# Аналіз характеристик
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
degree_centrality = dict(G.degree())

print(f'Кількість станцій (вузлів): {num_nodes}')
print(f'Кількість ліній (ребер): {num_edges}')
print("Ступінь вершин (кількість з'єднань для кожної станції):")
for station, degree in degree_centrality.items():
    print(f'{station}: {degree}')

# Знаходження шляхів за допомогою DFS і BFS
start_station = 'Central'
end_station = 'Airport'

# DFS
dfs_path = list(nx.dfs_edges(G, source=start_station))
try:
    dfs_shortest_path = nx.dfs_tree(G, source=start_station).predecessors(end_station)
    dfs_shortest_path = list(dfs_shortest_path)
    dfs_shortest_path.reverse()
    dfs_shortest_path.append(end_station)
except nx.NetworkXError:
    dfs_shortest_path = "Шлях не знайдено"

# BFS
try:
    bfs_shortest_path = nx.shortest_path(G, source=start_station, target=end_station)
except nx.NetworkXNoPath:
    bfs_shortest_path = "Шлях не знайдено"

print(f"\nDFS шлях від {start_station} до {end_station}: {dfs_shortest_path}")
print(f"BFS найкоротший шлях від {start_station} до {end_station}: {bfs_shortest_path}")

# Порівняння результатів
print("\nПорівняння алгоритмів:")
if dfs_shortest_path != bfs_shortest_path:
    print("DFS і BFS дали різні результати через різну стратегію обходу.")
else:
    print("DFS і BFS знайшли однаковий шлях.")

# Знаходження найкоротшого шляху за алгоритмом Дейкстри
dijkstra_paths = dict(nx.all_pairs_dijkstra_path(G))
dijkstra_lengths = dict(nx.all_pairs_dijkstra_path_length(G))

print("\nНайкоротші шляхи між усіма вершинами за алгоритмом Дейкстри:")
for start in stations:
    for end in stations:
        if start != end:
            print(f"{start} -> {end}: Шлях: {dijkstra_paths[start][end]}, Довжина: {dijkstra_lengths[start][end]}")