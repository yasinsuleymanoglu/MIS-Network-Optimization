import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. VERI HAZIRLAMA (Data Preparation)
# ---------------------------------------------------------------------------
# Ag verimizi tutan CSV dosyasini okuyoruz.
# Bu dosya, agdaki dugumleri (sunucular/yonlendiriciler) ve 
# aralarindaki baglantilarin gecikme surelerini (milisaniye cinsinden) icerir.
def load_data(filepath):
    """
    CSV dosyasindan ag verilerini yukler.
    pandas kutuphanesi kullanarak veriyi bir DataFrame'e donustururuz.
    """
    print(f"Veri '{filepath}' konumundan yukleniyor...")
    df = pd.read_csv(filepath)
    return df

# ---------------------------------------------------------------------------
# 2. AG GRAFIGINI OLUSTURMA (Network Graph Creation)
# ---------------------------------------------------------------------------
# NetworkX kutuphanesini kullanarak dugumleri (nodes) ve kenarlari (edges) 
# modelleyen bir graf (graph) yapisi olusturuyoruz.
def build_graph(df):
    """
    Veri cercevesini (DataFrame) kullanarak bir NetworkX grafigi olusturur.
    Her satir bir kenari (baglantiyi) temsil eder.
    Agirlik (weight) olarak gecikme suresini (latency_ms) kullaniyoruz.
    """
    # Yonlendirilmemis bir graf (Undirected Graph) olusturuyoruz. 
    # Veri akisinin iki yonde de ayni gecikmeye sahip oldugunu varsayiyoruz.
    G = nx.Graph()
    
    # DataFrame icindeki her bir satir uzerinde donuyoruz
    for index, row in df.iterrows():
        source = row['source']
        target = row['target']
        weight = row['latency_ms']
        
        # Grafa kenari ve agirligini ekliyoruz
        G.add_edge(source, target, weight=weight)
        
    print(f"Ag grafigi olusturuldu: {G.number_of_nodes()} Dugum (Node), {G.number_of_edges()} Baglanti (Edge)")
    return G

# ---------------------------------------------------------------------------
# 3. EN KISA YOLU BULMA (Shortest Path Optimization)
# ---------------------------------------------------------------------------
# Dijkstra algoritmasini kullanarak iki nokta arasindaki en dusuk 
# gecikmeli (en kisa) yolu hesapliyoruz.
def find_shortest_path(G, source_node, target_node):
    """
    Dijkstra Algoritmasi kullanarak en kisa yolu (en dusuk gecikmeli rota) bulur.
    """
    print(f"\nOptimizasyon: '{source_node}' ile '{target_node}' arasindaki en kisa yol hesaplaniyor...")
    
    try:
        # nx.shortest_path fonksiyonu, 'weight' parametresini dikkate alarak 
        # en dusuk toplam agirliga sahip rotayi bulur.
        shortest_path = nx.shortest_path(G, source=source_node, target=target_node, weight='weight')
        
        # Bulunan yolun toplam gecikme suresini hesapliyoruz
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
# Orijinal agi ve buldugumuz en kisa yolu gorsellestiriyoruz.
def visualize_network(G, shortest_path):
    """
    Agi ve hesaplanan en kisa yolu ekranda cizer.
    En kisa yol uzerindeki dugumler ve kenarlar vurgulanir (farkli renk/kalinlik).
    """
    print("\nAg gorsellestiriliyor. (Lutfen acilan pencereyi kapatarak programi sonlandirin.)")
    
    # Cizim alaninin boyutunu belirliyoruz
    plt.figure(figsize=(12, 8))
    
    # Dugumlerin konumlarini (layout) yayli bir sistemle belirliyoruz 
    # (gorsel olarak daha estetik durmasi icin)
    pos = nx.spring_layout(G, seed=42) # seed=42 her seferinde ayni dizilimi verir
    
    # 1. Tum Dugumleri ve Kenarlari Ciz
    # Dugumleri (acik mavi)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2500, alpha=0.9)
    
    # Dugum etiketlerini (isimlerini) ekle
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')
    
    # Kenarlari (gri ve ince) ciz
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.5, alpha=0.6)
    
    # Kenar etiketlerini (gecikme surelerini) ekle
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    
    # 2. En Kisa Yolu Vurgula
    if shortest_path:
        # En kisa yoldaki dugumleri belirle ve renklendir (yesil)
        path_nodes = shortest_path
        nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_color='lightgreen', node_size=2500)
        
        # En kisa yoldaki kenarlari (baglantilari) belirle
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        # Bu kenarlari vurgula (kirmizi ve kalin)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3.5)

    # Baslik ekle ve ekrani goster
    plt.title("Cloud Data Center Network Optimization (Shortest Path / Min Latency)", fontsize=14, fontweight='bold')
    plt.axis('off') # Eksenleri gizle
    plt.tight_layout()
    plt.savefig('network_visualization.png') # Gorseli ayrica kaydet
    plt.show()

# ---------------------------------------------------------------------------
# ANA PROGRAM AKISI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 1. Veri dosyasinin yolu
    data_file = 'data.csv'
    
    # 2. Kaynak (baslangic) ve Hedef (bitis) dugumleri
    start_node = 'DC-NewYork'
    end_node = 'DC-Tokyo'
    
    # Programi calistiran adimlar
    network_df = load_data(data_file)
    network_graph = build_graph(network_df)
    optimal_path, latency = find_shortest_path(network_graph, start_node, end_node)
    
    # Gorsellestirmeyi calistir
    visualize_network(network_graph, optimal_path)
    
    print("\nProgram basariyla tamamlandi. Gorsel 'network_visualization.png' olarak kaydedildi.")
