FROM usgsastro/miniflask
RUN conda install -c conda-forge flask psycopg2
ADD . /app
WORKDIR /app

CMD ["python","nomen.py"]
