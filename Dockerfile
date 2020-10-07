FROM caida/bgpstream:latest
LABEL maintainer="Mingwei Zhang <mingwei@caida.org>"

WORKDIR /tmp
COPY pybgpstream-print.py pybgpstream-print.py


ENTRYPOINT ["/usr/bin/python3"]
CMD ["pybgpstream-print.py"]