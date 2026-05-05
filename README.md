# Cloud Data Center Network Optimization

## 1. Real-World Problem Context
In modern cloud computing, telecommunications, and internet service provider networks, minimizing data transfer latency is critical for user experience and system efficiency. A global cloud service provider needs to transfer a large, time-sensitive dataset across international borders.

## 2. Problem Definition
The primary data center is located in New York (`DC-NewYork`), and a newly established regional data center is in Tokyo (`DC-Tokyo`). The data must pass through various international routers and network switches. The goal is to find the optimal network path that minimizes the total transmission latency (measured in milliseconds) between these two points.

## 3. Network Model
The network is modeled as an undirected graph where data transfer is bidirectional and latency is symmetric. The Shortest Path Problem optimization model is applied to find the path with the minimum total weight (latency).

## 4. Nodes and Edges
* **Nodes (7):** Represent data centers, network switches, and international routers (e.g., `DC-NewYork`, `Rtr-London`, `Sw-Amsterdam`). 
* **Edges (11):** Represent the physical or virtual network links connecting these nodes.
* **Edge Weights:** Represent the latency in milliseconds (ms) for data to travel across a specific link.

The data is stored in `data/network_data.csv` with columns: `source`, `target`, and `latency_ms`.

## 5. Selected Algorithm
The solution utilizes **Dijkstra's Algorithm** to solve the Shortest Route / Shortest Path Problem. It calculates the route with the lowest total accumulated weight (latency) between the source and target nodes.

## 6. Python Implementation
The solution is implemented in `src/solution.py` using Python and the `NetworkX` library.
* `pandas` is used to load the dataset.
* `nx.Graph()` is used to build the network.
* `nx.shortest_path()` computes Dijkstra's algorithm.
* `matplotlib` and `nx.draw()` are used to map out the network visually, highlighting the shortest path.

## 7. Results
* **Calculated Optimal Route:** DC-NewYork -> Rtr-London -> Rtr-Frankfurt -> DC-Tokyo
* **Calculated Total Minimum Latency:** 225 ms
*(See the `results/network_visualization.png` for the visual output).*

## 8. Managerial Interpretation
By determining the path with the absolute minimum latency, several insights are gained:
* **Cost & Performance Efficiency:** The algorithm mathematically guarantees the fastest delivery route. For a cloud provider, this translates to fulfilling Service Level Agreements (SLAs) for enterprise customers without routing through sub-optimal connections.
* **Bottleneck Identification:** Visualizing the network reveals critical junctions like `Rtr-London` or `Rtr-Frankfurt`. If these nodes experience downtime, latency to Tokyo increases significantly. Management can prioritize adding redundant links to these high-value nodes.
* **Strategic Planning:** When planning to construct a new data center, executives can simulate connecting it to different switches to calculate which new connection provides the best network speed improvement relative to cost.

## 9. How to Run the Code
1. Clone this repository.
2. Install the requirements: `pip install -r requirements.txt`
3. Run the script: `python src/solution.py`
4. Results will be saved in the `results/` folder.

## 10. References
* NetworkX Documentation: https://networkx.org/documentation/stable/
* Python Pandas Documentation: https://pandas.pydata.org/docs/
