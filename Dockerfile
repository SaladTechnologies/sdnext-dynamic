FROM saladtechnologies/sdnext:latest

RUN apt-get update && apt-get install -y \
  curl \
  jq

RUN wget https://raw.githubusercontent.com/SaladTechnologies/stable-diffusion-configurator/main/configure && \
  chmod +x configure

COPY entrypoint .
COPY readiness.py /probes/readiness.py
COPY healthcheck.py /probes/healthcheck.py

ENV HOST='[::]'
ENV PORT=7860

ENTRYPOINT ["./entrypoint"]

CMD []