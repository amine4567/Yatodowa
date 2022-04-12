FROM node:16

# Install Angular CLI
RUN npm install -g @angular/cli

# Install prettier
RUN npm install -g prettier

# Install python 3.10 (from source)
RUN apt update &&\
    apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev &&\
    wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz &&\
    tar -xf Python-3.10.*.tgz &&\
    cd Python-3.10.*/ && ./configure --enable-optimizations &&\
    make -j 4 &&\
    make altinstall

# Install python requirements
COPY backend/requirements-combined.txt requirements-combined.txt
RUN python3.10 -m pip install -r requirements-combined.txt

# Terminal autocompletion
RUN curl https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash
RUN inv --print-completion-script bash > ~/.invoke-completion.sh

# Custom bashrc
COPY .devcontainer/.bashrc_custom /root/.bashrc

# Some tools
RUN apt install tig nano