FROM python:3.11-slim-bookworm

RUN apt-get update -y && apt-get install -y ca-certificates fuse3 sqlite3
COPY --from=flyio/litefs:0.5 /usr/local/bin/litefs /usr/local/bin/litefs
ADD litefs/litefs.static-lease.yml /etc/litefs.yml

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY src/ .

ENTRYPOINT litefs mount
