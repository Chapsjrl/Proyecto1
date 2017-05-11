#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>

int dire(char *name){
	struct dirent *archivo;
	struct stat sb;
	DIR *dir;
	dir = opendir(name);
	while((archivo=readdir(dir))!=NULL){
 //strcmp permite comparar, si la comparación es verdadera devuelve un 0
 //Aquí se pregunta si el arhivo o directorio es distinto de . y ..
 //Para así asegurar que se muestre de forma recursiva los directorios y ficheros del directorio actual
	 if((strcmp(archivo->d_name,".")!=0)&&(strcmp(archivo->d_name,"..")!=0)){
		 stat(archivo->d_name,&sb);
		 //Si es un directorio, llamar a la misma función para mostrar archivos
		 if(S_ISDIR(sb.st_mode)){
		 	dire(archivo->d_name);
		 //Si no es directorio, mostrar archivos
		 }else{
			 printf(" %s\n", archivo->d_name);
		 }
	 }
	 
	}
	printf("\n");
	closedir(dir);
}

int main(int argc, char *argv[]) {
	
	if (argc != 2) {
		printf("Indique el directorio a mostrar\n");
		return 1;
	}
	dire(argv[1]);
}
