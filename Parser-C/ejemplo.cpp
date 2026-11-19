
/* Demostración de validacion correcta */
int main() {
    int edad = 20;
    float promedio = edad + 2.5;
    bool aprobado = promedio >= 10;

    if (aprobado) {
        edad += 1;
    }

    return edad;
}

/* Demostración con error léxico

int main() {
    int edad = 20 @ 5;
    return edad;
}

*/