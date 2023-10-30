FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
# ENV AMQP_HOST=localhost
# ENV AMQP_PORT=5672
# ENV AMQP_USER=guest
# ENV AMQP_PASSWORD=guest
COPY ["make_payment.py", "invokes.py", "amqp_setup.py", "./"]
CMD [ "python", "./make_payment.py", "./invokes.py"]