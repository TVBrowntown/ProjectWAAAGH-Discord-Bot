FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/TVBrowntown/ProjectWAAAGH-Discord-Bot.git .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV BOT_TOKEN=your_bot_token_here
ENV MYSQL_HOST=localhost
ENV MYSQL_USER=yourusername
ENV MYSQL_PASSWORD=yourpassword
ENV MYSQL_DATABASE=projectwar

CMD [ "python", "daemon.py" ]