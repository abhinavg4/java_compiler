class short_circuit{
    int printInt(int n);

    public static void main(){
        int i=1;

        if(i==1 || 1/0)
        {
           printInt(10);
        }

        if((i==0 && i==2) || i!=1)
        {
           printInt(15);
        }
    }
}
