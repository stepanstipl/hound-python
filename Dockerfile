FROM alpine:3.5

#ENV HOUND_GIT=https://github.com/houndci/hound.git
ENV REDIS_URL=redis://redis:6379

COPY . /hound-python

RUN apk add --update --virtual build-deps \
           build-base \
           python-dev \
    && apk add --update \
           python \
           py-pip \
           su-exec \
    && cd hound-python \
    && pip install -U -r requirements.txt \
    && apk del build-deps \
    && rm -rf /var/cache/apk/* \
    && adduser -S -D -H hound

WORKDIR /hound-python

ENTRYPOINT ["su-exec", "hound"]
CMD ["python", "worker.py", "python_review"]
