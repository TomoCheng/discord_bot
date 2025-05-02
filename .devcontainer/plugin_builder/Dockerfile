FROM gradle:8.5-jdk17 as builder

ENV YOUTUBE_PLUGIN_REPO=https://github.com/lavalink-devs/youtube-source.git

# Define user parameters
ARG USERNAME=gradle

USER $USERNAME

WORKDIR /builds

# Clone, add plugin.json, then build
RUN git clone ${YOUTUBE_PLUGIN_REPO} plugin && \
    mkdir -p plugin/src/main/resources && \
    mkdir -p plugin/src/main/resources/META-INF && \
    printf 'Manifest-Version: 1.0\nPlugin-Name: hung-plugin\nPlugin-Version: 1.0.0\nPlugin-Author: Hung Liang\nMain-Class: com.example.plugin.HungPluginMain' > plugin/src/main/resources/META-INF/MANIFEST.mf && \
    printf 'name: hung-plugin\nversion: 0.6.9\nmain: dev.lavalink.youtube.YoutubePlugin\napi-version: 4.0.0\ndescription: Provides YouTube support for Lavalink. Bababababa.\nauthor: hung liang' > plugin/src/main/resources/plugin.yml && \
    cd plugin && \
    ./gradlew build