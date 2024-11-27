#include <stdlib.h>


int main() {
    int** t = NULL; // memory &t
    int** a = NULL;// memory &a 
    
    int*    e = NULL; // memory &e
    int** y = NULL; // memory &y
    {
        int* x = NULL; // memory &x
        e = (int*) malloc( sizeof(int ));// memory 1
        x = (int*) malloc( sizeof(int ));// memory 2
        y = &x;
        а = &у;
        t = &e;
        // Location 1
        free (x);
    ｝
    // Location 2
    return 0;
}