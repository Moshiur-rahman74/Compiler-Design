#include <stdio.h>
#include <string.h>
int main() {
    char line[1000];
    int line_count = 0;
    printf("Enter text:\n");
    for (;;) {
        fgets(line, sizeof(line), stdin);
        line[strcspn(line, "\n")] = '\0';
        if (strlen(line) == 0) {
            break;
        }
        line_count++;
    }
    printf("\nTotal number of lines: %d\n", line_count);
    return 0;
}
