FROM rasa/rasa:latest-full 

USER root

WORKDIR /app
COPY . /app
COPY ./data /app/data
COPY ./external_data /app/external_data
RUN pip3 install --upgrade pip --user
RUN pip3 install nltk
RUN  python3 -m rasa train

# Switch back to a non-root user
USER 1001

VOLUME /app
VOLUME /app/data
VOLUME /app/models
VOLUME /app/external_data


CMD [ "run","-m","/app/models","--enable-api","--cors","*","--debug"]