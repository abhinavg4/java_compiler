class linked_list_search{
    int append(int l,int a);
    int printInt(int n);
    int next(int l);
    int val(int l);
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

        y = l[3];
        for(i=0;i<5;i++){
          int h = val(y);
          printInt(h);
          y=next(y);
        }
    }
}
