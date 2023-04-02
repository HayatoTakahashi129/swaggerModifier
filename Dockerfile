FROM python:3.9-slim
MAINTAINER HayatoTakahashi

COPY ./ ./

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PATH "${PATH}:/bin"

RUN pip install -r requirements.txt

CMD ["/bin/bash"]
# ENTRYPOINT ["python","swaggerModifier/__main__.py"]