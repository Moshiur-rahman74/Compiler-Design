#include <stdio.h>
#include <string.h>
int main() {
    char text[500], target[500];
    int found = 0;
    printf("Enter the text:- ");
    fgets(text, sizeof(text), stdin);
    printf("Enter the target:- ");
    fgets(target, sizeof(target), stdin);
    text[strcspn(text, "\n")] = '\0';
    target[strcspn(target, "\n")] = '\0';
    if (strstr(text, target) != NULL) {
        printf("Found\n");
    } else {
        printf("Not Found\n");
    }
    return 0;
}
