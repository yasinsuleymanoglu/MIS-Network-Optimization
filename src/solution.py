import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. VERI HAZIRLAMA (Data Preparation)
# ---------------------------------------------------------------------------
def load_data(filepath):
    print(f"Veri '{filepath}' konumundan yukleniyor...")
    df = pd.read_csv(filepath)
    return df

# ---------------------------------------------------------------------------
# 2. AG GRAFIGINI OLUSTURMA (Network Graph Creation)
# ---------------------------------------------------------------------------
def build_graph(df):
    G = nx.Graph()
    for index, row in df.iterrows():
        source = row['source']
        target = row['target']
        weight = row['latency_ms']
        G.add_edge(source, target, weight=weight)
    print(f"Ag grafigi olusturuldu: {G.number_of_nodes()} Dugum (Node), {G.number_of_edges()} Baglanti (Edge)")
    return G

# ---------------------------------------------------------------------------
# 3. EN KISA YOLU BULMA (Shortest Path Optimization)
# ---------------------------------------------------------------------------
def find_shortest_path(G, source_node, target_node):
    print(f"\nOptimizasyon: '{source_node}' ile '{target_node}' arasindaki en kisa yol hesaplaniyor...")
    try:
        shortest_path = nx.shortest_path(G, source=source_node, target=target_node, weight='weight')
        total_latency = nx.shortest_path_length(G, source=source_node, target=target_node, weight='weight')
        
        print("\n--- SONUCLAR ---")
        print(f"En Uygun Rota: {' -> '.join(shortest_path)}")
        print(f"Toplam Gecikme: {total_latency} ms")
        return shortest_path, total_latency
    except nx.NetworkXNoPath:
        print(f"HATA: {source_node} ve {target_node} arasinda bir baglanti bulunamadi!")
        return None, None

# ---------------------------------------------------------------------------
# 4. AG GORSELLESTIRME (Network Visualization)
# ---------------------------------------------------------------------------
def visualize_network(G, shortest_path):
    print("\nAg gorsellestiriliyor. (Lutfen acilan pencereyi kapatarak programi sonlandirin.)")
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42) 
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2500, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.5, alpha=0.6)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    
    if shortest_path:
        path_nodes = shortest_path
        nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_color='lightgreen', node_size=2500)
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3.5)

    plt.title("Cloud Data Center Network Optimization (Shortest Path / Min Latency)", fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('results/network_visualization.png') # Gorseli results klasorune kaydet
    plt.show()

# ---------------------------------------------------------------------------
# ANA PROGRAM AKISI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 1. Yeni Veri dosyasinin yolu
    data_file = 'data/network_data.csv'
    
    start_node = 'DC-NewYork'
    end_node = 'DC-Tokyo'
    
    network_df = load_data(data_file)
    network_graph = build_graph(network_df)
    optimal_path, latency = find_shortest_path(network_graph, start_node, end_node)
    
    visualize_network(network_graph, optimal_path)
    
    # Sonuclari txt dosyasina yazdirma
    with open('results/solution_output.txt', 'w') as f:
        f.write(f"Optimal Path: {' -> '.join(optimal_path)}\nTotal Latency: {latency} ms\n")
    
    print("\nProgram basariyla tamamlandi. Sonuclar 'results/' klasorune kaydedildi.")
