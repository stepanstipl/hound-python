FROM alpine:3.5

#ENV HOUND_GIT=https://github.com/houndci/hound.git
ENV REDIS_URL=redis://redis:6379

COPY . /hound-python

RUN apk add --update \
           build-base \
           python3-dev \
           python3 \
           su-exec \
    && cd hound-python \
    && pip3 install -U -r requirements.txt \
    && rm -rf /var/cache/apk/* \
    && adduser -S -D -H hound

WORKDIR /hound-python

ENTRYPOINT ["su-exec", "hound"]
CMD ["python3", "worker.py", "python_review"]
