FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /opt/project
ENV PYTHONPATH="/opt/project"

# Shared tooling layer (identical for all projects)
RUN apt-get update && apt-get install -y --no-install-recommends \
        git openssh-client curl ca-certificates \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        -o /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
        > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update && apt-get install -y --no-install-recommends gh \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install jupyterlab

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

EXPOSE 8888
CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--allow-root", "--no-browser", "--notebook-dir=/opt/project"]
