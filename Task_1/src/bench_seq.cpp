
#include "tools.h"

int main(int argc, char *argv[])
{

    int list_lengths[3] = {10000, 50000, 100000};
    int Len = sizeof(list_lengths) / sizeof(list_lengths[0]);
    for (int i = 0; i < Len; i++)
    {
        seq_function(list_lengths[i]);
    }
}