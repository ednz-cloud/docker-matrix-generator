FROM gcr.io/distroless/python3-debian12

COPY action /action

WORKDIR /action

ENV PYTHONPATH /action

CMD ["/action/matrix_generator.py"]
