FROM python

COPY base.db dataset_faces.dat dataset_name.dat Dockerfile README.md requirements.py search.py server.crt server.key server.py /search_face
WORKDIR /search_face

RUN apt-get update && \
    apt-get install -y cmake && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get install -y python3-dev python3-pip python3-numpy && \
    apt-get install -y libopencv-dev libatlas-base-dev && \
    apt-get install -y libssl1.1

RUN ln -sf /usr/lib/x86_64-linux-gnu/libssl.so.1.1 /usr/lib/x86_64-linux-gnu/libssl.so

RUN pip3 install --upgrade pip

RUN pip3 install dlib

RUN pip3 install -r requirements.txt

EXPOSE 9090

CMD python3 server.py