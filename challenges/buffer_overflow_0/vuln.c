#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Holds the dummy flag read from flag.txt when the program starts. */
static char flag[128];

/* The challenge uses this handler to reveal only its local dummy flag on a crash. */
static void on_crash(int signal_number) {
    (void)signal_number;
    fputs(flag, stdout);
    fputc('\n', stdout);
    fflush(stdout);
    _Exit(1);
}

/* Copy input into the intentionally undersized buffer used by this exercise. */
static void vulnerable_copy(const char *input) {
    char buffer[16];

    /* Intentionally unsafe: this is the vulnerability being studied. */
    strcpy(buffer, input);
    printf("Received: %s\n", buffer);
}

/* Load the dummy flag, accept one bounded line, then call the vulnerable copy. */
int main(void) {
    /* fgets keeps this teaching program's submitted line within a fixed limit. */
    char input[128];
    FILE *flag_file = fopen("flag.txt", "r");

    if (flag_file == NULL) {
        fputs("Missing local flag.txt; copy flag.txt.example first.\n", stderr);
        return 2;
    }
    if (fgets(flag, sizeof(flag), flag_file) == NULL) {
        fclose(flag_file);
        fputs("Could not read local dummy flag.\n", stderr);
        return 2;
    }
    fclose(flag_file);
    // Remove the line ending so the displayed flag has no extra blank line.
    flag[strcspn(flag, "\r\n")] = '\0';

    if (signal(SIGSEGV, on_crash) == SIG_ERR) {
        fputs("Could not install local crash handler.\n", stderr);
        return 2;
    }

    fputs("Input: ", stdout);
    fflush(stdout);
    if (fgets(input, sizeof(input), stdin) == NULL) {
        return 0;
    }
    // Keep the newline from fgets out of the value copied into the small buffer.
    input[strcspn(input, "\r\n")] = '\0';
    vulnerable_copy(input);
    return 0;
}
