# How to Build and Run the Jules Orchestration Container

This guide provides instructions on how to build the Docker image for the `jules.sh` orchestration script and how to run it.

## Prerequisites

- Docker must be installed on your system.

## 1. Building the Docker Image

First, you need to build the Docker image from the `Dockerfile`. This will create a self-contained environment with all the necessary dependencies.

Open your terminal, navigate to the directory containing the `Dockerfile` and `jules.sh`, and run the following command:

```bash
docker build -t jules-orchestrator .
```

This command builds a Docker image and tags it with the name `jules-orchestrator`.

## 2. Running the `jules.sh` Script

Once the image is built, you can run the `jules.sh` script using the `docker run` command. The container will execute the script and then exit.

### Basic Commands

To run a specific command from `jules.sh`, pass the command name as an argument to `docker run`.

**Example: Get the device ID**
```bash
docker run --rm jules-orchestrator device-id
```

**Example: Run the 'all' pipeline**
```bash
docker run --rm jules-orchestrator all
```

### Commands Requiring Environment Variables

Some commands, like `ddns`, require sensitive information to be passed in as environment variables. The `docker run` command supports the `-e` flag for this purpose.

**Example: Update a DuckDNS domain**

To run the `ddns` command, you need to provide your DuckDNS token via the `DUCKDNS_TOKEN` environment variable.

```bash
docker run --rm -e DUCKDNS_TOKEN="your-duckdns-token-goes-here" jules-orchestrator ddns your-subdomain
```

*   Replace `"your-duckdns-token-goes-here"` with your actual DuckDNS token.
*   Replace `your-subdomain` with the DuckDNS subdomain you want to update.

### Interactive Mode

For debugging or manual operations inside the container, you can start an interactive shell:

```bash
docker run --rm -it jules-orchestrator /bin/bash
```

This will give you a bash prompt inside the container, where you can run `./jules.sh` commands directly or inspect the environment.