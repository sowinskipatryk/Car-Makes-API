FROM python:3.10

ENV DockerHOME=/home/app/carmakesapi

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . $DockerHOME
WORKDIR $DockerHOME

EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]