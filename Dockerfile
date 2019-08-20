FROM python:3.7-slim

LABEL Maintainer = "Alvaro Mourino <alvaro@mourino.net>"

WORKDIR /usr/src/dnstls
COPY src .

EXPOSE 53/tcp 53/udp
# ENTRYPOINT ["/usr/src/dnstls/entrypoint.sh"]
CMD ["python3", "/usr/src/dnstls/main.py"]
