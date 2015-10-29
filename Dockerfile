FROM ubuntu
ADD ./*.py /tmp/emailbin/
RUN apt-get update
RUN apt-get install -y nginx python3-pip python3-dev
RUN pip3 install logbook
ADD ./emailb.in.conf /etc/nginx/sites-enabled/emailb.in.conf
EXPOSE 25
EXPOSE 80
CMD /etc/init.d/nginx start; /usr/bin/python3 /tmp/emailbin/emailb.in.py
