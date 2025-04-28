FROM python:3.12-slim

RUN apt-get update && apt-get install -y sudo git \
    ipmitool \
    openssl 

RUN rm -rf /var/lib/apt/lists/*

# Define user parameters
ARG USERNAME=dev_user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user and group (don't switch user yet)
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Now, switch to the dev_user after creation
USER $USERNAME

WORKDIR /workspaces

RUN pip install discord.py==2.5.2 python-dotenv==1.1.0 pytube==7.0.16 requests==2.32.3 youtube-search==2.1.2