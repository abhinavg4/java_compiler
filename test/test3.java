// Generic List

package Fall0811;
import java.util.Iterator;

public class GenericList<E> implements Iterable<E>{
 // class constant
    private static final int DEFAULT_CAP = 10;
 
    // instance variables
    protected E[] container; // the array is NOT the list
    private int listSize;
    
    public Iterator<E> iterator(){
        return new GenListIterator();
    }
    
    // inner class
    private class GenListIterator implements Iterator<E>{
        private int indexOfNextElement;
        private boolean okToRemove;
        
        private GenListIterator(){
            indexOfNextElement = 0;
            okToRemove = false;
        }
    }   
}
