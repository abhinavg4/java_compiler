class ackermann{
    int printInt(int n);

    public static void main(){
      int i, j, k;
              int a[][] = new int[2][2];
              int b[][] = new int[2][2];
              a[0][0]=1;
              a[0][1]=2;
              a[1][0]=3;
              a[1][1]=4;
              b[0][0]=5;
              b[0][1]=6;
              b[1][0]=7;
              b[1][1]=8;
              /* Create another 2d array to store the result using the original arrays' lengths on row and column respectively. */
              int r[][] = new int[2][2];
              /* Loop through each and get product, then sum up and store the value */
              for (i = 0; i < 2; i++) {
                  for (j = 0; j < 2; j++) {
                      for (k = 0; k < 2; k++) {
                          r[i][j] =  r[i][j] + a[i][k] * b[k][j];
                      }
                  }
              }
              /* Show the result */
              for (i = 0; i < 2; i++) {
                  for (k = 0; k < 2; k++) {
                      printInt(r[i][k]);
                  }
              }    }
}
