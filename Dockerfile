FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y ffmpeg ghostscript wget && \
    apt-get install -y autoconf pkg-config build-essential curl libpng-dev && \
    wget https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.1-24.tar.gz && \
    tar xzf 7.1.1-24.tar.gz && \
    rm 7.1.1-24.tar.gz && \
    apt-get clean && \
    apt-get autoremove

RUN sh ./ImageMagick-7.1.1-24/configure --prefix=/usr/local --with-bzlib=yes --with-fontconfig=yes --with-freetype=yes --with-gslib=yes --with-gvc=yes --with-jpeg=yes --with-jp2=yes --with-png=yes --with-tiff=yes --with-xml=yes --with-gs-font-dir=yes && \
    make -j && make install && ldconfig /usr/local/lib/

WORKDIR /src

COPY ./ ./

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD tail -f /dev/null
