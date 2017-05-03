class mutual_recursion{
    public static int fact(int a){
      int b=1;
      if(a==1){
        return b;
      }
      b = a*fact(a-1);
      return b;
    }
    public static void main(){
      int a;
      a = fact(5);
    }
}
