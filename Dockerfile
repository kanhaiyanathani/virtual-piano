FROM python:3

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get -y install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 python3-tk
#COPY requirements.txt ./
RUN pip install pyaudio numpy matplotlib pygame
#--no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./music_syn.py" ]