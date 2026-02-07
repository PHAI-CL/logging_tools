# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set the working directory and PYTHONPATH
WORKDIR /opt/project
ENV PYTHONPATH "${PYTHONPATH}:/opt/project"

# Copy project files to /opt/project
COPY . /opt/project

# Install pip requirements
RUN python -m pip install -r /opt/project/requirements.txt

# Install Jupyterlab
RUN pip install jupyterlab
EXPOSE 8888

# Start the Jupyter server
CMD jupyter lab --ip 0.0.0.0 --allow-root --no-browser --notebook-dir='/opt/project'
