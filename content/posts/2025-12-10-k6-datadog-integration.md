---
title: "k6 Metrics to Datadog via Logs, StatsD, and OTEL"
date: 2025-12-10T00:00:00Z
slug: k6-metrics-to-datadog-via-logs-statsd-and-otel
summary: "How we wired k6 to send metrics to Datadog using logs, StatsD, and OpenTelemetry, including the extra bits needed for AWS Fargate."
categories:
  - Coder's Grave
  - Home Page
tags: ["k6", "datadog", "otel", "statsd", "fargate", "load-testing"]
---

Recently we were asked to integrate k6 with Datadog and support **three** different ways of getting metrics out:

- Plain **log / file outputs** (JSON + CSV)
- **StatsD / DogStatsD**
- **OpenTelemetry (OTLP/gRPC)**

On top of that, our load tests run on **AWS Fargate**, which adds a couple of twists around networking and sidecar configuration.

This post is a walk-through of the Datadog/k6 side of that integration – **no internal k6 code**, just the environment variables and infrastructure wiring that made everything work. The goal is that you can lift these ideas into your own stack with as little friction as possible.

---

## 1. Metrics via Logs (JSON + CSV)

The lowest-friction way to get k6 metrics is to let it write them to disk and then ship or inspect them however you like.

In our setup, each run writes to a timestamped result directory, something like:

```text
/output/results/2025-12-08_12-34-56/
```

Inside that directory we keep:

- `metrics.json` – k6 metrics in JSON format
- `metrics.csv` – k6 metrics in CSV format
- `k6-dashboard.html` – exported k6 web dashboard
- `logs.jsonl` – line-delimited logs from the run

Conceptually, the runner does this:

```sh
RESULT_DIR="$(pwd)/output/results/$(date -u +%F-%H-%M-%S.%3N)"
mkdir -p "$RESULT_DIR"

./dist/k6 run \
  --log-format "${LOG_FORMAT:-raw}" \
  --log-output stdout \
  --out "json=$RESULT_DIR/metrics.json" \
  --out "csv=$RESULT_DIR/metrics.csv" \
  "$@" \
  | tee -a "$RESULT_DIR/logs.jsonl" \
   > /dev/stdout

  Key environment variables here (using neutral names for this article):
```

Key environment variables here (using neutral names for this article):

- `RESULT_DIR` – absolute path to the per-run result directory
- `LOG_FORMAT` – k6 log format (`raw` or `json`)

Even once we wired up StatsD and OTEL, we kept this file-based output path. It makes debugging and offline analysis much easier, and it gives you something to fall back on if remote transport is misbehaving.

---

## 2. Metrics via StatsD (DogStatsD)

The next integration layer is **StatsD**, specifically **DogStatsD** as implemented by the Datadog Agent.

From k6’s point of view, the essentials are:

