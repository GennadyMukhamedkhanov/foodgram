FROM python:3.10.9-slim
WORKDIR /backend
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .






RUN pip install gunicorn

#CMD ["gunicorn","-b","0.0.0.0:8000","conf.wsgi"]

#RUN gunicorn -b 0.0.0.0:8000 conf.wsgi