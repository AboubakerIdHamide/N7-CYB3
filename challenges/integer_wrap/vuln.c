#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

/* Read the dummy flag only after the narrowed ticket count wraps to zero. */
static void reveal_flag(void) {
    char flag[128];
    FILE *file = fopen("flag.txt", "r");

    if (file == NULL || fgets(flag, sizeof(flag), file) == NULL) {
        if (file != NULL) {
            fclose(file);
        }
        fputs("Could not read local dummy flag.\n", stderr);
        exit(2);
    }
    fclose(file);
    fputs(flag, stdout);
}

int main(void) {
    char line[128];
    char *end = NULL;
    unsigned long requested;
    uint8_t ticket_count;

    fputs("Enter ticket count: ", stdout);
    fflush(stdout);
    if (fgets(line, sizeof(line), stdin) == NULL) {
        fputs("No input received.\n", stderr);
        return 2;
    }

    errno = 0;
    requested = strtoul(line, &end, 10);
    if (errno != 0 || end == line || (*end != '\n' && *end != '\0')) {
        fputs("Invalid ticket count.\n", stderr);
        return 1;
    }

    /* The narrowing conversion is the intentional logic flaw in this exercise. */
    ticket_count = (uint8_t)requested;
    if (requested != 0 && ticket_count == 0) {
        reveal_flag();
        return 0;
    }

    puts("No flag for that ticket count.");
    return 0;
}
