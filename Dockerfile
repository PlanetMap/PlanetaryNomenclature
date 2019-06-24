FROM usgsastro/miniflask
RUN echo "http://mirror.leaseweb.com/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add --no-cache gcc libc-dev geos-dev
RUN conda install -c conda-forge flask psycopg2
ADD . /
WORKDIR /app

CMD ["python","nomen.py"]
