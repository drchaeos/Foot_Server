FROM pytorch/pytorch
WORKDIR /
COPY . /

#WORKDIR /usr/src/app
#COPY . /usr/src/app

RUN apt-get update && apt-get install -y git && apt-get install -y build-essential

RUN pip3 install --user tensorboard cmake   # cmake from apt-get is too old
RUN pip3 install --user 'git+https://github.com/facebookresearch/fvcore'
RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo
RUN pip3 install --user -e detectron2_repo
RUN pip3 -q install pip --upgrade

RUN pip install -r requirements.txt

EXPOSE 9999

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app.main:create_app()"]

