FROM nvidia/cuda:latest                                                                                                                                                      
# FROM nvidia/cuda:9.1-base

RUN apt-get update -y

#install utility common command
RUN apt-get install -y --no-install-recommends wget sudo language-pack-ja fonts-ipafont fonts-ipaexfont libboost-dev nkf
# #install java
# RUN apt-get install -y --no-install-recommends default-jre default-jdk openjdk-8-jre openjdk-8-jdk
#install utility for jupyter
# RUN apt-get install -y --no-install-recommends software-properties-common build-essential git curl file make xz-utils patch
#install utility for mecab-ipadic-neologd
RUN apt-get install -y --no-install-recommends git curl file make xz-utils patch
# #install utility for rstudio
# # RUN apt-get install -y --no-install-recommends ed clang ccache software-properties-common dirmngr gpg-agent gdebi-core
# RUN apt-get install -y --no-install-recommends ed clang ccache software-properties-common dirmngr gdebi-core
# 
#create directory
RUN mkdir downloads

#install mecab
RUN apt-get install -y --no-install-recommends mecab libmecab-dev mecab-ipadic-utf8 && \
    git clone https://github.com/neologd/mecab-ipadic-neologd.git downloads/mecab-ipadic-neologd && \
    yes yes| downloads/mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd && \
    sed -i -e 's/\/var\/lib\/mecab\/dic\/debian/\/usr\/lib\/x86_64-linux-gnu\/mecab\/dic\/mecab-ipadic-neologd/' etc/mecabrc && \
    rm -rf downloads/*

# #install juman++
# RUN cd downloads && \
#     wget -q http://lotus.kuee.kyoto-u.ac.jp/nl-resource/jumanpp/jumanpp-1.01.tar.xz  && \
#     tar xJvf jumanpp-1.01.tar.xz && \
#     cd jumanpp-1.01 && \
#     ./configure && \
#     make && \
#     sudo make install

#install sudachi
# RUN yes 2| sudo update-alternatives --config java && \
#     yes 2| sudo update-alternatives --config javac && \
#     git clone https://github.com/WorksApplications/Sudachi.git downloads/Sudachi && \
#     cd downloads/Sudachi/ && \
#     mvn dependency:tree && \
#     mvn package
# FROM rottenfruits/analyticker:common


# FROM mytest:latest

#install jupyter                                                                                                                                                             
#https://daichan.club/linux/78323
RUN sudo apt-get update && \
    sudo apt-get install bzip2 && \
    wget -q https://repo.continuum.io/archive/Anaconda3-2019.03-Linux-x86_64.sh -P ./downloads/ && \
    bash ./downloads/Anaconda3-2019.03-Linux-x86_64.sh -b && \
    rm -f ./downloads/Anaconda3-2019.03-Linux-x86_64.sh
ENV PATH $PATH:/root/anaconda3/bin

RUN sudo apt-get update && \
    sudo apt-get install -y --no-install-recommends python-pydot python-pydot-ng graphviz
RUN conda install -y jupyter tensorflow-gpu keras pydotplus graphviz
RUN pip install -y --no-install-recommends dtreeviz
