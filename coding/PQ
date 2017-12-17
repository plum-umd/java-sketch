

/**
 * A min priority queue implementation using a binary heap.
 * @author William Fiset, william.alexandre.fiset@gmail.com
 * @author Siyuan Xu, code adapted or modified from existing repo for sketch synthesis use
 **/

import java.util.*;

import org.junit.*;

//class PQueue <T extends Comparable<T>> {
class PQueue {

 // The number of elements currently inside the heap
  private int heapSize = 0;

  // The internal capacity of the heap
  private int heapCapacity = 0;

  // A dynamic list to track the elements inside the heap
  private List <Integer> heap = null;

  // This map keeps track of the possible indices a particular 
  // node value is found in the heap. Having this mapping lets
  // us have O(log(n)) removals and O(1) element containment check
  // at the cost of some additional space and minor overhead
  private Map <Integer, TreeSet<Integer>> map = new HashMap<>();

  // Construct and initially empty priority queue
  public PQueue() {
    this(1);
  }

  // Construct a priority queue with an initial capacity
  public PQueue(int sz) {
    heap = new ArrayList<>(sz);
    // instance variables not working??? Gotta be careful
    map = new HashMap<>();
    heapSize = 0;
    heapCapacity = 0;
  }
  
  
  // Return the size of the heap
  public int size() {
    return heapSize;
  }

  // Returns true/false depending on if the priority queue is empty
  public boolean isEmpty() {
    return heapSize == 0;
  }

 // omit two constructors


 // Add a node value and its index to the map
  private void mapAdd(Integer value, int index) {
    
    Integer indexTmp = new Integer(index);
    TreeSet <Integer> set = map.get(value);

    // New value being inserted in map
    if (set == null) {

      set = new TreeSet<>();
      set.add(indexTmp);
      map.put(value, set);

    // Value already exists in map
    } else set.add(indexTmp);

  }
  


   // Removes the index at a given value, O(log(n))
  private void mapRemove(Integer value, int index) {
    Integer indexTmp = new Integer(index);
    TreeSet <Integer> set = map.get(value);
    set.remove(indexTmp); // TreeSets take O(log(n)) removal time
    if (set.size() == 0) map.remove(value);
  }

  // Extract an index position for the given value
  // NOTE: If a value exists multiple times in the heap the highest 
  // index is returned (this has arbitrarily been chosen)
  private Integer mapGet(Integer value) {
    TreeSet <Integer> set = map.get(value);
    if (set != null) return set.last();
    return null;
  }


  // Removes a particular element in the heap, O(log(n))



  // Removes a particular element in the heap, O(log(n))
  public boolean remove(Integer element) {
    
    if (element == null) return false;
    
    // Linear removal via search, O(n)
    // for (int i = 0; i < heapSize; i++) {
    //   if (element.equals(heap.get(i))) {
    //     removeAt(i);
    //     return true;
    //   }
    // }

    // Logarithmic removal with map, O(log(n))
    Integer index = mapGet(element);
    int indexTmp = index.intValue();
    if (index != null) 
       removeAt(indexTmp);
    return index != null;

  }

// Tests if the value of node i <= node j
  // This method assumes i & j are valid indices, O(1)
   private boolean less(int i, int j) {

    Integer node1 = heap.get(i);
    Integer node2 = heap.get(j);
    return node1.compareTo(node2) <= 0;
    
  }

// intop down node sink, O(log(n))
   private void sink(int k) {

    while ( true ) {
      
      int left  = 2 * k + 1; // Left  node
      int right = 2 * k + 2; // Right node
      int smallest = left;   // Assume left is the smallest node of the two children

      // Find which is smaller left or right
      // If right is smaller set smallest to be right
      if ( right < heapSize && less(right, left) )
        smallest = right;

      // Stop if we're outside the bounds of the tree
      // or stop early if we cannot sink k anymore
      if ( left >= heapSize || less(k, smallest)) return;
      
      // Move down the tree following the smallest node
      swap(smallest, k);
      k = smallest;

    }

  }

// Exchange the index of two nodes internally within the map
  private void mapSwap(Integer val1, Integer val2, int val1Index, int val2Index) {

    
    Set <Integer> set1 = map.get(val1);
    Set <Integer> set2 = map.get(val2);

    Integer val1IndexTmp =  new Integer(val1Index);
    Integer val2IndexTmp = new Integer(val2Index);
    set1.remove(val1IndexTmp);
    set2.remove(val2IndexTmp);

    set1.add(val2IndexTmp);
    set2.add(val1IndexTmp);


  }

 


