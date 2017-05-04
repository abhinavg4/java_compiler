public class MyBinarySearch {
    int printInt(int n);

    public int binarySearch(int inputArr[], int len, int key) {
        int start = 0,mid;
        int end = len - 1;
        while (start <= end) {
            mid = (start + end) / 2;
            if (key == inputArr[mid]) {
                return mid;
            }
            if (key < inputArr[mid]) {
                end = mid - 1;
            } else {
                start = mid + 1;
            }
        }
        return -1;
    }
    public static void main() {
        //MyBinarySearch mbs = new MyBinarySearch();
        int arr[] = new int[8];
        arr[0] = 2;
        arr[1] = 4;
        arr[2] = 6;
        arr[3] = 8;
        arr[4] = 10;
        arr[5] = 12;
        arr[6] = 14;
        arr[7] = 16;
        printInt(binarySearch(arr, 8, 14));

        int arr1[] = new int[6];
        arr1[0] = 6;
        arr1[1] = 34;
        arr1[2] = 78;
        arr1[3] = 123;
        arr1[4] = 432;
        arr1[5] = 900;
        printInt(binarySearch(arr1, 6, 431));
    }
}
