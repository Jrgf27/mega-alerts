# syntax=docker/dockerfile:1

# Alpine is chosen for its small footprint
# compared to Ubuntu

FROM python:slim-bookworm

RUN pip3 install tenacity requests PyQt5 \
    && apt-get update \
    && apt-get install -y libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
RUN mkdir /app/data/
RUN mkdir /app/user_data/
RUN mkdir /app/user_data/mega/
RUN mkdir /app/user_data/simple/
RUN mkdir /app/utils/
COPY ./mega_alerts.py /app/
COPY ./utils/* /app/utils/
COPY ./data/* /app/data/
COPY ./user_data/mega/* /app/user_data/mega/
COPY ./user_data/simple/* /app/user_data/simple/
COPY ./run /app/
RUN chmod +x /app/*

CMD ["python3", "/app/mega_alerts.py"]

# run local
#  docker run -dit \
#      --name wow-test \
#      --env WOW_REGION=NA \
#      --env DESIRED_ITEMS='{"194641": 500000, "159840":40000}' \
#      --env DESIRED_PETS='{"3390": 2700}' \
#      --env MEGA_WEBHOOK_URL=$MEGA_WEBHOOK_URL \
#      --env WOW_CLIENT_ID=$WOW_CLIENT_ID \
#      --env WOW_CLIENT_SECRET=$WOW_CLIENT_SECRET \
#      cohenaj194/mega-alerts

## run local ilvl
#  docker run -dit \
#      --name wow-test \
#      --env WOW_REGION=NA \
#      --env DESIRED_ILVL='{"ilvl": 470, "buyout": 5000000, "sockets": false, "speed": false, "leech": false, "avoidance": false}' \
#      --env MEGA_WEBHOOK_URL=$MEGA_WEBHOOK_URL \
#      --env WOW_CLIENT_ID=$WOW_CLIENT_ID \
#      --env WOW_CLIENT_SECRET=$WOW_CLIENT_SECRET \
#      cohenaj194/mega-alerts

## test the list from my env
# docker run -dit \
#     --name wow-test \
#     --env DEBUG=true \
#     --env WOW_REGION=NA \
#     --env DESIRED_ILVL_LIST="$DESIRED_ILVL_LIST" \
#     --env MEGA_WEBHOOK_URL="$MEGA_WEBHOOK_URL" \
#     --env WOW_CLIENT_ID="$WOW_CLIENT_ID" \
#     --env WOW_CLIENT_SECRET="$WOW_CLIENT_SECRET" \
#     cohenaj194/mega-alerts-test