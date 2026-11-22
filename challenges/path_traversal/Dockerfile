FROM gcc:12-bookworm AS build
WORKDIR /src
COPY vuln.c ./vuln.c
RUN gcc -Wall -Wextra -O2 -o /path-viewer vuln.c

FROM debian:bookworm-slim
WORKDIR /opt/challenge
COPY --from=build --chown=0:0 /path-viewer ./challenge
COPY --chown=0:0 flag.txt.example ./flag.txt
COPY --chown=0:0 pages ./pages
RUN chmod 0555 ./challenge && chmod 0444 ./flag.txt ./pages/welcome.txt && chmod 0555 ./pages
USER 65534:65534
ENTRYPOINT ["/opt/challenge/challenge"]
