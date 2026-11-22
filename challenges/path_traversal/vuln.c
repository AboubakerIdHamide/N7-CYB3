#include <stdio.h>
#include <string.h>

int main(void) {
    char path[128];
    char contents[256];
    FILE *file;

    fputs("Choose a page under pages/: ", stdout);
    fflush(stdout);
    if (fgets(path, sizeof(path), stdin) == NULL) {
        fputs("No path received.\n", stderr);
        return 2;
    }
    path[strcspn(path, "\r\n")] = '\0';

    /* This prefix check is intentionally incomplete: it does not stop ../. */
    if (strncmp(path, "pages/", 6) != 0) {
        fputs("Pages must be selected from the pages directory.\n", stderr);
        return 1;
    }

    file = fopen(path, "r");
    if (file == NULL) {
        fputs("Page not found.\n", stderr);
        return 1;
    }
    while (fgets(contents, sizeof(contents), file) != NULL) {
        fputs(contents, stdout);
    }
    fclose(file);
    return 0;
}
