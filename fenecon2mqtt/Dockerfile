# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Execute during the build of the image
ARG TEMPIO_VERSION BUILD_ARCH
RUN \
    curl -sSLf -o /usr/bin/tempio \
    "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}"

# Copy and install Python requirements
COPY requirements.txt /tmp/

RUN cd /tmp \
    && apk add apparmor \
    && apk add apparmor-utils

RUN cd /tmp \
    && pip3 install \
        --no-cache-dir \
        --prefer-binary \
        -r ./requirements.txt

# Copy root filesystem
COPY rootfs /
