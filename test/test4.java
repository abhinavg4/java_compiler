// A class for measuring how long it takes for a program to run

/**
 A class to measure time elapsed.
*/

public class Stopwatch
{
    private long startTime;
    private long stopTime;

    public static final long NANOS_PER_SEC = 1000000000;

        /**
         start the stop watch.
        */
        int System,nanoTime;
        public long nanoTime(){}
        public void start(){
                startTime = System.nanoTime();
        }

        /**
         stop the stop watch.
        */
        public void stop()
        {       stopTime = System.nanoTime();   }

        /**
        elapsed time in seconds.
        @return the time recorded on the stopwatch in seconds
        */
        public double time()
        {       return (stopTime - startTime) / NANOS_PER_SEC;  }

        public String toString(){
            return "elapsed time: " + time() + " seconds.";
        }

        /**
        elapsed time in nanoseconds.
        @return the time recorded on the stopwatch in nanoseconds
        */
        public long timeInNanoseconds()
        {       return (stopTime - startTime);  }
}