 // Swap two nodes. Assumes i & j are valid, O(1)
 private void swap(int i, int j) {
    
    Integer i_elem = heap.get(i);
    Integer j_elem = heap.get(j);

    heap.set(i, j_elem);
    heap.set(j, i_elem);

    mapSwap(i_elem, j_elem, i, j);

  }

  // Perform bottom up node swim, O(log(n))
   private void swim(int k) {
    
    // Grab the index of the next parent node WRT to k
    int parent = (k-1) / 2;

    // Keep swimming while we have not reached the
    // root and while we're less than our parent.
    while (k > 0 && less(k, parent)) {

      // Exchange k with the parent
      swap( parent, k);
      k = parent;

      // Grab the index of the next parent node WRT to k
      parent = (k-1) / 2;

    }

  }


  // Removes a node at particular index, O(log(n))
  private Integer removeAt(int i) {
    
    if (isEmpty()) return null;

    heapSize--;
    Integer removed_data = heap.get(i);
    swap(i, heapSize);
	

    // Obliterate the value
    heap.set(heapSize, null);
    mapRemove(removed_data, heapSize);

    // Removed last element
    if (i == heapSize) return removed_data;

    Integer elem = heap.get(i);

    // intry sinking element
    sink(i);
	

	/*	The newer synthesized version Verified Works! 2017-11-31
	generator example
	boolean b = k.equals(key);

            if ({|b, k == key|}) {
    */
    // If sinking did not work try swimming
	Integer res = heap.get(i);
	boolean b = res.equals(elem);
	if ({|b,res == elem|})
		swim(i);
    
	// original code!!!!!! 
	/*
	if ( heap.get(i).equals(elem) )
      swim(i);
	*/

    return removed_data;

  }


 






  // Clears everything inside the heap, O(n)
  public void clear() {
	//for (int i = 0; i < heapCapacity; i++)
    for (int i = ??; i < heapCapacity; i++)
      heap.set(i, null);
    heapSize = 0;
    map.clear();
  }
    

 

 // Returns the value of the element with the lowest
  // priority in this priority queue. If the priority 
  // queue is empty null is returned.
  public Integer peek() {
    if (isEmpty()) return null;
    return heap.get(0);
  }

  // Removes the root of the heap, O(log(n))
  public Integer poll() {
    return removeAt(0);
  }



 public boolean contains(Integer elem) {

    // Map lookup to check containment, O(1)
    if (elem == null) return false;
    return map.containsKey(elem);

   

  }


  // Adds an element to the priority queue, the 
  // element must not be null, O(log(n))
  public void add(Integer elem) {
    
    if (elem == null) return; //throw new IllegalArgumentException();

    if (heapSize < heapCapacity) {
      heap.set(heapSize, elem);
    } else {
      heap.add(elem);
      heapCapacity++;
    }

    mapAdd(elem, heapSize);

    swim(heapSize); 
    heapSize++;

  }


  // Recursively checks if this heap is a min heap
  // This method is just for testing purposes to make
  // sure the heap invariant is still being maintained
  // Called this method with k=0 to start at the root
 
    public boolean isMinHeap(int k) {

    // If we are outside the bounds of the heap return true 
    if (k >= heapSize) return true;

    int left  = 2 * k + 1;
    int right = 2 * k + 2;

    // Make sure that the current node k is less than
    // both of its children left, and right if they exist
    // return false otherwise to indicate an invalid heap
    if (left  < heapSize  && !less(k, left))  return false;
    if (right < heapSize  && !less(k, right)) return false;

    // Recurse on both children to make sure they're also valid heaps
    return isMinHeap(left) && isMinHeap(right);

  }  
 


 // Something wrong with this part
 // @Override public String toString() {
 //   return heap.toString();

 // }
  

  harness static void m()
  {
    static final int LOOPS = 1000;

    static final int MAX_SZ = 100;

    testEmpty();
	testHeapProperty();
	testClear();
	testContainment();
	testRemovingDuplicates();


  }

    @Test
    public void testEmpty() {
    	PQueue<Integer> q = new PQueue<>();
    	Assert.assertEquals (q.size(), 0);
    	assert (q.isEmpty());
    	assert q.poll() == null;
    	assert q.peek() == null;
    }

