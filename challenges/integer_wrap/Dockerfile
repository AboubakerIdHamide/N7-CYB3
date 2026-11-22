FROM gcc:12-bookworm AS build
WORKDIR /src
COPY vuln.c ./vuln.c
RUN gcc -Wall -Wextra -O2 -o /integer-wrap vuln.c

FROM debian:bookworm-slim
WORKDIR /opt/challenge
COPY --from=build --chown=0:0 /integer-wrap ./challenge
COPY --chown=0:0 flag.txt.example ./flag.txt
RUN chmod 0555 ./challenge && chmod 0444 ./flag.txt
USER 65534:65534
ENTRYPOINT ["/opt/challenge/challenge"]
