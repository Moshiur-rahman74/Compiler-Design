#include <stdio.h>
#include <string.h>
#include <ctype.h>
int main(){
    char a[200];
    printf("Enter input: ");
    fgets(a,sizeof(a),stdin);
    a[strcspn(a,"\n")]='\0';
    int c=0;
    for (int i = 0; a[i]; i++){
        if (a[i]==' ') c++;
    }
    if (c>0) {
        for (int i=0; a[i]; i++){
            if (i==0||a[i-1]==' ')
                printf("%c",toupper(a[i]));
        }
        return 0;
    }
    char x=a[0];
    for (int i=1;a[i];i++){
        if (a[i]!=x){
            printf("%c%c ",toupper(x),a[i]);
        }
    }
return 0;
}
