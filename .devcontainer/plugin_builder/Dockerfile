FROM gradle:8.5-jdk17

# Define user parameters
ARG USERNAME=gradle

USER $USERNAME

WORKDIR /builds

# Clone, add plugin.json, then build
RUN git clone https://github.com/lavalink-devs/youtube-source.git && \
    cd youtube-source && \
    ./gradlew build