- Use a k6 build that includes [`xk6-output-statsd`](https://github.com/LeonAdato/xk6-output-statsd) (or another StatsD output extension)
- Point it at a `host:port` where a DogStatsD-compatible server is listening


```sh
xk6 build v1.1.0
  --output dist/k6
  --with github.com/LeonAdato/xk6-output-statsd@latest
```

### 2.1 k6-side environment variables

Configure k6 directly with its StatsD settings:

- `K6_STATSD_ENABLE_TAGS=true`
  - Enables tags in StatsD metrics (DogStatsD-style tags for Datadog).
- `K6_STATSD_ADDR=<host:port>`
  - Address of the DogStatsD server (e.g. `localhost:8125`).

Add the k6 output flag:

```sh
--out output-statsd
```

Minimal example:

```sh
K6_STATSD_ENABLE_TAGS=true \
K6_STATSD_ADDR=localhost:8125 \
./k6 run --out output-statsd script.js
```

### 2.2 Datadog Agent configuration for StatsD

On the Agent side we need to:

1. Allow DogStatsD to accept traffic
2. Expose the correct ports

Key environment variables:

- `DD_DOGSTATSD_NON_LOCAL_TRAFFIC=1`
  - Allows DogStatsD to accept traffic from non-loopback interfaces (useful even in containers).

Common supporting variables:

- `DD_SITE="datadoghq.com"` (or your region-specific site)
- `DD_API_KEY=<your-api-key>`
- `DD_LOG_LEVEL="info"` (or `debug` while you’re tuning things)

Ports to expose (Docker or ECS):

- `8125/udp` – DogStatsD metrics
- `8126/tcp` – APM traces (optional for this use case)

Example Docker run for local dev:

```sh
docker run -d \
  --name datadog-agent \
  -e DD_SITE="datadoghq.com" \
  -e DD_API_KEY="$DD_API_KEY" \
  -e DD_LOG_LEVEL="info" \
  -e DD_DOGSTATSD_NON_LOCAL_TRAFFIC=1 \
  -p 8125:8125/udp \
  -p 8126:8126 \
  datadog/agent:latest
```

In ECS/CloudFormation, the same variables and ports go into the `datadog-agent` container definition.

---

## 3. Metrics via OpenTelemetry (OTLP / gRPC)

The third path is **OpenTelemetry**, using the experimental OTLP output from k6 and the Datadog Agent’s OTLP receiver.

### 3.1 k6 OTEL environment variables

Configure k6 directly with its OTLP/gRPC exporter settings:

- `K6_OTEL_GRPC_EXPORTER_ENDPOINT=<host:port>`
  - Example: `localhost:4317` (host:port only; no scheme).
- `K6_OTEL_GRPC_EXPORTER_INSECURE=true`
  - Use non-TLS for local/sidecar setups.
- `K6_OTEL_METRIC_PREFIX="k6."`
  - Prefix for exported metric names.
- `K6_OTEL_FLUSH_INTERVAL="1s"`
  - Flush frequency for metrics.
- `K6_OTEL_SERVICE_NAME=<service-name>`
- `K6_OTEL_SERVICE_VERSION=<version>`

Add the k6 output flag:

```sh
--out experimental-opentelemetry
```

Minimal example:

```sh
K6_OTEL_GRPC_EXPORTER_ENDPOINT=localhost:4317 \
K6_OTEL_GRPC_EXPORTER_INSECURE=true \
K6_OTEL_METRIC_PREFIX="k6." \
K6_OTEL_FLUSH_INTERVAL="1s" \
K6_OTEL_SERVICE_NAME="load-tests" \
K6_OTEL_SERVICE_VERSION="1.0.0" \
./k6 run --out experimental-opentelemetry script.js
```

### 3.2 Datadog Agent environment for OTLP

Enable the Datadog Agent’s OTLP receivers and expose the ports:

- `DD_OTLP_CONFIG_ENABLE="true"`
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC="true"`
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP="true"`
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_ENDPOINT="0.0.0.0:4317"`
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP_ENDPOINT="0.0.0.0:4318"`

Tuning for larger runs:

- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_MAX_RECV_MSG_SIZE_MIB="32"`
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_MAX_CONCURRENT_STREAMS="100"`

Common Agent variables:

- `DD_SITE="datadoghq.com"`
- `DD_API_KEY=<your-api-key>`
- `DD_LOG_LEVEL="info"`

Ports to expose:

- `4317/tcp` – OTLP/gRPC
- `4318/tcp` – OTLP/HTTP

Example Docker run for local dev:

```sh
docker run -d \
  --name datadog-agent \
  -e DD_SITE="datadoghq.com" \
  -e DD_API_KEY="$DD_API_KEY" \
  -e DD_LOG_LEVEL="info" \
  -e DD_OTLP_CONFIG_ENABLE="true" \
  -e DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC="true" \
  -e DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP="true" \
  -e DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_ENDPOINT="0.0.0.0:4317" \
  -e DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP_ENDPOINT="0.0.0.0:4318" \
  -e DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_MAX_RECV_MSG_SIZE_MIB="32" \
  -e DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_MAX_CONCURRENT_STREAMS="100" \
  -p 4317:4317/tcp \
  -p 4318:4318/tcp \
  datadog/agent:latest
```

### 3.3 Datadog Agent environment for OTLP

The Datadog Agent needs to be explicitly told to accept OTLP.

In **local Docker** examples you may see env vars like `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_ENABLED`. In **our Fargate stack**, the authoritative set is the one below (taken directly from the task definition in `devops/load-test/cloudformation/env-stack.basic.yaml`).

Essential variables (matching Fargate):

- `DD_OTLP_CONFIG_ENABLE="true"`
  - Master switch to enable OTLP in the Agent.
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC="true"`
  - Turn on the OTLP/gRPC receiver.
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP="true"`
  - Turn on the OTLP/HTTP receiver.
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_ENDPOINT="0.0.0.0:4317"`
  - Where the Agent listens for OTLP/gRPC.
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP_ENDPOINT="0.0.0.0:4318"`
  - Where the Agent listens for OTLP/HTTP.

For heavier test runs, we also increase the defaults (again, exactly as in the stack):

- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_MAX_RECV_MSG_SIZE_MIB="32"`
  - Max gRPC message size (MiB). k6 can generate large metric payloads.
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_MAX_CONCURRENT_STREAMS="100"`
  - Concurrency for high-throughput cases.

Plus the standard Agent env vars used in the same Fargate task:

- `DD_SITE="datadoghq.com"`
- `DD_API_KEY=<your-api-key>`
- `DD_LOG_LEVEL="info"`
- `ECS_FARGATE="true"`
- `DD_LOGS_ENABLED="true"`
- `DD_DOGSTATSD_NON_LOCAL_TRAFFIC="1"`

Ports to expose:

- `4317/tcp` – OTLP/gRPC
- `4318/tcp` – OTLP/HTTP
- `8125/udp` – DogStatsD
- `8126/tcp` – APM (optional)

If you want to run the same thing locally with `docker run`, keep **the same variable names and values**; just translate them from the CloudFormation snippet into `-e` flags. The crucial part is that the env var set matches what we actually deploy in Fargate, otherwise the Agent will not accept the OTLP traffic from k6.

---

## 4. AWS Fargate Particularities

The interesting part of this integration is that our tests run as an **ECS Task on Fargate**, with **two containers** in the same task:

- `load-generator` – runs k6
- `datadog-agent` – runs the Datadog Agent

Here are the non-obvious pieces that mattered.

### 4.1 Network mode and addressing

Our task definition uses:

```yaml
NetworkMode: awsvpc
RequiresCompatibilities:
  - FARGATE
```

In `awsvpc` mode (which is mandatory for Fargate):

- The **task** gets an ENI and its own IP.
- All containers in the task share that network namespace.
- Containers talk to each other via **`localhost`**, not by container name.

So from the k6 container, the Datadog Agent is reachable at:

- `localhost:8125` for DogStatsD
- `localhost:4317` for OTLP/gRPC

### 4.2 Task definition sketch (exact env from `env-stack.basic.yaml`)

A stripped-down version of the task definition (with the **real** Datadog Agent env vars we use) looks like this:

```yaml
Resources:
  LoadTestTaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: !Sub LoadTestTask
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      Cpu: '4096'
      Memory: '30720'
      ExecutionRoleArn: !Ref ExecutionRoleArn
      TaskRoleArn: !Ref TaskRoleArn
      ContainerDefinitions:
        - Name: load-generator
          DependsOn:
            - ContainerName: datadog-agent
              Condition: START
          Image: !Sub ${EcrRepositoryUri}:${DockerTag}
          User: k6
          Command: ['src/main.ts']
          WorkingDirectory: /home/k6/scripts
          Environment:
            - Name: S3_BUCKET_NAME
              Value: !Ref LoadTestBucket
            - Name: K6_STATSD_ENABLE_TAGS
              Value: 'true'
            - Name: K6_STATSD_ADDR
              Value: 'localhost:8125'
            - Name: K6_OTEL_GRPC_EXPORTER_ENDPOINT
              Value: 'localhost:4317'
            - Name: K6_OTEL_GRPC_EXPORTER_INSECURE
              Value: 'true'
            - Name: K6_OTEL_METRIC_PREFIX
              Value: 'k6.'
            - Name: K6_OTEL_FLUSH_INTERVAL
              Value: '1s'
            - Name: K6_OTEL_SERVICE_NAME
              Value: 'load-tests'
            - Name: K6_OTEL_SERVICE_VERSION
              Value: '1.0.0'
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroupName
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: loadtest

        - Name: datadog-agent
          Essential: true
          Image: 'public.ecr.aws/datadog/agent:latest'
          PortMappings:
            - ContainerPort: 4317
              Protocol: tcp
            - ContainerPort: 4318
              Protocol: tcp
            - ContainerPort: 8125
              Protocol: udp
            - ContainerPort: 8126
              Protocol: tcp
          Environment:
            - Name: DD_SITE
              Value: datadoghq.com
            - Name: DD_API_KEY
              Value: !Sub ${DatadogApiKey}
            - Name: DD_LOG_LEVEL
              Value: info
            - Name: ECS_FARGATE
              Value: 'true'
            - Name: DD_LOGS_ENABLED
              Value: 'true'
            - Name: DD_OTLP_CONFIG_ENABLE
              Value: 'true'
            - Name: DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC
              Value: 'true'
            - Name: DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP
              Value: 'true'
            - Name: DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_ENDPOINT
              Value: '0.0.0.0:4317'
            - Name: DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP_ENDPOINT
              Value: '0.0.0.0:4318'
            - Name: DD_DOGSTATSD_NON_LOCAL_TRAFFIC
              Value: '1'
            - Name: DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_MAX_RECV_MSG_SIZE_MIB
              Value: '32'
            - Name: DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_MAX_CONCURRENT_STREAMS
              Value: '100'
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroupName
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: datadog-agent
```

A few notes:

- `ECS_FARGATE=true` helps the Agent recognize it’s on Fargate.
- We don’t mount Docker sockets or host `/proc`/cgroups – that’s fine for this use-case where we only care about k6 → Agent metrics.
- Ports are defined per container; since the task has a single IP, `localhost:<port>` works from the k6 container.

If you want to be extra careful about ordering, you can add a `DependsOn` from `load-generator` to `datadog-agent` with `Condition: START`, but in practice OTLP and DogStatsD both behave reasonably with a few initial connection retries.

---

## 5. Summary Cheat Sheet

Here’s a compact checklist you can use when wiring this up elsewhere.

### k6 / Runner environment

- **Logs / Files**
  - `RESULT_DIR` – absolute path to result directory
  - `LOG_FORMAT` – `raw` or `json`

- **StatsD (DogStatsD)**
  - `STATSD_ENDPOINT=host:port` (e.g. `localhost:8125`)
  - Derived:
    - `K6_STATSD_ENABLE_TAGS=true`
    - `K6_STATSD_ADDR=$STATSD_ENDPOINT`
    - `--out output-statsd`

- **OpenTelemetry (OTLP/gRPC)**
  - `OTEL_ENDPOINT=host:port` (e.g. `localhost:4317`)
  - Derived:
    - `K6_OTEL_GRPC_EXPORTER_ENDPOINT=$OTEL_ENDPOINT`
    - `K6_OTEL_GRPC_EXPORTER_INSECURE=true`
    - `K6_OTEL_METRIC_PREFIX="k6."`
    - `K6_OTEL_FLUSH_INTERVAL="1s"`
    - `K6_OTEL_SERVICE_NAME=<service-name>`
    - `K6_OTEL_SERVICE_VERSION=<version>`
    - `--out experimental-opentelemetry`

### Datadog Agent (common)

- `DD_SITE="datadoghq.com"`
- `DD_API_KEY=<your-api-key>`
- `DD_LOG_LEVEL="info"`

### Datadog Agent (StatsD)

- `DD_DOGSTATSD_NON_LOCAL_TRAFFIC=1`
- Ports:
  - `8125/udp`
  - `8126/tcp`

### Datadog Agent (OTLP)

- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_ENABLED="true"`
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_ENDPOINT="0.0.0.0:4317"`
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP_ENDPOINT="0.0.0.0:4318"`
- `DD_OTLP_CONFIG_LOGS_ENABLED="true"`
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_MAX_RECV_MSG_SIZE_MIB="32"`
- `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_MAX_CONCURRENT_STREAMS="100"`
- Ports:
  - `4317/tcp`
  - `4318/tcp`

### Fargate-specific

- Task definition:
  - `NetworkMode: awsvpc`
  - `RequiresCompatibilities: [FARGATE]`
- Datadog Agent container:
  - `ECS_FARGATE=true`
  - Env + ports as above
- k6 container:
  - Use `localhost:<port>` for both StatsD and OTLP endpoints

If you keep those pieces aligned, you get a nice, flexible setup: k6 writes local artifacts (JSON/CSV/logs), pushes real-time metrics to Datadog via StatsD and/or OTEL, and the whole thing runs happily on Fargate.
