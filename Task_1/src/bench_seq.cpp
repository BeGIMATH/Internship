
#include "tools.h"


int main(int argc, char *argv[])
{
    
    int list_lengths[3] = {1000,5000,10000};
    int Len = sizeof(list_lengths)/sizeof(list_lengths[0]);
    for(int i = 0; i < Len; i++){
         seq_function(list_lengths[i]);
    }
}