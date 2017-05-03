class ackermann{
    int printInt(int n);
    int Ack(int m,int n) {
        int i ;
        if (m>=0 && n>=0) {
            if (m == 0) {
                i = n + 1;
            } else if (n == 0) {
                int j=m-1;
                i = Ack(j, 1);
            } else {
                int j = m-1;
                i = Ack(j, Ack(m, n - 1));
            }
        }
        return i;
    }
    public static void main(){
        int i = Ack(3,4);
        printInt(i);
    }
}
