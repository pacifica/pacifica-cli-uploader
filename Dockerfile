FROM python:3.6

ENV UPLOAD_URL http://localhost:8066/upload
ENV STATE_URL http://localhost:8066/get_state
ENV POLICY_URL http://localhost:8181/uploader
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install .
RUN cp travis/uploader.json .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
