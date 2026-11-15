# Compile with the toolchain in a separate stage so it is absent at runtime.
FROM gcc:12-bookworm AS build
WORKDIR /src
COPY vuln.c ./vuln.c
RUN gcc -Wall -Wextra -O0 -g -fno-stack-protector -no-pie -o /vuln vuln.c

# Keep the final image small and limited to the program and dummy flag.
FROM debian:bookworm-slim
WORKDIR /opt/challenge
COPY --from=build --chown=0:0 /vuln ./vuln
COPY --chown=0:0 flag.txt.example ./flag.txt
RUN chmod 0555 ./vuln && chmod 0444 ./flag.txt
USER 65534:65534
ENTRYPOINT ["/opt/challenge/vuln"]
