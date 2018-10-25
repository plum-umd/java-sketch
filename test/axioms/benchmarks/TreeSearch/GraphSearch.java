// Java program to print BFS traversal from a given source vertex. 
// BFS(int s) traverses vertices reachable from s. 
import java.io.*; 
import java.util.*; 

// This class represents a directed graph using adjacency list 
// representation 
class GraphSearch 
{ 
	private int V; // No. of vertices 
	private TwoDArray adj; //Adjacency Lists 

	// Constructor 
        public GraphSearch(int v) 
	{ 
	    V = v; 
	    adj = new TwoDArray(v, v);
	} 

	// Function to add an edge into the graph 
	void addEdge(int v,int w) 
	{
	    adj.set(v,w,1);
	} 

	int[] newSearch() {
	    int[] bfs = new int[V];
	    for(int i = 0; i < V; i++) {
		bfs[i] = -1;
	    }
	    return bfs;
	}

	// prints BFS traversal from a given source s 
	int[] BFS(int s) { 
	    // Mark all the vertices as not visited(By default 
	    // set as false) 
	    boolean[] visited = new boolean[V]; 
	    int[] bfs = newSearch();
	    int seen = 0;
	    
	    // Create a queue for BFS 
	    LinkedList<Integer> queue = new LinkedList<Integer>(); 
	    
	    // Mark the current node as visited and enqueue it 
	    visited[s]=true; 
	    queue.add(new Integer(s)); 
	    
	    while (queue.size() != 0) { 
	    	// Dequeue a vertex from queue and print it
	    	Integer s_box = queue.poll();
	    	s = s_box.intValue();
	    	bfs[seen] = s;
	    	seen++;
		
	    	// System.out.print(s+" "); 
		
	    	// Get all adjacent vertices of the dequeued vertex s 
	    	// If a adjacent has not been visited, then mark it 
	    	// visited and enqueue it
	    	int[] adjs = adj.getRow(s);
	    	for (int i=0; i<adjs.length; i++) {
	    	    int n = adjs[i];
	    	    if (!visited[i] && n == 1) {
	    		visited[i] = true;
	    		queue.add(new Integer(i));
	    	    }
	    	}
	    }
	    return bfs;
	}

    
	// prints DFS traversal from a given source s 
	int[] DFS(int s) 
	{	       
		// Mark all the vertices as not visited(By default 
		// set as false) 
		boolean[] visited = new boolean[V]; 
		int[] bfs = newSearch();
		int seen = 0;
		
		// Create a queue for BFS 
		Stack<Integer> stack = new Stack<Integer>(); 

		// Mark the current node as visited and enqueue it 
		stack.push(new Integer(s)); 

		while (!stack.empty()) 
		{ 
			// Dequeue a vertex from queue and print it 
			Integer s_box = stack.pop();
			s = s_box.intValue();

			if (!visited[s]) {
			    visited[s] = true;
			    bfs[seen] = s;
			    seen++;
			}

			// Get all adjacent vertices of the dequeued vertex s 
			// If a adjacent has not been visited, then mark it 
			// visited and enqueue it
			int[] adjs = adj.getRow(s);
			for (int i=0; i<adjs.length; i++) {
			    int n = adjs[i];
			    if (!visited[i] && n == 1) {
				stack.push(new Integer(i));
			    }
			}
			// // Get all adjacent vertices of the dequeued vertex s 
			// // If a adjacent has not been visited, then mark it 
			// // visited and enqueue it 
			// Iterator<Integer> i = adj[s].listIterator(); 
			// while (i.hasNext()) 
			// { 
			// 	int n = i.next(); 
			// 	if (!visited[n]) 
			// 	{ 
			// 		stack.push(n); 
			// 	} 
			// } 
		}
		return bfs;
	} 

	// // Driver method to 
	// public static void main(String args[]) 
	// { 
	//         GraphSearch g = new GraphSearch(4); 

	// 	g.addEdge(0, 1); 
	// 	g.addEdge(0, 2); 
	// 	g.addEdge(1, 2); 
	// 	g.addEdge(2, 0); 
	// 	g.addEdge(2, 3); 
	// 	g.addEdge(3, 3); 

	// 	int[] bfs = g.BFS(2);
	// 	for(int i = 0; i < bfs.length; i++) {
	// 	    int node = bfs[i];
	// 	    if (node >= 0) {
	// 		System.out.println(node);
	// 	    }
	// 	}
	// } 
} 
// This code is contributed by Aakash Hasija 
