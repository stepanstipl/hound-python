FROM alpine:3.5

#ENV HOUND_GIT=https://github.com/houndci/hound.git
ENV REDIS_URL=redis://redis:6379

COPY . /hound-python

RUN apk add --update --virtual build-deps \
           build-base \
           python-dev \
           python3-dev \
    && apk add \
           python3 \
           python \
           py2-pip \
           su-exec \
    && cd hound-python \
    && pip3 install -U -r requirements.txt \
    && pip install -U -r requirements.txt \
    && rm -rf /var/cache/apk/* \
    && adduser -S -D -H hound

WORKDIR /hound-python

ENTRYPOINT ["su-exec", "hound"]
CMD ["python3", "worker.py", "python_review"]