	@Test
    public void testHeapProperty ()
    {
		PQueue q = new PQueue();
    	Integer[] nums = { new Integer(3),new Integer(2), new Integer(5), new Integer(6), new Integer(7), new Integer(9), new Integer(4), new Integer(8), new Integer(1) };
    
    	// Try manually creating heap
	     
	   
    	for (int i = 0; i <= 8; i++ )
    	//for (int i = ??; i <= 8; i++ )
    	{sketch --fe-tempdir result --fe-keep-tmp --fe-output sk_PQueue --fe-inc result/sk_PQueue result/sk_PQueue/main.sk --bnd-unroll-amnt 10 --bnd-inline-amnt 3

			q.add(nums[i]);
    	}

    	//for (int i = 1; i <= 9; i++)
		for (int i = 1; i <= 9; i++)
    	{
        	Integer ii = q.poll();
			assert (i == ii.intValue());
    	}
    }

	@Test
  	public void testClear() 
	{
    	PQueue q = new PQueue();
    	Integer[] nums = {new Integer(11), new Integer(22), new Integer(33), new Integer(44), new Integer(55)};
    	for (int i = 0; i < 5; i++ )
    	{
			q.add(nums[i]);
    	}
    	q.clear();
    	Assert.assertEquals(q.size(), 0);
    	Assert.assertTrue(q.isEmpty());
	}

	
	@Test
  	public void testContainment() {

    	Integer[] nums = {new Integer(11), new Integer(22), new Integer(33), new Integer(44), new Integer(55)};    
    	PQueue q = new PQueue();
		for (int i = 0; i < 5; i++ )
    	{
			q.add(nums[i]);
    	}
    	q.remove(new Integer(11));
    	Assert.assertFalse(q.contains(new Integer(11)));
    	q.remove(new Integer(22));
    	Assert.assertFalse(q.contains(new Integer(22)));
    	q.remove(new Integer(33));
    	Assert.assertFalse(q.contains(new Integer(33)));
    	q.remove(new Integer(44));
    	Assert.assertFalse(q.contains(new Integer(44)));
    	q.clear();
    	Assert.assertFalse(q.contains(new Integer(55)));


	}
	
	// There is no assert in the test, so no constraints! We don't need them! 
	/*
	@Test
  	public void testRemoving() {

    	Integer [] in = {new Integer(1),new Integer(2),new Integer(3),new Integer(4),new Integer(5), new Integer(6),new Integer(7)};
    	Integer [] removeOrder = { new Integer(1),new Integer(3),new Integer(6),new Integer(4),new Integer(5),new Integer(7),new Integer(2) };
    	sequentialRemoving(in, removeOrder);

    	in = new Integer[] {new Integer(1),new Integer(2),new Integer(3),new Integer(4),new Integer(5), new Integer(6),new Integer(7),new Integer(8), new Integer(9),new Integer(10),new Integer(11)};
    	removeOrder = new Integer[] {new Integer(7),4,6,10,2,5,11,3,1,8,9};
    	sequentialRemoving(in, removeOrder);

	}
	*/
	
	@Test
  	public void testRemovingDuplicates() {

    	Integer[] in = {new Integer(2), new Integer(7), new Integer(2), new Integer(11), new Integer(7),new Integer(13),new Integer(2)};
		PQueue pq = new PQueue();
   		for (int i = 0; i < 7; i++ )
    	{
			pq.add(in[i]);
    	}

	// the double dot does not work(function_a().function_b()), so needs a temporary variable

	Integer tmp = pq.peek();
    	Assert.assertTrue(tmp.intValue()==2);
    	pq.add(new Integer(3));
	
	tmp = pq.poll();
    	Assert.assertTrue(tmp.intValue() == 2);
	tmp = pq.poll();
    	Assert.assertTrue(tmp.intValue() == 2);
	tmp = pq.poll();
    	Assert.assertTrue(tmp.intValue() == 2);
	tmp = pq.poll();    	
	Assert.assertTrue(tmp.intValue() == 3);
	tmp = pq.poll();
    	Assert.assertTrue(tmp.intValue() == 7);
	tmp = pq.poll();
    	Assert.assertTrue(tmp.intValue() == 7);
	tmp = pq.poll();
    	Assert.assertTrue(tmp.intValue() == 11);
	tmp = pq.poll();
   	Assert.assertTrue(tmp.intValue() == 13);

	}
}










