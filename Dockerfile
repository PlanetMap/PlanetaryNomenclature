FROM usgsastro/miniflask
RUN conda install -c conda-forge flask psycopg2
ADD . /
WORKDIR /app

CMD ["python","nomen.py"]
