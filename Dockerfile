FROM usgsastro/miniflask
RUN conda install -c conda-forge flask
ADD . /app
WORKDIR /app

CMD ["python","nomen.py"]
