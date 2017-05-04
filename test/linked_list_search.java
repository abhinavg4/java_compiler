class ifib{
    int append(int l,int a);
    int printInt(int n);
    int next(int l);
    int val(int l);
    public static void main() {
        int l;
        int i;
        int y = append(0,1);
        l = y;
        for (i = 0;i<5;i++)
          y = append(y,i+3);

        for(i=0;i<5;i++){
          int h = val(l);
          if(h == 5){
            printInt(1);
          }
          l=next(l);
        }
    }
}
