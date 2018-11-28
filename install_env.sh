#!/bin/bash

yum -y install gcc gcc-c++ make git patch openssl-devel zlib-devel readline-devel sqlite-devel bzip2-devel bzip2-libs

curl -L https://raw.github.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

echo -e '\n#pyenv' >>~/.bashrc
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

source ~/.bashrc

wget --no-check-certificate https://pypi.python.org/packages/source/t/tornado/tornado-4.0.tar.gz


tar zxf tornado-4.0.tar.gz && cd tornado-4.0 && python setup.py build && python setup.py install
