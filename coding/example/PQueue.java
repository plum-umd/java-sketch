/**
 * A min priority queue implementation using a binary heap.
 * @author William Fiset, william.alexandre.fiset@gmail.com
 **/

import java.util.*;

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
  }
  
  
  // Return the size of the heap
  public int size() {
    return heapSize;
  }

  // Returns true/false depending on if the priority queue is empty
  public boolean isEmpty() {
    return heapSize == 0;
  }

  // Construct a priority queue using heapify in O(n) time, a great explanation can be found at:
  // http://www.cs.umd.edu/~meesh/351/mount/lectures/lect14-heapsort-analysis-part.pdf
 // public PQueue (int[] elems) {

	// unnecessary constructor
  // Priority queue construction, O(nlog(n))
 // public PQueue (Collection <Integer> elems) {
//    this(elems.size());
//    for( int elem : elems) add(elem);
//  }
//------------------------------------------------------------------------------------------
// The above working now
  


 

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
  

//---------------------------------------------------------Below does not work---------------------------------------------

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
    if (set != null) return set.last();   //need to implement last!!!!!!!!!
    return null;
  }



  // Removes a particular element in the heap, O(log(n))
  public boolean remove(Integer element) {
    
    if (element == null) return false;
    
    // Linear removal via search, O(n)
     for (int i = 0; i < heapSize; i++) {
       if (element.equals(heap.get(i))) {
        // removeAt(i);
         return true;
       }
     }

    // Logarithmic removal with map, O(log(n))
    Integer index = mapGet(element);
    //if (index != null) removeAt(index);
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
      if ( left >= heapSize || less(k, smallest)) return;  // Caused by this line But the terminal says something wrong with Arraylist
      
      // Move down the tree following the smallest node
     // swap(smallest, k);
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
 // private void swap(int i, int j) {
    
  //  Integer i_elem = heap.get(i);
 //   Integer j_elem = heap.get(j);

 //   heap.set(i, j_elem);
 //   heap.set(j, i_elem);
//
    //mapSwap(i_elem, j_elem, i, j);

 // }

/*
  // Removes a node at particular index, O(log(n))
  private Integer removeAt(int i) {
    
    if (isEmpty()) return null;

    heapSize--;
    int removed_data = heap.get(i);
    swap(i, heapSize);

    // Obliterate the value
    heap.set(heapSize, null);
    mapRemove(removed_data, heapSize);

    // Removed last element
    if (i == heapSize) return removed_data;

    int elem = heap.get(i);

    // intry sinking element
    sink(i);

    // If sinking did not work try swimming
    if ( heap.get(i).equals(elem) )
      swim(i);

    return removed_data;

  }


 

  
*/
/*





  // Clears everything inside the heap, O(n)
  public void clear() {
    for (int i = 0; i < heapCapacity; i++)
      heap.set(i, null);
    heapSize = 0;
    map.clear();
  }

  
 

  // Returns the value of the element with the lowest
  // queue is empty null is returned.
  public Integer peek() {
    if (isEmpty()) return null;
    return heap.get(0);
  }

  // Removes the root of the heap, O(log(n))
  public Integer poll() {
    return removeAt(0);
  }

  // intest if an element is in heap, O(1)
  public boolean contains(Integer elem) {

    // Map lookup to check containment, O(1)
    if (elem == null) return false;
    return map.containsKey(elem);

    // Linear scan to check containment, O(n)
    // for(int i = 0; i < heapSize; i++)
    //   if (heap.get(i).equals(elem))
    //     return true;
    // return false;

  }


  // Adds an element to the priority queue, the 
  // element must not be null, O(log(n))
  public void add(Integer elem) {
    
    if (elem == null) throw new IllegalArgumentException();

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

  


  // Recursively checks if this heap is a min heap
  // This method is just for testing purposes to make
  // sure the heap invariant is still being maintained
  // Called this method with k=0 to start at the root
 // public boolean isMinHeap(int k)
  
 
*/

 // Something wrong with this part
 // @Override public String toString() {
 //   return heap.toString();

 // }
  

  harness static void m()
  {
    static final int LOOPS = 1000;

    static final int MAX_SZ = 100;


    PQueue q = new PQueue();

    assert q.size()== 0;

    assert q.isEmpty();

  //  assertEquals(q.poll(), null);

  //  assertEquals(q.peek(), null);

  }
}












