FROM python:3
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ["./sendpromotion.py","invokes.py","amqp_setup.py", "./"]
CMD [ "python", "./sendpromotion.py","./invokes.py"]