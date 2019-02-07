FROM python:3.6

ENV UPLOAD_URL http://ingestfrontend:8066/upload
ENV UPLOAD_STATUS_URL http://ingestfrontend:8066/get_state
ENV UPLOAD_POLICY_URL http://policyserver:8181/uploader
ENV UPLOAD_VALIDATION_URL http://policyserver:8181/ingest
ENV DOWNLOAD_URL http://cartdfrontend:8081
ENV DOWNLOAD_POLICY_URL http://policyserver:8181/status/transactions/by_id
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install .
RUN mkdir /etc/pacifica-cli
RUN cp travis/uploader.json /etc/pacifica-cli
RUN cp docs/_static/example.ini /etc/pacifica-cli
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
