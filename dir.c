#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>

void lista_directorio(char *nombre);

int main(int argc, char *argv[]) {
	
	if (argc != 2) {
		printf("Indique el directorio a mostrar\n");
		return 1;
	}
	lista_directorio(argv[1]);
}


//Función que permite listar un directorio de manera recursiva
void lista_directorio(char *nombre){

	//Declaramos variables, estructuras
	struct stat atri;
	struct dirent *archivo;
	DIR *dire;

	dire = opendir(nombre);

	// printf("abriendo el directorio %s\n",nombre);
	//Recorrer directorio
	while((archivo=readdir(dire))!=NULL){
		//strcmp permite comparar, si la comparación es verdadera devuelve un 0
		//Aquí se pregunta si el archivo o directorio es distinto de . y ..
		//Para así asegurar que se muestre de forma recursiva los directorios y ficheros del directorio actual
		if((strcmp(archivo->d_name,".")!=0)&&(strcmp(archivo->d_name,"..")!=0)){
			char *ruta;
			strcat(ruta,nombre);
#ifdef _WIN32
			strcat(ruta,"\\");
#endif

#ifdef linux
			strcat(ruta,"/");
#endif
			strcat(ruta,archivo->d_name);
			int res = stat(ruta,&atri);
			printf("%s\n", ruta);
			printf("%d\n", res);
			//Si es un directorio, llamar a la misma función para mostrar archivos
			if(S_ISDIR(atri.st_mode)){
				printf("%s es directorio\n", archivo->d_name);
				lista_directorio(ruta);
				//Si no es directorio, mostrar archivos
			}
			else{
				printf(" %s\n", archivo->d_name);
			}
		}

	}
	closedir(dire);
	 
}


