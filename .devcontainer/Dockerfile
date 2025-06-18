FROM qmcgaw/latexdevcontainer:latest-full
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends make
RUN addgroup --gid 1000 vscode
RUN adduser --disabled-password --gecos "" --uid 1000 --gid 1000 vscode
ENV HOME=/home/vscode
USER vscode
RUN touch /home/vscode/.zshrc
