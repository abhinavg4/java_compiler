class fileio{
    int scanString();
    int fcreate(int f);
    int fopen(int f);
    int fwrite(int f, int m);
    int fclose(int f);
    int fread(int f, int len);

    public static void main(){
      int file_name = scanString();

      int fd_out = fcreate(file_name);

      int msg = scanString();

      fwrite(fd_out, msg);

      fclose(fd_out);

      int fd_in = fopen(file_name);

      fread(fd_in, 5);
}}
