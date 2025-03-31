#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    // Inicialitza el generador de nombres aleatoris
    srand(time(NULL));
    int random_number = rand(); // Genera un nombre aleatori
    printf("El número aleatori és: %d\n", random_number);
    return 0;
}
