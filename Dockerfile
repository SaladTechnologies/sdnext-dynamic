FROM saladtechnologies/sdnext:beta

RUN apt-get update && apt-get install -y \
  curl \
  jq

COPY entrypoint .

ENV HOST='0.0.0.0'
ENV PORT=7860

ENTRYPOINT ["./entrypoint"]

CMD []