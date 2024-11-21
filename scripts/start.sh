uwsgi --https 0.0.0.0:8443,../certs/fullchain.pem,../certs/privkey.pem --master --processes 1 -w main:app
