public class Tester {
    harness public static void main() {
	GraphSearch g = new GraphSearch(5); 

	g.addEdge(0, 1); 
	g.addEdge(0, 2); 
	g.addEdge(1, 2); 
	g.addEdge(2, 0); 
	g.addEdge(2, 3); 
	g.addEdge(3, 3);
	g.addEdge(3, 4);

	testDFS(g);
	testBFS(g);
    }

    public static void testDFS(GraphSearch g) {
    	int[] bfs = g.DFS(2);

    	assert bfs[0] == 2;
    	assert bfs[1] == 3;
    	assert bfs[2] == 4;	
    	assert bfs[3] == 0;
    	assert bfs[4] == 1;
    }

    public static void testBFS(GraphSearch g) {
	int[] bfs = g.BFS(2);

	assert bfs[0] == 2;
	assert bfs[1] == 0;
	assert bfs[2] == 3;	
	assert bfs[3] == 1;
	assert bfs[4] == 4;
    }
}
