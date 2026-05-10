FROM caida/bgpstream@sha256:d808116911c107926451f882295d85c80940285791ff38c7e6999976d355e3d4
LABEL maintainer="Adam Horsewood <a.horsewood@googlemail.com>"

WORKDIR /tmp
COPY pybgpstream_print.py pybgpstream_print.py

ENTRYPOINT ["/usr/bin/python3", "pybgpstream_print.py"]