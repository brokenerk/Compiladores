//gcc python_c.c -lpython3.7m -o p
#include <Python.h>
 
int main() {
	//Inicilizamos inteprete
	Py_Initialize();
	 
	//Prueba de compilaciom
	PyRun_SimpleString("print('Ya estas usando Python :D')");
	 
	//Terminamos inteprete
	Py_Finalize();
	 
	return 0;
}