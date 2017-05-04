class many_para_func{
    int printInt(int n);

    int sum(int a, int b, int c, int d, int e, int f, int g, int h, int i, int j){
        return (a+b+c+d+e+f+g+h+i+j);
    }
    public static void main(){
        printInt(sum(1,2,3,4,5,6,7,8,9,10));
    }
}
