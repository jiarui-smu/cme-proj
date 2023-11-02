FROM python:3
ENV dbURL 'mysql+mysqlconnector://root@localhost:3306/quikkarts'
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./app.py .
CMD [ "python", "./app.py" ]