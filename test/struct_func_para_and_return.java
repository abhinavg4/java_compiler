class complex_data_type{
    int append(int l,int a);
    int printInt(int n);
    int next(int l);
    int val(int l);
    public static int complex(int y){
      int i;
      for(i=0;i<5;i++){
        int h = val(y);
        printInt(h);
        y=next(y);
      }
      return 0;
    }
    public static void main() {
        int l[] = new int[5];
        int i,j,y;
        for (i=0;i<5;i++){
          y = append(0,1);
          l[i]=y;
          for(j=0;j<6;j++){
            y = append(y,i*j);
          }
        }
        complex(l[4]);

    }
}
