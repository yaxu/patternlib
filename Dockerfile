FROM lvm23/tida1vm:0.9
MAINTAINER Mauro <mauro@sdf.org>

###
#
# ENV VARS 
#
##

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
ENV USER tidal
ENV UID 1000
ENV HOME /home/$USER
ENV PATH $PATH:$HOME/bin
ENV PROJECT patternlib
ENV PROJECT_HOME $HOME/$PROJECT/

###
#
# OS DEPENDENCIES
#
##

RUN apt-get update \
    && apt-get install -yq wget unzip \
    python-pip git-core ca-certificates \
    python-setuptools python-dev \
    libxml2-dev libxslt1-dev \
    build-essential libssl-dev libffi-dev \
    python-virtualenv libmysqlclient-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists

###
#
# USER & APP
#
##

RUN useradd -u $UID -m -d $HOME -s /usr/sbin/nologin $USER \
    && wget https://github.com/lvm/patternlib/archive/master.zip -O $HOME/patternlib-master.zip \
    && wget https://raw.githubusercontent.com/yaxu/tidalbot/master/runpattern.hs -O /tmp/runpattern.hs \
    && cabal update && cabal install hint tagsoup \
    && unzip $HOME/patternlib-master.zip -d $HOME \
    && mv $HOME/patternlib-master $PROJECT_HOME \
    && chown -Rh $USER:$USER -- $HOME

###
#
# uncomment for debugging purposes
#
##

COPY ["patternsite/local_settings.py", "$PROJECT_HOME/patternsite/local_settings.py"]

###
#
# DEFINE USER & WORKDIR
#
##

# USER $USER
WORKDIR $PROJECT_HOME

###
#
# DEPLOY
#
##

RUN pip install -r requirements.pip \
    && fab deploy_test
