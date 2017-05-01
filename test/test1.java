class mutual_recursion{
    int fact(int n){
        if (n==1){
          return 1;
        }
        int q = n + fact(n-1);
        return q;
    }
    public static void main(){
        int i = fact(2);
    }
}
