#include "tools.h"
int main()
{
    MPI_Init(NULL, NULL);
    int list_lengths[3] = {10000, 50000, 100000};
    int Len = sizeof(list_lengths) / sizeof(list_lengths[0]);

    for (int i = 0; i < Len; i++)
    {
        pure_mpi_function(list_lengths[i]);
    }

    MPI_Finalize();
    return 0;
}
