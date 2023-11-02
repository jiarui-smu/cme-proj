FROM python:3
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ["order.py", "./"]
CMD [ "python", "./order.py"]