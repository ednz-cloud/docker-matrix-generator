FROM gcr.io/distroless/python3-debian10

COPY action /action

WORKDIR /action

ENV PYTHONPATH /action

CMD ["/action/matrix_generator.py"]
