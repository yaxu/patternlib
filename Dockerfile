FROM lvm23/tida1vm:0.9
MAINTAINER Mauro <mauro@sdf.org>

###
#
# Define ENV_VARS
#
###
ENV LANG C.UTF-8
ENV USER tidal
ENV UID 1000
ENV HOME /home/$USER
ENV PATH $PATH:$HOME/bin
ENV PROJECT patternlib
ENV PROJECT_HOME $HOME/$PROJECT/

ENV DEBIAN_FRONTEND noninteractive

###
#
# Install dependencies &&
# Create home and user dirs
#
###
RUN apt-get update \
    && apt-get install -yq wget unzip \
    python-pip git-core ca-certificates \
    python-setuptools python-dev \
    libxml2-dev libxslt1-dev \
    python-virtualenv libmysqlclient-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists \
    && useradd -u $UID -m -d $HOME -s /usr/sbin/nologin $USER \
    && wget https://github.com/lvm/patternlib/archive/master.zip -O $HOME/patternlib-master.zip
    && wget https://raw.githubusercontent.com/yaxu/tidalbot/master/runpattern.hs -O /tmp/runpattern.hs \
    && cabal update && cabal install hint tagsoup

###
#
# Install Tidal && Fix perms
#
###

RUN unzip $HOME/patternlib-master.zip -d $HOME \
    && mv $HOME/patternlib-master $PROJECT_HOME \
    && chown -Rh $USER:$USER -- $HOME

###
#
# Init
#
###
USER $USER
WORKDIR $HOME
