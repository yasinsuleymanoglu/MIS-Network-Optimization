# Cloud Data Center Network Optimization (Shortest Path Problem)

This project solves a real-world Management Information Systems (MIS) network optimization problem using Python and NetworkX. It demonstrates the **Shortest Route / Shortest Path Problem** applied to a cloud computing infrastructure, satisfying all the requirements for the final assignment.

## 1. Problem Context (MIS-Related)

In modern cloud computing, telecommunications, and internet service provider networks, minimizing data transfer latency is critical for user experience and system efficiency. 

**The Scenario:** A global cloud service provider needs to transfer a large, time-sensitive dataset from their primary data center in New York (`DC-NewYork`) to a newly established regional data center in Tokyo (`DC-Tokyo`). The data must pass through various international routers and network switches. 

**The Goal:** Find the optimal network path that minimizes the total transmission latency (measured in milliseconds).

## 2. Network Representation & Dataset

The network is represented as an undirected graph where:
*   **Nodes (7):** Represent data centers, network switches, and international routers (e.g., `DC-NewYork`, `Rtr-London`, `Sw-Amsterdam`). This satisfies the minimum requirement of 6 nodes.
*   **Edges (10):** Represent the physical or virtual network links connecting these nodes. This satisfies the minimum requirement of 8 edges.
*   **Edge Weights:** Represent the **latency in milliseconds (ms)** for data to travel across that specific link.

The dataset is clearly defined in a separate `data.csv` file with the following columns:
*   `source`: The starting node of the link.
*   `target`: The ending node of the link.
*   `latency_ms`: The latency cost of the link in milliseconds (numerical edge attribute).

*Assumption: The network links are bidirectional and have symmetric latency.*

## 3. Python Solution & Tools Used

The solution is implemented in `main.py` using Python and the required **NetworkX** library.

### Code Explanation:
The script is modular and fully commented. Here is how it works:
1.  **`load_data()`**: Uses `pandas` to read the `data.csv` file. 
2.  **`build_graph()`**: Iterates through the loaded data and uses `nx.Graph().add_edge()` to create a NetworkX graph structure. Nodes represent the networking hardware, edges represent the connections, and the `weight` attribute is assigned the latency value.
3.  **`find_shortest_path()`**: Uses `nx.shortest_path()` which runs **Dijkstra's Algorithm** under the hood. It calculates the route with the lowest total accumulated weight (latency) between the source and target nodes.
4.  **`visualize_network()`**: Uses `matplotlib` and `nx.draw()` to map out the network visually. It renders nodes in blue, edges in grey, and specifically highlights the mathematically proven shortest path by changing its nodes to green and edges to thick red.

## 4. Managerial Interpretation of Results

By running the optimization algorithm, the program determines the path with the absolute minimum latency. 

*   **Calculated Optimal Route:** DC-NewYork -> Rtr-London -> Sw-Amsterdam -> Rtr-Frankfurt -> DC-Tokyo
*   **Calculated Total Minimum Latency:** 228 ms

**Managerial Insights:**
*   **Cost & Performance Efficiency:** Instead of routing data directly through high-latency connections (if they existed) or choosing sub-optimal switches, the algorithm mathematically guarantees the fastest delivery route. For a cloud provider or ISP, this directly translates to fulfilling Service Level Agreements (SLAs) for enterprise customers.
*   **Bottleneck Identification:** Visualizing the network reveals critical junctions like `Rtr-London` or `Rtr-Frankfurt`. If these specific nodes experience downtime or heavy traffic, the latency to Tokyo would increase significantly. Management can use this insight to prioritize infrastructure investments, such as adding redundant parallel links to these high-value nodes to improve overall network resilience.
*   **Strategic Infrastructure Planning:** When executives plan to construct a new data center, they can use this optimization model to simulate connecting it to different existing switches. They can then calculate which new connection provides the best overall network speed improvement relative to the cost of laying new physical fiber cables.

## 5. How to Run the Project

1. Ensure Python 3.x is installed on your system.
2. Clone this repository to your local machine.
3. Install the required Python libraries using pip:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Python script:
   ```bash
   python main.py
   ```
5. The console will print the calculated path and total latency. A window will open showing the visual representation of the network with the shortest path clearly highlighted in red. The image will also be saved automatically as `network_visualization.png`.
