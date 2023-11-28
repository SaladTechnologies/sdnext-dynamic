FROM saladtechnologies/sdnext:latest

RUN apt-get update && apt-get install -y \
  curl \
  jq

COPY entrypoint .
COPY readiness.py /probes/readiness.py

ENV HOST='[::]'
ENV PORT=7860

ENTRYPOINT ["./entrypoint"]

CMD []