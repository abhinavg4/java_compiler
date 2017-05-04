class ackermann{
    int printInt(int n);

    int Ack(int m,int n) {
        int i = -1, j = -1;
        if (m>=0 && n>=0) {
            if (m == 0) {
                i = n + 1;
            } else if (n == 0) {
                i = Ack(m - 1, 1);
            } else {
                j = Ack(m, n - 1);
                i = Ack(m - 1, j);
            }
        }
        return i;
    }
    public static void main(){
        int i = Ack(3,4);
        printInt(i);
    }
}
