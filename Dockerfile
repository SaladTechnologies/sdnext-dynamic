FROM saladtechnologies/sdnext:latest

RUN apt-get update && apt-get install -y \
  curl \
  jq

COPY entrypoint .
COPY readiness.py .

ENV HOST='0.0.0.0'
ENV PORT=7860

ENTRYPOINT ["./entrypoint"]

CMD []