FROM python:3.10

WORKDIR /usr/src/app
RUN mkdir tech_challenge_001

COPY ./requirements.txt ./tech_challenge_001

RUN pip install -r /usr/src/app/tech_challenge_001/requirements.txt

COPY . ./tech_challenge_001

RUN bash "/usr/src/app/tech_challenge_001/sh/00-install.sh"

CMD [ "/bin/bash", "-c", "/usr/src/app/tech_challenge_001/sh/01-run.sh"]