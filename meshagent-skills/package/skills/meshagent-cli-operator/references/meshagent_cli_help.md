# MeshAgent CLI Help

_Packaged CLI help reference for MeshAgent CLI `0.34.0`._

_Generated from the installed `meshagent` binary with recursive `--help` capture up to depth 1 and timeout 2s per command._

## `meshagent`

```console
$ meshagent --help
                                                                                
 Usage: meshagent [OPTIONS] COMMAND [ARGS]...                                   
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ version              Print the version                                       │
│ setup                Perform initial login and project/api key activation.   │
│ call                 Trigger agent/tool calls via URL                        │
│ auth                 Authenticate to meshagent                               │
│ project              Manage or activate your meshagent projects              │
│ api-key              Manage or activate api-keys for your project            │
│ session              Inspect recent sessions and events                      │
│ token                Generate participant tokens (JWTs)                      │
│ webhook              Manage project webhooks                                 │
│ service              Manage services for your project                        │
│ mcp                  Bridge MCP servers into MeshAgent rooms                 │
│ secret               Manage secrets for your project.                        │
│ helper               Developer helper services                               │
│ rooms                Create, list, and manage rooms in a project             │
│ mailbox              Manage mailboxes for your project                       │
│ route                Manage routes for your project                          │
│ scheduled-task       Manage scheduled tasks for your project                 │
│ meeting-transcriber  Join a meeting transcriber to a room                    │
│ port                 Port forwarding into room containers                    │
│ webserver            Run an HTTP webserver connected to a MeshAgent room.    │
│ codex                Codex-backed agents                                     │
│ multi                Connect agents and tools to a room                      │
│ voicebot             Join a voicebot to a room                               │
│ chatbot              Join a chatbot to a room                                │
│ process              Join a process-backed agent to a room                   │
│ mailbot              Join a mailbot to a room                                │
│ task-runner          Join a taskrunner to a room                             │
│ worker               Join a worker agent to a room                           │
│ room                 Operate within a room                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent api-key`

```console
$ meshagent api-key --help
                                                                                
 Usage: meshagent api-key [OPTIONS] COMMAND [ARGS]...                           
                                                                                
 Manage or activate api-keys for your project                                   
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ list      List API keys for a project.                                       │
│ create    Create a new API key for a project.                                │
│ activate  Set the default API key for a project in local CLI settings.       │
│ delete    Delete an API key from a project.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent api-key create`

```console
$ meshagent api-key create --help
                                                                                
 Usage: meshagent api-key create [OPTIONS] NAME                                 
                                                                                
 Create a new API key for a project.                                            
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    name      TEXT  [required]                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id                      TEXT  A MeshAgent project id. If empty,    │
│                                         the activated project will be used.  │
│                                         [default:                            │
│                                         203b1bf9-72c9-4022-bfaa-55d6f656dfe… │
│ --description                     TEXT  a description for the api key        │
│ --activate       --no-activate          use this key by default for commands │
│                                         that accept an API key               │
│                                         [default: no-activate]               │
│ --silent         --no-silent            do not print api key                 │
│                                         [default: no-silent]                 │
│ --help                                  Show this message and exit.          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent auth`

```console
$ meshagent auth --help
                                                                                
 Usage: meshagent auth [OPTIONS] COMMAND [ARGS]...                              
                                                                                
 Authenticate to meshagent                                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ login                                                                        │
│ logout                                                                       │
│ whoami                                                                       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent auth whoami`

```console
$ meshagent auth whoami --help
                                                                                
 Usage: meshagent auth whoami [OPTIONS]                                         
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent call`

```console
$ meshagent call --help
                                                                                
 Usage: meshagent call [OPTIONS] COMMAND [ARGS]...                              
                                                                                
 Trigger agent/tool calls via URL                                               
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ tool     Send a call request to a tool webhook URL                           │
│ agent    Send a call request to an agent webhook URL                         │
│ toolkit  Send a call request to a toolkit webhook URL                        │
│ schema   Send a call request to a schema webhook URL                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent chatbot`

```console
$ meshagent chatbot --help
                                                                                
 Usage: meshagent chatbot [OPTIONS] COMMAND [ARGS]...                           
                                                                                
 Join a chatbot to a room                                                       
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ join     Join a room and run a chatbot agent.                                │
│ service                                                                      │
│ spec     Generate a service spec for deploying a chatbot.                    │
│ deploy   Deploy a chatbot service to a project or room.                      │
│ run      Join a room, run the chatbot, and wait for messages.                │
│ use      Send a one-shot or interactive message to a running chatbot.        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent codex`

```console
$ meshagent codex --help
                                                                                
 Usage: meshagent codex [OPTIONS] COMMAND [ARGS]...                             
                                                                                
 Codex-backed agents                                                            
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ chatbot      Run codex chatbot agents                                        │
│ task-runner  Run codex task-runner agents                                    │
│ worker       Run codex worker agents                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent helper`

```console
$ meshagent helper --help
                                                                                
 Usage: meshagent helper [OPTIONS] COMMAND [ARGS]...                            
                                                                                
 Developer helper services                                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ service  Run local helper HTTP services                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent mailbot`

```console
$ meshagent mailbot --help
                                                                                
 Usage: meshagent mailbot [OPTIONS] COMMAND [ARGS]...                           
                                                                                
 Join a mailbot to a room                                                       
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ join     Join a room and run a mailbot agent.                                │
│ service                                                                      │
│ spec     Generate a service spec for deploying a mailbot.                    │
│ deploy   Deploy a mailbot service to a project or room.                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent mailbot spec`

```console
$ meshagent mailbot spec --help
                                                                                
 Usage: meshagent mailbot spec [OPTIONS]                                        
                                                                                
 Generate a service spec for deploying a mailbot.                               
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --service-name                                  TEXT  service name        │
│    --service-descrip…                              TEXT  service description │
│    --service-title                                 TEXT  a display name for  │
│                                                          the service         │
│ *  --agent-name                                    TEXT  Name of the agent   │
│                                                          to call             │
│                                                          [required]          │
│    --rule              -r                          TEXT  a system rule       │
│    --rules-file                                    TEXT                      │
│    --require-toolkit   -rt                         TEXT  the name or url of  │
│                                                          a required toolkit  │
│    --require-schema    -rs                         TEXT  the name or url of  │
│                                                          a required schema   │
│    --model                                         TEXT  Name of the LLM     │
│                                                          model to use for    │
│                                                          the chatbot         │
│                                                          [default: gpt-5.4]  │
│    --require-shell          --no-require-shell           Enable function     │
│                                                          shell tool calling  │
│                                                          [default:           │
│                                                          no-require-shell]   │
│    --require-local-s…       --no-require-local…          Enable local shell  │
│                                                          tool calling        │
│                                                          [default:           │
│                                                          no-require-local-s… │
│    --require-web-sea…       --no-require-web-s…          Enable web search   │
│                                                          tool calling        │
│                                                          [default:           │
│                                                          no-require-web-sea… │
│    --require-web-fet…       --no-require-web-f…          Enable web fetch    │
│                                                          tool calling        │
│                                                          [default:           │
│                                                          no-require-web-fet… │
│    --discover-script…       --no-discover-scri…          Automatically add   │
│                                                          script tools from   │
│                                                          the room            │
│                                                          [default:           │
│                                                          no-discover-script… │
│    --require-apply-p…       --no-require-apply…          Enable apply patch  │
│                                                          tool calling        │
│                                                          [default:           │
│                                                          no-require-apply-p… │
│    --queue                                         TEXT  the name of the     │
│                                                          mail queue          │
│ *  --email-address                                 TEXT  the email address   │
│                                                          of the agent        │
│                                                          [required]          │
│    --toolkit-name                                  TEXT  the name of a       │
│                                                          toolkit to expose   │
│                                                          mail operations     │
│    --room-rules        -rr                         TEXT  a path to a rules   │
│                                                          file within the     │
│                                                          room that can be    │
│                                                          used to customize   │
│                                                          the agent's         │
│                                                          behavior            │
│    --whitelist                                     TEXT  an email to         │
│                                                          whitelist           │
│    --require-storage        --no-require-stora…          Enable storage      │
│                                                          toolkit             │
│                                                          [default:           │
│                                                          no-require-storage] │
│    --require-read-on…       --no-require-read-…          Enable read only    │
│                                                          storage toolkit     │
│                                                          [default:           │
│                                                          no-require-read-on… │
│    --storage-tool-lo…                              TEXT  Mount local path as │
│                                                          <source>:<mount>[:… │
│    --storage-tool-ro…                              TEXT  Mount room path as  │
│                                                          <source>:<mount>[:… │
│    --shell-room-mount                              TEXT  Mount room storage  │
│                                                          as                  │
│                                                          <source>:<mount>[:… │
│    --shell-project-m…                              TEXT  Mount project       │
│                                                          storage as          │
│                                                          <source>:<mount>[:… │
│    --shell-empty-dir…                              TEXT  Mount empty dir at  │
│                                                          <mount>[:ro|rw]     │
│    --shell-image-mou…                              TEXT  Mount image as      │
│                                                          <image>=<mount>[:r… │
│    --require-time           --no-require-time            Enable              │
│                                                          time/datetime tools │
│                                                          [default:           │
│                                                          require-time]       │
│    --require-uuid           --no-require-uuid            Enable UUID         │
│                                                          generation tools    │
│                                                          [default:           │
│                                                          no-require-uuid]    │
│    --use-memory                                    TEXT  Use memories        │
│                                                          toolkit for <name>  │
│                                                          or                  │
│                                                          <namespace>/<name>  │
│    --memory-model                                  TEXT  Model name for      │
│                                                          memory LLM          │
│                                                          ingestion           │
│    --database-namesp…                              TEXT  Use a specific      │
│                                                          database namespace  │
│    --require-table-r…                              TEXT  Enable table read   │
│                                                          tools for a         │
│                                                          specific table      │
│    --require-table-w…                              TEXT  Enable table write  │
│                                                          tools for a         │
│                                                          specific table      │
│    --require-compute…       --no-require-compu…          Enable computer use │
│                                                          [default:           │
│                                                          no-require-compute… │
│    --starting-url                                  TEXT  Initial URL to open │
│                                                          when starting a     │
│                                                          computer-use        │
│                                                          browser session     │
│    --allow-goto-url                                      Expose the goto URL │
│                                                          helper tool for     │
│                                                          computer use        │
│    --reply-all              --no-reply-all               Reply-all when      │
│                                                          responding to       │
│                                                          emails              │
│                                                          [default:           │
│                                                          no-reply-all]       │
│    --enable-attachme…       --no-enable-attach…          Allow downloading   │
│                                                          and processing      │
│                                                          email attachments   │
│                                                          [default:           │
│                                                          no-enable-attachme… │
│    --working-dir                                   TEXT  The default working │
│                                                          directory for shell │
│                                                          commands            │
│    --skill-dir                                     TEXT  an agent skills     │
│                                                          directory           │
│    --llm-participant                               TEXT  Delegate LLM        │
│                                                          interactions to a   │
│                                                          remote participant  │
│    --shell-image                                   TEXT  an image tag to use │
│                                                          to run shell        │
│                                                          commands in         │
│    --delegate-shell-…       --no-delegate-shel…          Delegate the room   │
│                                                          token to shell      │
│                                                          tools               │
│                                                          [default:           │
│                                                          no-delegate-shell-… │
│    --shell-copy-env                                TEXT  Copy local env vars │
│                                                          into shell tool     │
│                                                          env. Accepts        │
│                                                          comma-separated     │
│                                                          names and can be    │
│                                                          repeated.           │
│    --shell-set-env                                 TEXT  Set env vars in     │
│                                                          shell tool env as   │
│                                                          NAME=VALUE. Can be  │
│                                                          repeated.           │
│    --log-llm-requests       --no-log-llm-reque…          log all requests to │
│                                                          the llm             │
│                                                          [default:           │
│                                                          no-log-llm-request… │
│    --help                                                Show this message   │
│                                                          and exit.           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent mailbox`

```console
$ meshagent mailbox --help
                                                                                
 Usage: meshagent mailbox [OPTIONS] COMMAND [ARGS]...                           
                                                                                
 Manage mailboxes for your project                                              
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ create  Create a mailbox attached to the project.                            │
│ update  Update a mailbox routing configuration.                              │
│ show    Show mailbox details.                                                │
│ list    List mailboxes for the project.                                      │
│ delete  Delete a mailbox.                                                    │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent mailbox create`

```console
$ meshagent mailbox create --help
                                                                                
 Usage: meshagent mailbox create [OPTIONS]                                      
                                                                                
 Create a mailbox attached to the project.                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id           TEXT  A MeshAgent project id. If empty, the        │
│                                 activated project will be used.              │
│                                 [default:                                    │
│                                 203b1bf9-72c9-4022-bfaa-55d6f656dfeb]        │
│ *  --address      -a      TEXT  Mailbox email address (unique per project)   │
│                                 [required]                                   │
│    --room                 TEXT  Room name                                    │
│ *  --queue        -q      TEXT  Queue name to deliver inbound messages to    │
│                                 [required]                                   │
│    --public                     Queue name to deliver inbound messages to    │
│    --annotations  -n      TEXT  annotations in json format {"name":"value"}  │
│    --help                       Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent mailbox delete`

```console
$ meshagent mailbox delete --help
                                                                                
 Usage: meshagent mailbox delete [OPTIONS] ADDRESS                              
                                                                                
 Delete a mailbox.                                                              
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    address      TEXT  Mailbox address to delete [required]                 │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id        TEXT  A MeshAgent project id. If empty, the activated    │
│                           project will be used.                              │
│                           [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb]    │
│ --help                    Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent mailbox list`

```console
$ meshagent mailbox list --help
                                                                                
 Usage: meshagent mailbox list [OPTIONS]                                        
                                                                                
 List mailboxes for the project.                                                
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id          TEXT  A MeshAgent project id. If empty, the activated  │
│                             project will be used.                            │
│                             [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb]  │
│ --room                TEXT  Room name                                        │
│ --output      -o      TEXT  output format  [default: table]                  │
│ --help                      Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent mailbox show`

```console
$ meshagent mailbox show --help
                                                                                
 Usage: meshagent mailbox show [OPTIONS] ADDRESS                                
                                                                                
 Show mailbox details.                                                          
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    address      TEXT  Mailbox address to show [required]                   │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id        TEXT  A MeshAgent project id. If empty, the activated    │
│                           project will be used.                              │
│                           [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb]    │
│ --help                    Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent mailbox update`

```console
$ meshagent mailbox update --help
                                                                                
 Usage: meshagent mailbox update [OPTIONS] ADDRESS                              
                                                                                
 Update a mailbox routing configuration.                                        
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    address      TEXT  Mailbox email address to update [required]           │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id           TEXT  A MeshAgent project id. If empty, the activated │
│                              project will be used.                           │
│                              [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb] │
│ --room         -r      TEXT  Room name to route inbound mail into            │
│ --queue        -q      TEXT  Queue name to deliver inbound messages to       │
│ --public                     Queue name to deliver inbound messages to       │
│ --annotations  -n      TEXT  annotations in json format {"name":"value"}     │
│ --help                       Show this message and exit.                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent mcp`

```console
$ meshagent mcp --help
                                                                                
 Usage: meshagent mcp [OPTIONS] COMMAND [ARGS]...                               
                                                                                
 Bridge MCP servers into MeshAgent rooms                                        
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ sse            Connect an MCP server over SSE and register it as a toolkit   │
│ http           Connect an MCP server over streamable HTTP and register it as │
│                a toolkit                                                     │
│ stdio          Run an MCP server over stdio and register it as a toolkit     │
│ http-proxy     Expose a stdio MCP server over streamable HTTP                │
│ sse-proxy      Expose a stdio MCP server over SSE                            │
│ stdio-service  Run a stdio MCP server as an HTTP service                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent meeting-transcriber`

```console
$ meshagent meeting-transcriber --help
                                                                                
 Usage: meshagent meeting-transcriber [OPTIONS] COMMAND [ARGS]...               
                                                                                
 Join a meeting transcriber to a room                                           
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ join     Join a room and run the meeting transcriber agent.                  │
│ service                                                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent port`

```console
$ meshagent port --help
                                                                                
 Usage: meshagent port [OPTIONS] COMMAND [ARGS]...                              
                                                                                
 Port forwarding into room containers                                           
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ forward  Forward a container port to localhost                               │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent port forward`

```console
$ meshagent port forward --help
                                                                                
 Usage: meshagent port forward [OPTIONS]                                        
                                                                                
 Forward a container port to localhost                                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id            TEXT  A MeshAgent project id. If empty, the       │
│                                  activated project will be used.             │
│                                  [default:                                   │
│                                  203b1bf9-72c9-4022-bfaa-55d6f656dfeb]       │
│ *  --room          -r      TEXT  Room name containing the target container   │
│                                  [required]                                  │
│    --name          -n      TEXT  Container name to port-forward into         │
│    --container-id  -c      TEXT  Container ID to port-forward into           │
│ *  --port          -p      TEXT  Port mapping in the form LOCAL:REMOTE       │
│                                  [required]                                  │
│    --help                        Show this message and exit.                 │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent process`

```console
$ meshagent process --help
                                                                                
 Usage: meshagent process [OPTIONS] COMMAND [ARGS]...                           
                                                                                
 Join a process-backed agent to a room                                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ join     Join a room and run a process-backed agent.                         │
│ service  Add a process-backed agent service to the host.                     │
│ spec     Generate a service spec for deploying a process-backed agent.       │
│ deploy   Deploy a process-backed agent service.                              │
│ run      Join a room, run a process-backed agent, and wait for messages.     │
│ use      Send a one-shot or interactive message to a running process-backed  │
│          agent.                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent process join`

```console
$ meshagent process join --help
                                                                                
 Usage: meshagent process join [OPTIONS]                                        
                                                                                
 Join a room and run a process-backed agent.                                    
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id                             TEXT            A MeshAgent      │
│                                                             project id. If   │
│                                                             empty, the       │
│                                                             activated        │
│                                                             project will be  │
│                                                             used.            │
│                                                             [default:        │
│                                                             203b1bf9-72c9-4… │
│ *  --room                                   TEXT            Room name        │
│                                                             [required]       │
│    --role                                   TEXT            [default: agent] │
│    --agent-name                             TEXT            Name of the      │
│                                                             agent to call    │
│    --token-from-e…                          TEXT            Name of          │
│                                                             environment      │
│                                                             variable         │
│                                                             containing a     │
│                                                             MeshAgent token  │
│    --rule           -r                      TEXT            a system rule    │
│    --room-rules     -rr                     TEXT            a path to a      │
│                                                             rules file       │
│                                                             within the room  │
│                                                             that can be used │
│                                                             to customize the │
│                                                             agent's behavior │
│    --rules-file                             TEXT                             │
│    --require-tool…  -rt                     TEXT            the name or url  │
│                                                             of a required    │
│                                                             toolkit          │
│    --require-sche…  -rs                     TEXT            the name or url  │
│                                                             of a required    │
│                                                             schema           │
│    --model                                  TEXT            Name of the LLM  │
│                                                             model to use for │
│                                                             the chatbot      │
│                                                             [default:        │
│                                                             gpt-5.4]         │
│    --image-genera…                          TEXT            Name of an image │
│                                                             gen model        │
│    --computer-use        --no-computer-…                    Enable computer  │
│                                                             use              │
│                                                             [default:        │
│                                                             no-computer-use] │
│    --local-shell         --no-local-she…                    Enable local     │
│                                                             shell tool       │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-local-shell]  │
│    --shell               --no-shell                         Enable function  │
│                                                             shell tool       │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-shell]        │
│    --apply-patch         --no-apply-pat…                    Enable apply     │
│                                                             patch tool       │
│                                                             [default:        │
│                                                             no-apply-patch]  │
│    --web-search          --no-web-search                    Enable web       │
│                                                             search tool      │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-web-search]   │
│    --web-fetch           --no-web-fetch                     Enable web fetch │
│                                                             tool calling     │
│                                                             [default:        │
│                                                             no-web-fetch]    │
│    --script-tool         --no-script-to…                    Enable script    │
│                                                             tool calling     │
│                                                             [default:        │
│                                                             no-script-tool]  │
│    --discover-scr…       --no-discover-…                    Automatically    │
│                                                             add script tools │
│                                                             from the room    │
│                                                             [default:        │
│                                                             no-discover-scr… │
│    --mcp                 --no-mcp                           Enable mcp tool  │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-mcp]          │
│    --storage             --no-storage                       Enable storage   │
│                                                             toolkit          │
│                                                             [default:        │
│                                                             no-storage]      │
│    --storage-tool…                          TEXT            Mount local path │
│                                                             as               │
│                                                             <source>:<mount… │
│    --storage-tool…                          TEXT            Mount room path  │
│                                                             as               │
│                                                             <source>:<mount… │
│    --shell-room-m…                          TEXT            Mount room       │
│                                                             storage as       │
│                                                             <source>:<mount… │
│    --shell-projec…                          TEXT            Mount project    │
│                                                             storage as       │
│                                                             <source>:<mount… │
│    --shell-empty-…                          TEXT            Mount empty dir  │
│                                                             at               │
│                                                             <mount>[:ro|rw]  │
│    --shell-image-…                          TEXT            Mount image as   │
│                                                             <image>=<mount>… │
│    --require-imag…                          TEXT            Name of an image │
│                                                             gen model        │
│    --starting-url                           TEXT            Initial URL to   │
│                                                             open when        │
│                                                             starting a       │
│                                                             computer-use     │
│                                                             browser session  │
│    --allow-goto-u…                                          Expose the goto  │
│                                                             URL helper tool  │
│                                                             for computer use │
│    --require-loca…       --no-require-l…                    Enable local     │
│                                                             shell tool       │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-require-loca… │
│    --require-shell       --no-require-s…                    Enable function  │
│                                                             shell tool       │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-require-shel… │
│    --require-appl…       --no-require-a…                    Enable apply     │
│                                                             patch tool       │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-require-appl… │
│    --require-web-…       --no-require-w…                    Enable web       │
│                                                             search tool      │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-require-web-… │
│    --require-web-…       --no-require-w…                    Enable web fetch │
│                                                             tool calling     │
│                                                             [default:        │
│                                                             no-require-web-… │
│    --require-mcp         --no-require-m…                    Enable mcp tool  │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-require-mcp]  │
│    --require-stor…       --no-require-s…                    Enable storage   │
│                                                             toolkit          │
│                                                             [default:        │
│                                                             no-require-stor… │
│    --database-nam…                          TEXT            Use a specific   │
│                                                             database         │
│                                                             namespace        │
│    --require-tabl…                          TEXT            Enable table     │
│                                                             read tools for a │
│                                                             specific table   │
│    --require-tabl…                          TEXT            Enable table     │
│                                                             write tools for  │
│                                                             a specific table │
│    --require-read…       --no-require-r…                    Enable read only │
│                                                             storage toolkit  │
│                                                             [default:        │
│                                                             no-require-read… │
│    --require-time        --no-require-t…                    Enable           │
│                                                             time/datetime    │
│                                                             tools            │
│                                                             [default:        │
│                                                             require-time]    │
│    --require-uuid        --no-require-u…                    Enable UUID      │
│                                                             generation tools │
│                                                             [default:        │
│                                                             no-require-uuid] │
│    --use-memory                             TEXT            Use memories     │
│                                                             toolkit for      │
│                                                             <name> or        │
│                                                             <namespace>/<na… │
│    --memory-model                           TEXT            Model name for   │
│                                                             memory LLM       │
│                                                             ingestion        │
│    --require-docu…       --no-require-d…                    Enable           │
│                                                             MeshDocument     │
│                                                             authoring        │
│                                                             [default:        │
│                                                             no-require-docu… │
│    --require-disc…       --no-require-d…                    Enable discovery │
│                                                             of agents and    │
│                                                             tools            │
│                                                             [default:        │
│                                                             no-require-disc… │
│    --working-dir                            TEXT            The default      │
│                                                             working          │
│                                                             directory for    │
│                                                             shell commands   │
│    --key                                    TEXT            an api key to    │
│                                                             sign the token   │
│                                                             with             │
│    --llm-particip…                          TEXT            Delegate LLM     │
│                                                             interactions to  │
│                                                             a remote         │
│                                                             participant      │
│    --decision-mod…                          TEXT            Model used for   │
│                                                             thread naming    │
│                                                             and other        │
│                                                             secondary LLM    │
│                                                             decisions        │
│    --host                                   TEXT            Host to bind the │
│                                                             service on       │
│    --port                                   INTEGER         Port to bind the │
│                                                             service on       │
│    --path                                   TEXT            HTTP path to     │
│                                                             mount the        │
│                                                             service at       │
│    --always-reply        --no-always-re…                    Always reply     │
│    --threading-mo…                          [none|default-  Threading mode   │
│                                             new]            for thread UIs.  │
│                                                             Use              │
│                                                             'default-new' to │
│                                                             show a           │
│                                                             new-thread       │
│                                                             composer before  │
│                                                             loading a        │
│                                                             thread.          │
│                                                             [default: none]  │
│    --thread-dir                             TEXT            Thread directory │
│                                                             for agent thread │
│                                                             files. Defaults  │
│                                                             to               │
│                                                             .threads/<agent… │
│                                                             when not         │
│                                                             provided.        │
│    --channel                                TEXT            Attach a channel │
│                                                             to the agent     │
│                                                             process. Can be  │
│                                                             repeated.        │
│                                                             Currently        │
│                                                             supported: chat, │
│                                                             mail:EMAIL_ADDR… │
│                                                             queue:QUEUE_NAM… │
│                                                             toolkit:NAME.    │
│    --skill-dir                              TEXT            an agent skills  │
│                                                             directory        │
│    --shell-image                            TEXT            an image tag to  │
│                                                             use to run shell │
│                                                             commands in      │
│    --delegate-she…       --no-delegate-…                    log all requests │
│                                                             to the llm       │
│                                                             [default:        │
│                                                             no-delegate-she… │
│    --shell-copy-e…                          TEXT            Copy local env   │
│                                                             vars into shell  │
│                                                             tool env.        │
│                                                             Accepts          │
│                                                             comma-separated  │
│                                                             names and can be │
│                                                             repeated.        │
│    --shell-set-env                          TEXT            Set env vars in  │
│                                                             shell tool env   │
│                                                             as NAME=VALUE.   │
│                                                             Can be repeated. │
│    --log-llm-requ…       --no-log-llm-r…                    log all requests │
│                                                             to the llm       │
│                                                             [default:        │
│                                                             no-log-llm-requ… │
│    --help                                                   Show this        │
│                                                             message and      │
│                                                             exit.            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent process spec`

```console
$ meshagent process spec --help
                                                                                
 Usage: meshagent process spec [OPTIONS]                                        
                                                                                
 Generate a service spec for deploying a process-backed agent.                  
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --service-name                           TEXT            service name     │
│    --service-desc…                          TEXT            service          │
│                                                             description      │
│    --service-title                          TEXT            a display name   │
│                                                             for the service  │
│ *  --agent-name                             TEXT            Name of the      │
│                                                             agent to call    │
│                                                             [required]       │
│    --rule           -r                      TEXT            a system rule    │
│    --rules-file                             TEXT                             │
│    --room-rules     -rr                     TEXT            a path to a      │
│                                                             rules file       │
│                                                             within the room  │
│                                                             that can be used │
│                                                             to customize the │
│                                                             agent's behavior │
│    --require-tool…  -rt                     TEXT            the name or url  │
│                                                             of a required    │
│                                                             toolkit          │
│    --require-sche…  -rs                     TEXT            the name or url  │
│                                                             of a required    │
│                                                             schema           │
│    --model                                  TEXT            Name of the LLM  │
│                                                             model to use for │
│                                                             the chatbot      │
│                                                             [default:        │
│                                                             gpt-5.4]         │
│    --image-genera…                          TEXT            Name of an image │
│                                                             gen model        │
│    --local-shell         --no-local-she…                    Enable local     │
│                                                             shell tool       │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-local-shell]  │
│    --shell               --no-shell                         Enable function  │
│                                                             shell tool       │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-shell]        │
│    --apply-patch         --no-apply-pat…                    Enable apply     │
│                                                             patch tool       │
│                                                             [default:        │
│                                                             no-apply-patch]  │
│    --computer-use        --no-computer-…                    Enable computer  │
│                                                             use              │
│                                                             [default:        │
│                                                             no-computer-use] │
│    --web-search          --no-web-search                    Enable web       │
│                                                             search tool      │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-web-search]   │
│    --web-fetch           --no-web-fetch                     Enable web fetch │
│                                                             tool calling     │
│                                                             [default:        │
│                                                             no-web-fetch]    │
│    --script-tool         --no-script-to…                    Enable script    │
│                                                             tool calling     │
│                                                             [default:        │
│                                                             no-script-tool]  │
│    --discover-scr…       --no-discover-…                    Automatically    │
│                                                             add script tools │
│                                                             from the room    │
│                                                             [default:        │
│                                                             no-discover-scr… │
│    --mcp                 --no-mcp                           Enable mcp tool  │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-mcp]          │
│    --storage             --no-storage                       Enable storage   │
│                                                             toolkit          │
│                                                             [default:        │
│                                                             no-storage]      │
│    --storage-tool…                          TEXT            Mount local path │
│                                                             as               │
│                                                             <source>:<mount… │
│    --storage-tool…                          TEXT            Mount room path  │
│                                                             as               │
│                                                             <source>:<mount… │
│    --shell-room-m…                          TEXT            Mount room       │
│                                                             storage as       │
│                                                             <source>:<mount… │
│    --shell-projec…                          TEXT            Mount project    │
│                                                             storage as       │
│                                                             <source>:<mount… │
│    --shell-empty-…                          TEXT            Mount empty dir  │
│                                                             at               │
│                                                             <mount>[:ro|rw]  │
│    --require-imag…                          TEXT            Name of an image │
│                                                             gen model        │
│    --starting-url                           TEXT            Initial URL to   │
│                                                             open when        │
│                                                             starting a       │
│                                                             computer-use     │
│                                                             browser session  │
│    --allow-goto-u…                                          Expose the goto  │
│                                                             URL helper tool  │
│                                                             for computer use │
│    --require-loca…       --no-require-l…                    Enable local     │
│                                                             shell tool       │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-require-loca… │
│    --require-shell       --no-require-s…                    Enable function  │
│                                                             shell tool       │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-require-shel… │
│    --require-appl…       --no-require-a…                    Enable apply     │
│                                                             patch tool       │
│                                                             [default:        │
│                                                             no-require-appl… │
│    --require-web-…       --no-require-w…                    Enable web       │
│                                                             search tool      │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-require-web-… │
│    --require-web-…       --no-require-w…                    Enable web fetch │
│                                                             tool calling     │
│                                                             [default:        │
│                                                             no-require-web-… │
│    --require-mcp         --no-require-m…                    Enable mcp tool  │
│                                                             calling          │
│                                                             [default:        │
│                                                             no-require-mcp]  │
│    --require-stor…       --no-require-s…                    Enable storage   │
│                                                             toolkit          │
│                                                             [default:        │
│                                                             no-require-stor… │
│    --database-nam…                          TEXT            Use a specific   │
│                                                             database         │
│                                                             namespace        │
│    --require-tabl…                          TEXT            Enable table     │
│                                                             read tools for a │
│                                                             specific table   │
│    --require-tabl…                          TEXT            Enable table     │
│                                                             write tools for  │
│                                                             a specific table │
│    --require-read…       --no-require-r…                    Enable read only │
│                                                             storage toolkit  │
│                                                             [default:        │
│                                                             no-require-read… │
│    --require-time        --no-require-t…                    Enable           │
│                                                             time/datetime    │
│                                                             tools            │
│                                                             [default:        │
│                                                             require-time]    │
│    --require-uuid        --no-require-u…                    Enable UUID      │
│                                                             generation tools │
│                                                             [default:        │
│                                                             no-require-uuid] │
│    --use-memory                             TEXT            Use memories     │
│                                                             toolkit for      │
│                                                             <name> or        │
│                                                             <namespace>/<na… │
│    --memory-model                           TEXT            Model name for   │
│                                                             memory LLM       │
│                                                             ingestion        │
│    --working-dir                            TEXT            The default      │
│                                                             working          │
│                                                             directory for    │
│                                                             shell commands   │
│    --require-docu…       --no-require-d…                    Enable document  │
│                                                             authoring        │
│                                                             [default:        │
│                                                             no-require-docu… │
│    --require-disc…       --no-require-d…                    Enable discovery │
│                                                             of agents and    │
│                                                             tools            │
│                                                             [default:        │
│                                                             no-require-disc… │
│    --llm-particip…                          TEXT            Delegate LLM     │
│                                                             interactions to  │
│                                                             a remote         │
│                                                             participant      │
│    --decision-mod…                          TEXT            Model used for   │
│                                                             thread naming    │
│                                                             and other        │
│                                                             secondary LLM    │
│                                                             decisions        │
│    --always-reply        --no-always-re…                    Always reply     │
│    --threading-mo…                          [none|default-  Threading mode   │
│                                             new]            for thread UIs.  │
│                                                             Use              │
│                                                             'default-new' to │
│                                                             show a           │
│                                                             new-thread       │
│                                                             composer before  │
│                                                             loading a        │
│                                                             thread.          │
│                                                             [default: none]  │
│    --thread-dir                             TEXT            Thread directory │
│                                                             for agent thread │
│                                                             files. Defaults  │
│                                                             to               │
│                                                             .threads/<agent… │
│                                                             when not         │
│                                                             provided.        │
│    --channel                                TEXT            Attach a channel │
│                                                             to the agent     │
│                                                             process. Can be  │
│                                                             repeated.        │
│                                                             Currently        │
│                                                             supported: chat, │
│                                                             mail:EMAIL_ADDR… │
│                                                             queue:QUEUE_NAM… │
│                                                             toolkit:NAME.    │
│    --skill-dir                              TEXT            an agent skills  │
│                                                             directory        │
│    --shell-image                            TEXT            an image tag to  │
│                                                             use to run shell │
│                                                             commands in      │
│    --delegate-she…       --no-delegate-…                    log all requests │
│                                                             to the llm       │
│                                                             [default:        │
│                                                             no-delegate-she… │
│    --shell-copy-e…                          TEXT            Copy local env   │
│                                                             vars into shell  │
│                                                             tool env.        │
│                                                             Accepts          │
│                                                             comma-separated  │
│                                                             names and can be │
│                                                             repeated.        │
│    --shell-set-env                          TEXT            Set env vars in  │
│                                                             shell tool env   │
│                                                             as NAME=VALUE.   │
│                                                             Can be repeated. │
│    --log-llm-requ…       --no-log-llm-r…                    log all requests │
│                                                             to the llm       │
│                                                             [default:        │
│                                                             no-log-llm-requ… │
│    --help                                                   Show this        │
│                                                             message and      │
│                                                             exit.            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent project`

```console
$ meshagent project --help
                                                                                
 Usage: meshagent project [OPTIONS] COMMAND [ARGS]...                           
                                                                                
 Manage or activate your meshagent projects                                     
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ create    Create a new MeshAgent project.                                    │
│ list      List projects and mark the currently active one.                   │
│ activate  Set the active project for subsequent CLI commands.                │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent project activate`

```console
$ meshagent project activate --help
                                                                                
 Usage: meshagent project activate [OPTIONS] [PROJECT_ID]                       
                                                                                
 Set the active project for subsequent CLI commands.                            
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│   project_id      [PROJECT_ID]                                               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --interactive  -i        Interactively select or create a project            │
│ --help                   Show this message and exit.                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent project create`

```console
$ meshagent project create --help
                                                                                
 Usage: meshagent project create [OPTIONS] NAME                                 
                                                                                
 Create a new MeshAgent project.                                                
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    name      TEXT  [required]                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent project list`

```console
$ meshagent project list --help
                                                                                
 Usage: meshagent project list [OPTIONS]                                        
                                                                                
 List projects and mark the currently active one.                               
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --output  -o      TEXT  output format  [default: table]                      │
│ --help                  Show this message and exit.                          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent room`

```console
$ meshagent room --help
                                                                                
 Usage: meshagent room [OPTIONS] COMMAND [ARGS]...                              
                                                                                
 Operate within a room                                                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ agent      Interact with agents and toolkits                                 │
│ secret     Manage secrets in a room                                          │
│ queue      Use queues in a room                                              │
│ messaging  Send and receive messages                                         │
│ storage    Manage storage for a room                                         │
│ service    Manage services in a room                                         │
│ developer  Developer utilities for a room                                    │
│ database   Manage database tables in a room                                  │
│ memory     Manage memories in a room                                         │
│ container  Manage containers and images in a room                            │
│ sync       Inspect and update mesh documents in a room                       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent room agent`

```console
$ meshagent room agent --help
                                                                                
 Usage: meshagent room agent [OPTIONS] COMMAND [ARGS]...                        
                                                                                
 Interact with agents and toolkits                                              
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ invoke-tool    Invoke a specific tool from a toolkit                         │
│ list-toolkits  List toolkits (and tools) available in the room               │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room agent invoke-tool`

```console
$ meshagent room agent invoke-tool --help
                                                                                
 Usage: meshagent room agent invoke-tool [OPTIONS]                              
                                                                                
 Invoke a specific tool from a toolkit                                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id             TEXT     A MeshAgent project id. If empty, the   │
│                                      activated project will be used.         │
│                                      [default:                               │
│                                      203b1bf9-72c9-4022-bfaa-55d6f656dfeb]   │
│ *  --room                   TEXT     Room name [required]                    │
│ *  --toolkit                TEXT     Toolkit name [required]                 │
│ *  --tool                   TEXT     Tool name [required]                    │
│ *  --arguments              TEXT     JSON string with arguments for the tool │
│                                      [required]                              │
│    --participant-id         TEXT     Optional participant ID to invoke the   │
│                                      tool on                                 │
│    --on-behalf-of-id        TEXT     Optional 'on_behalf_of' participant ID  │
│    --caller-context         TEXT     Optional JSON for caller context        │
│    --timeout                INTEGER  How long to wait for the toolkit if the │
│                                      toolkit is not in the room              │
│                                      [default: 30]                           │
│    --help                            Show this message and exit.             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room agent list-toolkits`

```console
$ meshagent room agent list-toolkits --help
                                                                                
 Usage: meshagent room agent list-toolkits [OPTIONS]                            
                                                                                
 List toolkits (and tools) available in the room                                
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id            TEXT  A MeshAgent project id. If empty, the       │
│                                  activated project will be used.             │
│                                  [default:                                   │
│                                  203b1bf9-72c9-4022-bfaa-55d6f656dfeb]       │
│ *  --room                  TEXT  Room name [required]                        │
│    --role                  TEXT  [default: user]                             │
│    --participant-id        TEXT  Optional participant ID                     │
│    --help                        Show this message and exit.                 │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent room container`

```console
$ meshagent room container --help
                                                                                
 Usage: meshagent room container [OPTIONS] COMMAND [ARGS]...                    
                                                                                
 Manage containers and images in a room                                         
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ list   List containers in a room.                                            │
│ stop   Stop a running container in a room.                                   │
│ log    Print container logs from a room.                                     │
│ exec   Execute a command inside a running container.                         │
│ run    Run a container inside a room.                                        │
│ image  Image operations                                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room container exec`

```console
$ meshagent room container exec --help
                                                                                
 Usage: meshagent room container exec [OPTIONS]                                 
                                                                                
 Execute a command inside a running container.                                  
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id                  TEXT  A MeshAgent project id. If empty, the │
│                                        activated project will be used.       │
│                                        [default:                             │
│                                        203b1bf9-72c9-4022-bfaa-55d6f656dfeb] │
│ *  --room                        TEXT  Room name [required]                  │
│ *  --container-id                TEXT  container id [required]               │
│    --command                     TEXT  Command to execute in the container   │
│                                        (quoted string)                       │
│    --tty             --no-tty          Allocate a TTY [default: no-tty]      │
│    --help                              Show this message and exit.           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room container list`

```console
$ meshagent room container list --help
                                                                                
 Usage: meshagent room container list [OPTIONS]                                 
                                                                                
 List containers in a room.                                                     
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id          TEXT  A MeshAgent project id. If empty, the         │
│                                activated project will be used.               │
│                                [default:                                     │
│                                203b1bf9-72c9-4022-bfaa-55d6f656dfeb]         │
│ *  --room                TEXT  Room name [required]                          │
│    --all         -a            Include exited containers in the listing.     │
│    --output              TEXT  json | table [default: json]                  │
│    --help                      Show this message and exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room container log`

```console
$ meshagent room container log --help
                                                                                
 Usage: meshagent room container log [OPTIONS]                                  
                                                                                
 Print container logs from a room.                                              
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id                   TEXT  A MeshAgent project id. If empty,    │
│                                         the activated project will be used.  │
│                                         [default:                            │
│                                         203b1bf9-72c9-4022-bfaa-55d6f656dfe… │
│ *  --room                         TEXT  Room name [required]                 │
│ *  --id                           TEXT  Container ID [required]              │
│    --follow        --no-follow          Stream logs [default: no-follow]     │
│    --help                               Show this message and exit.          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent room database`

```console
$ meshagent room database --help
                                                                                
 Usage: meshagent room database [OPTIONS] COMMAND [ARGS]...                     
                                                                                
 Manage database tables in a room                                               
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ table         List database tables in a room.                                │
│ inspect       Inspect a table schema in a room database.                     │
│ install       Install required tables from a requirements JSON file.         │
│ create        Create a room database table with optional schema and seed     │
│               data.                                                          │
│ drop          Drop a room database table.                                    │
│ add-columns   Add columns to a room database table.                          │
│ drop-columns  Drop columns from a room database table.                       │
│ insert        Insert records into a room database table.                     │
│ merge         Upsert records into a room database table.                     │
│ update        Update rows in a room database table.                          │
│ delete        Delete rows from a room database table.                        │
│ search        Search rows in a room database table.                          │
│ sql           Execute SQL against room database tables.                      │
│ optimize      Optimize a room database table.                                │
│ version       List versions for a room database table.                       │
│ checkout      Check out a room database table at a specific version.         │
│ restore       Restore a room database table to a specific version.           │
│ index         List indexes on a room database table.                         │
│ index-create  Create an index on a room database table.                      │
│ index-drop    Drop an index from a room database table.                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room database inspect`

```console
$ meshagent room database inspect --help
                                                                                
 Usage: meshagent room database inspect [OPTIONS]                               
                                                                                
 Inspect a table schema in a room database.                                     
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id          TEXT  A MeshAgent project id. If empty, the         │
│                                activated project will be used.               │
│                                [default:                                     │
│                                203b1bf9-72c9-4022-bfaa-55d6f656dfeb]         │
│ *  --room                TEXT  Room name [required]                          │
│ *  --table       -t      TEXT  Table name [required]                         │
│    --namespace   -n      TEXT  Namespace path segments (repeatable).         │
│                                Example: -n prod -n analytics                 │
│    --json                      Output raw schema JSON                        │
│    --help                      Show this message and exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room database search`

```console
$ meshagent room database search --help
                                                                                
 Usage: meshagent room database search [OPTIONS]                                
                                                                                
 Search rows in a room database table.                                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id                      TEXT     A MeshAgent project id. If     │
│                                               empty, the activated project   │
│                                               will be used.                  │
│                                               [default:                      │
│                                               203b1bf9-72c9-4022-bfaa-55d6f… │
│ *  --room                            TEXT     Room name [required]           │
│ *  --table        -t                 TEXT     Table name [required]          │
│    --namespace    -n                 TEXT     Namespace path segments        │
│                                               (repeatable). Example: -n prod │
│                                               -n analytics                   │
│    --text                            TEXT     Full-text query                │
│    --vector-json                     TEXT     Vector JSON array              │
│    --where                           TEXT     SQL WHERE clause               │
│    --where-json                      TEXT     JSON object converted to       │
│                                               equality ANDs                  │
│    --select                          TEXT     Columns to select (repeatable) │
│    --limit                           INTEGER  Max rows to return             │
│    --offset                          INTEGER  Rows to skip                   │
│    --pretty           --no-pretty             Pretty-print JSON              │
│                                               [default: pretty]              │
│    --help                                     Show this message and exit.    │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room database table`

```console
$ meshagent room database table --help
                                                                                
 Usage: meshagent room database table [OPTIONS]                                 
                                                                                
 List database tables in a room.                                                
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id          TEXT  A MeshAgent project id. If empty, the         │
│                                activated project will be used.               │
│                                [default:                                     │
│                                203b1bf9-72c9-4022-bfaa-55d6f656dfeb]         │
│ *  --room                TEXT  Room name [required]                          │
│    --namespace   -n      TEXT  Namespace path segments (repeatable).         │
│                                Example: -n prod -n analytics                 │
│    --help                      Show this message and exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent room developer`

```console
$ meshagent room developer --help
                                                                                
 Usage: meshagent room developer [OPTIONS] COMMAND [ARGS]...                    
                                                                                
 Developer utilities for a room                                                 
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ watch  Stream developer logs from a room                                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room developer watch`

```console
$ meshagent room developer watch --help
                                                                                
 Usage: meshagent room developer watch [OPTIONS]                                
                                                                                
 Stream developer logs from a room                                              
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id        TEXT          A MeshAgent project id. If empty, the   │
│                                      activated project will be used.         │
│                                      [default:                               │
│                                      203b1bf9-72c9-4022-bfaa-55d6f656dfeb]   │
│ *  --room              TEXT          Room name [required]                    │
│    --format            [plain|json]  Output format [default: plain]          │
│    --help                            Show this message and exit.             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent room memory`

```console
$ meshagent room memory --help
                                                                                
 Usage: meshagent room memory [OPTIONS] COMMAND [ARGS]...                       
                                                                                
 Manage memories in a room                                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ list                  List memories in a room namespace.                     │
│ create                Create a room memory store.                            │
│ drop                  Drop a room memory store.                              │
│ inspect               Inspect metadata and datasets for a memory.            │
│ query                 Run a SQL-like query against memory datasets.          │
│ upsert-table          Upsert records from JSON into memory tables.           │
│ upsert-nodes          Upsert entity nodes into memory.                       │
│ upsert-relationships  Upsert relationship edges into memory.                 │
│ import                Import entities and relationships from a FalkorDB      │
│                       dump.rdb file.                                         │
│ ingest-text           Extract memory from input text.                        │
│ ingest-image          Extract memory from an image.                          │
│ ingest-file           Extract memory from local file/text content.           │
│ ingest-from-table     Extract memory from table rows.                        │
│ ingest-from-storage   Extract memory from room storage paths.                │
│ recall                Recall entities and relationships from memory.         │
│ delete-entities       Delete entities (and related edges) from memory.       │
│ delete-relationships  Delete relationship edges from memory.                 │
│ optimize              Optimize memory datasets.                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent room messaging`

```console
$ meshagent room messaging --help
                                                                                
 Usage: meshagent room messaging [OPTIONS] COMMAND [ARGS]...                    
                                                                                
 Send and receive messages                                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ list       List messaging-enabled participants                               │
│ send       Send a direct message to a participant                            │
│ broadcast  Broadcast a message to all participants                           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent room queue`

```console
$ meshagent room queue --help
                                                                                
 Usage: meshagent room queue [OPTIONS] COMMAND [ARGS]...                        
                                                                                
 Use queues in a room                                                           
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ list       List queues in a room.                                            │
│ send       Send a JSON message to a room queue.                              │
│ send-mail  Create an email message and send it to a room queue.              │
│ receive    Receive a message from a room queue.                              │
│ size       Show the current size of a room queue.                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room queue receive`

```console
$ meshagent room queue receive --help
                                                                                
 Usage: meshagent room queue receive [OPTIONS]                                  
                                                                                
 Receive a message from a room queue.                                           
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id        TEXT  A MeshAgent project id. If empty, the activated │
│                              project will be used.                           │
│                              [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb] │
│ *  --room              TEXT  Room name [required]                            │
│ *  --queue             TEXT  Queue name [required]                           │
│    --help                    Show this message and exit.                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room queue send`

```console
$ meshagent room queue send --help
                                                                                
 Usage: meshagent room queue send [OPTIONS]                                     
                                                                                
 Send a JSON message to a room queue.                                           
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id          TEXT  A MeshAgent project id. If empty, the         │
│                                activated project will be used.               │
│                                [default:                                     │
│                                203b1bf9-72c9-4022-bfaa-55d6f656dfeb]         │
│ *  --room                TEXT  Room name [required]                          │
│ *  --queue               TEXT  Queue name [required]                         │
│ *  --json                TEXT  a JSON message to send to the queue           │
│                                [required]                                    │
│    --file        -f      TEXT  File path to a JSON file                      │
│    --help                      Show this message and exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room queue size`

```console
$ meshagent room queue size --help
                                                                                
 Usage: meshagent room queue size [OPTIONS]                                     
                                                                                
 Show the current size of a room queue.                                         
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id        TEXT  A MeshAgent project id. If empty, the activated │
│                              project will be used.                           │
│                              [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb] │
│ *  --room              TEXT  Room name [required]                            │
│ *  --queue             TEXT  Queue name [required]                           │
│    --help                    Show this message and exit.                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent room secret`

```console
$ meshagent room secret --help
                                                                                
 Usage: meshagent room secret [OPTIONS] COMMAND [ARGS]...                       
                                                                                
 Manage secrets in a room                                                       
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ oauth    Request an OAuth token from another participant.                    │
│ request  Request a secret from another participant.                          │
│ get      Fetch a stored secret by ID.                                        │
│ set      Store a secret by ID.                                               │
│ list     List secrets in the room.                                           │
│ delete   Delete a secret by ID.                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent room service`

```console
$ meshagent room service --help
                                                                                
 Usage: meshagent room service [OPTIONS] COMMAND [ARGS]...                      
                                                                                
 Manage services in a room                                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ list     List services running in a room                                     │
│ restart  Restart a running room service by stopping its current container.   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room service list`

```console
$ meshagent room service list --help
                                                                                
 Usage: meshagent room service list [OPTIONS]                                   
                                                                                
 List services running in a room                                                
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id          TEXT  A MeshAgent project id. If empty, the         │
│                                activated project will be used.               │
│                                [default:                                     │
│                                203b1bf9-72c9-4022-bfaa-55d6f656dfeb]         │
│ *  --room                TEXT  Room name [required]                          │
│    --output      -o      TEXT  output format  [default: table]               │
│    --help                      Show this message and exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent room storage`

```console
$ meshagent room storage --help
                                                                                
 Usage: meshagent room storage [OPTIONS] COMMAND [ARGS]...                      
                                                                                
 Manage storage for a room                                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ exists  Check whether a path exists in room storage.                         │
│ cp      Copy files between local paths and room storage.                     │
│ show    Print file contents from local disk or room storage.                 │
│ rm      Remove files or directories from local disk or room storage.         │
│ ls      List files and directories locally or in room storage.               │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### `meshagent room storage exists`

```console
$ meshagent room storage exists --help
                                                                                
 Usage: meshagent room storage exists [OPTIONS] PATH                            
                                                                                
 Check whether a path exists in room storage.                                   
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  [required]                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id        TEXT  A MeshAgent project id. If empty, the activated │
│                              project will be used.                           │
│                              [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb] │
│ *  --room              TEXT  Room name [required]                            │
│    --help                    Show this message and exit.                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent room sync`

```console
$ meshagent room sync --help
                                                                                
 Usage: meshagent room sync [OPTIONS] COMMAND [ARGS]...                         
                                                                                
 Inspect and update mesh documents in a room                                    
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ show     Print the full document JSON                                        │
│ grep     Search the document for matching content                            │
│ inspect  Print the document schema JSON                                      │
│ create   Create a new document at a path                                     │
│ update   Apply a JSON patch to a document                                    │
│ import   Import external exports into room documents                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent rooms`

```console
$ meshagent rooms --help
                                                                                
 Usage: meshagent rooms [OPTIONS] COMMAND [ARGS]...                             
                                                                                
 Create, list, and manage rooms in a project                                    
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ create  Create a room in the project.                                        │
│ delete  Delete a room by ID (or by name if --name is supplied).              │
│ update  Update a room's name (ID is preferred; name will be resolved to ID   │
│         if needed).                                                          │
│ list    List rooms in the project.                                           │
│ get     Get a single room by name (handy for resolving the ID).              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent rooms list`

```console
$ meshagent rooms list --help
                                                                                
 Usage: meshagent rooms list [OPTIONS]                                          
                                                                                
 List rooms in the project.                                                     
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id        TEXT                       A MeshAgent project id. If    │
│                                                empty, the activated project  │
│                                                will be used.                 │
│                                                [default:                     │
│                                                203b1bf9-72c9-4022-bfaa-55d6… │
│ --limit             INTEGER RANGE [1<=x<=500]  Max rooms to return           │
│                                                [default: 50]                 │
│ --offset            INTEGER RANGE [x>=0]       Offset for pagination         │
│                                                [default: 0]                  │
│ --order-by          TEXT                       Order by column (e.g.         │
│                                                "room_name", "created_at")    │
│                                                [default: room_name]          │
│ --help                                         Show this message and exit.   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent route`

```console
$ meshagent route --help
                                                                                
 Usage: meshagent route [OPTIONS] COMMAND [ARGS]...                             
                                                                                
 Manage routes for your project                                                 
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ create  Create a route attached to the project.                              │
│ update  Update a route configuration.                                        │
│ show    Show route details.                                                  │
│ list    List routes for the project.                                         │
│ delete  Delete a route.                                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent route create`

```console
$ meshagent route create --help
                                                                                
 Usage: meshagent route create [OPTIONS]                                        
                                                                                
 Create a route attached to the project.                                        
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id           TEXT  A MeshAgent project id. If empty, the        │
│                                 activated project will be used.              │
│                                 [default:                                    │
│                                 203b1bf9-72c9-4022-bfaa-55d6f656dfeb]        │
│ *  --domain       -d      TEXT  Domain name to route (unique per project)    │
│                                 [required]                                   │
│    --room                 TEXT  Room name                                    │
│ *  --port         -p      TEXT  Published port to route to [required]        │
│    --annotations  -n      TEXT  annotations in json format {"name":"value"}  │
│    --help                       Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent route delete`

```console
$ meshagent route delete --help
                                                                                
 Usage: meshagent route delete [OPTIONS] DOMAIN                                 
                                                                                
 Delete a route.                                                                
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    domain      TEXT  Domain name to delete [required]                      │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id        TEXT  A MeshAgent project id. If empty, the activated    │
│                           project will be used.                              │
│                           [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb]    │
│ --help                    Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent route list`

```console
$ meshagent route list --help
                                                                                
 Usage: meshagent route list [OPTIONS]                                          
                                                                                
 List routes for the project.                                                   
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id          TEXT  A MeshAgent project id. If empty, the activated  │
│                             project will be used.                            │
│                             [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb]  │
│ --room                TEXT  Room name                                        │
│ --output      -o      TEXT  output format  [default: table]                  │
│ --help                      Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent route show`

```console
$ meshagent route show --help
                                                                                
 Usage: meshagent route show [OPTIONS] DOMAIN                                   
                                                                                
 Show route details.                                                            
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    domain      TEXT  Domain name to show [required]                        │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id        TEXT  A MeshAgent project id. If empty, the activated    │
│                           project will be used.                              │
│                           [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb]    │
│ --help                    Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent route update`

```console
$ meshagent route update --help
                                                                                
 Usage: meshagent route update [OPTIONS] DOMAIN                                 
                                                                                
 Update a route configuration.                                                  
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    domain      TEXT  Domain name to update [required]                      │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id           TEXT  A MeshAgent project id. If empty, the activated │
│                              project will be used.                           │
│                              [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb] │
│ --room         -r      TEXT  Room name to route traffic into                 │
│ --port         -p      TEXT  Published port to route to                      │
│ --annotations  -n      TEXT  annotations in json format {"name":"value"}     │
│ --help                       Show this message and exit.                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent scheduled-task`

```console
$ meshagent scheduled-task --help
                                                                                
 Usage: meshagent scheduled-task [OPTIONS] COMMAND [ARGS]...                    
                                                                                
 Manage scheduled tasks for your project                                        
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ add     Add a scheduled task.                                                │
│ list    List scheduled tasks.                                                │
│ update  Update a scheduled task.                                             │
│ delete  Delete a scheduled task.                                             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent scheduled-task add`

```console
$ meshagent scheduled-task add --help
                                                                                
 Usage: meshagent scheduled-task add [OPTIONS]                                  
                                                                                
 Add a scheduled task.                                                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id                      TEXT  A MeshAgent project id. If empty, │
│                                            the activated project will be     │
│                                            used.                             │
│                                            [default:                         │
│                                            203b1bf9-72c9-4022-bfaa-55d6f656… │
│    --room          -r                TEXT  Room name                         │
│ *  --queue         -q                TEXT  Queue name to dispatch the task   │
│                                            to                                │
│                                            [required]                        │
│ *  --schedule      -s                TEXT  Cron schedule for task execution  │
│                                            [required]                        │
│    --payload                         TEXT  JSON payload to enqueue (for      │
│                                            example '{"action":"sync"}')      │
│    --payload-file                    TEXT  Path to a file containing JSON    │
│                                            payload                           │
│    --id                              TEXT  Optional task id                  │
│    --once                                  Run once and then deactivate      │
│    --active            --inactive          Initial active state              │
│                                            [default: active]                 │
│    --annotations   -n                TEXT  annotations in json format        │
│                                            {"name":"value"}                  │
│    --help                                  Show this message and exit.       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent scheduled-task delete`

```console
$ meshagent scheduled-task delete --help
                                                                                
 Usage: meshagent scheduled-task delete [OPTIONS] TASK_ID                       
                                                                                
 Delete a scheduled task.                                                       
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    task_id      TEXT  Scheduled task id to delete [required]               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id        TEXT  A MeshAgent project id. If empty, the activated    │
│                           project will be used.                              │
│                           [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb]    │
│ --help                    Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent scheduled-task list`

```console
$ meshagent scheduled-task list --help
                                                                                
 Usage: meshagent scheduled-task list [OPTIONS]                                 
                                                                                
 List scheduled tasks.                                                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id            TEXT     A MeshAgent project id. If empty, the       │
│                                  activated project will be used.             │
│                                  [default:                                   │
│                                  203b1bf9-72c9-4022-bfaa-55d6f656dfeb]       │
│ --room          -r      TEXT     Filter by room name                         │
│ --id,--task-id          TEXT     Filter by scheduled task id                 │
│ --active                         Filter to active tasks only                 │
│ --inactive                       Filter to inactive tasks only               │
│ --limit                 INTEGER  Maximum number of tasks to return           │
│                                  [default: 200]                              │
│ --offset                INTEGER  Row offset for pagination [default: 0]      │
│ --output        -o      TEXT     output format  [default: table]             │
│ --help                           Show this message and exit.                 │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent scheduled-task update`

```console
$ meshagent scheduled-task update --help
                                                                                
 Usage: meshagent scheduled-task update [OPTIONS] TASK_ID                       
                                                                                
 Update a scheduled task.                                                       
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    task_id      TEXT  Scheduled task id to update [required]               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id            TEXT  A MeshAgent project id. If empty, the          │
│                               activated project will be used.                │
│                               [default:                                      │
│                               203b1bf9-72c9-4022-bfaa-55d6f656dfeb]          │
│ --room          -r      TEXT  Updated room name                              │
│ --queue         -q      TEXT  Updated queue name                             │
│ --schedule      -s      TEXT  Updated cron schedule                          │
│ --payload               TEXT  Updated JSON payload to enqueue (for example   │
│                               '{"action":"sync"}')                           │
│ --payload-file          TEXT  Path to a file containing updated JSON payload │
│ --active                      Mark the task active                           │
│ --inactive                    Mark the task inactive                         │
│ --annotations   -n      TEXT  annotations in json format {"name":"value"}    │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent secret`

```console
$ meshagent secret --help
                                                                                
 Usage: meshagent secret [OPTIONS] COMMAND [ARGS]...                            
                                                                                
 Manage secrets for your project.                                               
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ list    List all secrets in the project (typed as Docker/ACR/GAR or Keys     │
│         secrets).                                                            │
│ delete  Delete a secret.                                                     │
│ key     Create or update environment-based key-value secrets.                │
│ docker  Create or update a Docker registry pull secret.                      │
│ acr     Create or update an Azure Container Registry pull secret.            │
│ gar     Create or update a Google Artifact Registry pull secret.             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent service`

```console
$ meshagent service --help
                                                                                
 Usage: meshagent service [OPTIONS] COMMAND [ARGS]...                           
                                                                                
 Manage services for your project                                               
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ spec               Render a service or template YAML spec without creating a │
│                    service.                                                  │
│ create             Create a service attached to the project.                 │
│ update             Create a service attached to the project.                 │
│ validate           Validate a service spec from a YAML file.                 │
│ create-template    Create a service from a ServiceTemplate spec.             │
│ update-template    Update a service using a ServiceTemplate spec.            │
│ validate-template  Validate a service template from a YAML file.             │
│ render-template    Render a service template with variables and print the    │
│                    rendered YAML.                                            │
│ run                Run a local command and register it as a temporary room   │
│                    service.                                                  │
│ show               Show a services for the project.                          │
│ list               List all services for the project.                        │
│ delete             Delete a service.                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent service list`

```console
$ meshagent service list --help
                                                                                
 Usage: meshagent service list [OPTIONS]                                        
                                                                                
 List all services for the project.                                             
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id          TEXT  A MeshAgent project id. If empty, the activated  │
│                             project will be used.                            │
│                             [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb]  │
│ --output      -o      TEXT  output format  [default: table]                  │
│ --room                TEXT  Room name                                        │
│ --help                      Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent service render-template`

```console
$ meshagent service render-template --help
                                                                                
 Usage: meshagent service render-template [OPTIONS]                             
                                                                                
 Render a service template with variables and print the rendered YAML.          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --file         -f      TEXT  File path to a service template                 │
│ --url                  TEXT  URL to a service template                       │
│ --values-file          TEXT  File path to template values                    │
│ --value        -v      TEXT  Template value override (key=value)             │
│ --help                       Show this message and exit.                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent service show`

```console
$ meshagent service show --help
                                                                                
 Usage: meshagent service show [OPTIONS] SERVICE_ID                             
                                                                                
 Show a services for the project.                                               
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    service_id      TEXT  ID of the service to show [required]              │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --project-id        TEXT  A MeshAgent project id. If empty, the activated    │
│                           project will be used.                              │
│                           [default: 203b1bf9-72c9-4022-bfaa-55d6f656dfeb]    │
│ --room              TEXT  Room name                                          │
│ --help                    Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent service spec`

```console
$ meshagent service spec --help
                                                                                
 Usage: meshagent service spec [OPTIONS]                                        
                                                                                
 Render a service or template YAML spec without creating a service.             
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --file        -f      TEXT                File path to a service definition  │
│ --url                 TEXT                URL to a service definition        │
│ --mcp                 TEXT                MCP server URL. Auto-discovers     │
│                                           metadata and generates a service   │
│                                           spec without creating it.          │
│ --format              [service|template]  Output format. 'service' emits     │
│                                           Service YAML. 'template' emits     │
│                                           ServiceTemplate YAML.              │
│                                           [default: service]                 │
│ --service-id          TEXT                Optional override for              │
│                                           meshagent.service.id in metadata   │
│                                           annotations.                       │
│ --help                                    Show this message and exit.        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent service validate`

```console
$ meshagent service validate --help
                                                                                
 Usage: meshagent service validate [OPTIONS]                                    
                                                                                
 Validate a service spec from a YAML file.                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ *  --file  -f      TEXT  File path to a service definition [required]        │
│    --help                Show this message and exit.                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent service validate-template`

```console
$ meshagent service validate-template --help
                                                                                
 Usage: meshagent service validate-template [OPTIONS]                           
                                                                                
 Validate a service template from a YAML file.                                  
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --file         -f      TEXT  File path to a service template                 │
│ --url                  TEXT  URL to a service template                       │
│ --values-file          TEXT  File path to template values                    │
│ --value        -v      TEXT  Template value override (key=value)             │
│ --help                       Show this message and exit.                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent session`

```console
$ meshagent session --help
                                                                                
 Usage: meshagent session [OPTIONS] COMMAND [ARGS]...                           
                                                                                
 Inspect recent sessions and events                                             
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ list  List recent sessions                                                   │
│ show  Show events for a session                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent setup`

```console
$ meshagent setup --help
                                                                                
 Usage: meshagent setup [OPTIONS]                                               
                                                                                
 Perform initial login and project/api key activation.                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent task-runner`

```console
$ meshagent task-runner --help
                                                                                
 Usage: meshagent task-runner [OPTIONS] COMMAND [ARGS]...                       
                                                                                
 Join a taskrunner to a room                                                    
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ join     Join a room and run a task-runner agent.                            │
│ run      Join a room, run the task-runner, and wait for tasks.               │
│ service                                                                      │
│ spec     Generate a service spec for deploying a task-runner.                │
│ deploy   Deploy a task-runner service to a project or room.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent token`

```console
$ meshagent token --help
                                                                                
 Usage: meshagent token [OPTIONS] COMMAND [ARGS]...                             
                                                                                
 Generate participant tokens (JWTs)                                             
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ generate  Generate a participant token (JWT) from a spec                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent token generate`

```console
$ meshagent token generate --help
                                                                                
 Usage: meshagent token generate [OPTIONS]                                      
                                                                                
 Generate a participant token (JWT) from a spec                                 
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id          TEXT  A MeshAgent project id. If empty, the         │
│                                activated project will be used.               │
│                                [default:                                     │
│                                203b1bf9-72c9-4022-bfaa-55d6f656dfeb]         │
│    --output      -o      TEXT  File path to a file                           │
│ *  --input       -i      TEXT  File path to a token spec [required]          │
│    --key                 TEXT  an api key to sign the token with             │
│    --help                      Show this message and exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent version`

```console
$ meshagent version --help
                                                                                
 Usage: meshagent version [OPTIONS]                                             
                                                                                
 Print the version                                                              
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent voicebot`

```console
$ meshagent voicebot --help
                                                                                
 Usage: meshagent voicebot [OPTIONS] COMMAND [ARGS]...                          
                                                                                
 Join a voicebot to a room                                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ join     Join a room and run a voicebot agent.                               │
│ service                                                                      │
│ spec     Generate a service spec for deploying a voicebot.                   │
│ deploy   Deploy a voicebot service to a project or room.                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent webhook`

```console
$ meshagent webhook --help
                                                                                
 Usage: meshagent webhook [OPTIONS] COMMAND [ARGS]...                           
                                                                                
 Manage project webhooks                                                        
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ create  Create a webhook                                                     │
│ list    List webhooks                                                        │
│ delete  Delete a webhook                                                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent webserver`

```console
$ meshagent webserver --help
                                                                                
 Usage: meshagent webserver [OPTIONS] COMMAND [ARGS]...                         
                                                                                
 Run an HTTP webserver connected to a MeshAgent room.                           
                                                                                
 The webserver mounts static files/folders and python handlers from a routes    
 file.                                                                          
 Python handlers run with access to the active room and request objects.        
 This lets you build web applications that take advantage of the MeshAgent      
 room's full feature set.                                                       
                                                                                
 Default routes file: webserver.yaml                                            
                                                                                
 Add routes with the CLI:                                                       
   meshagent webserver add --path / --python handlers/home.py                   
   meshagent webserver add --path /assets --static ./public                     
                                                                                
 Start it locally by joining a room:                                            
   meshagent webserver join --room my-room --agent-name my-web -f               
 webserver.yaml --watch                                                         
                                                                                
 View the site from your local machine:                                         
   http://127.0.0.1:8000                                                        
                                                                                
 Use the host/port from webserver.yaml (or explicit --host/--port or            
 --web-host/--web-port overrides).                                              
                                                                                
 To make the site available outside your machine:                               
   meshagent webserver deploy --service-name my-web --agent-name my-web --room  
 my-room -f webserver.yaml --website-path /website --domain                     
 my-web.meshagent.app                                                           
                                                                                
 `--domain` automatically creates or updates the route to the deployed room and 
 webserver port.                                                                
 If the domain already targets a different room, deploy fails to avoid          
 accidental repoints.                                                           
 Without `--domain`, create the route manually:                                 
   meshagent route create --room my-room --port 8000 --domain                   
 my-web.meshagent.app                                                           
                                                                                
 Route source path rules:                                                       
 - `python` and `static` sources that start with `/` resolve to `{cwd}/...`.    
 - `python` and `static` sources without a leading `/` resolve relative to the  
 routes file.                                                                   
 - `static` supports both files and directories.                                
 - Set `--app-dir` to control Python import root (defaults to routes file       
 directory).                                                                    
                                                                                
                                                                                
 Example routes file:                                                           
 kind: WebServer                                                                
 version: v1                                                                    
 host: 0.0.0.0                                                                  
 port: 8000                                                                     
 routes:                                                                        
   - path: /                                                                    
     methods:                                                                   
       - GET                                                                    
     python: handlers/home.py                                                   
   - path: /assets                                                              
     static: ./public                                                           
                                                                                
 Example python handler (handlers/home.py):                                     
 from aiohttp import web                                                        
 from meshagent.api import RoomClient                                           
                                                                                
 async def handler(                                                             
     *,                                                                         
     room: RoomClient,                                                          
     req: web.Request,                                                          
 ) -> web.StreamResponse:                                                       
     return web.Response(text="hello")                                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ check   Validate a routes file and print the resolved routes.                │
│ init    Create a routes file scaffold.                                       │
│ add     Add a route entry to the routes file.                                │
│ join    Join a room and run the configured webserver routes locally with     │
│         optional hot reload.                                                 │
│ spec    Generate a service spec for deploying this webserver configuration.  │
│ deploy  Deploy this webserver as a service, updating an existing service     │
│         with the same name.                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent webserver check`

```console
$ meshagent webserver check --help
                                                                                
 Usage: meshagent webserver check [OPTIONS]                                     
                                                                                
 Validate a routes file and print the resolved routes.                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│            -f      TEXT  Path to routes file (default: webserver.yaml). YAML │
│                          format: kind: WebServer, version: v1, host?, port?, │
│                          routes: [{path, methods?, python?|static?}]. Route  │
│                          source resolution: '/x' -> '{cwd}/x'; 'x' ->        │
│                          relative to routes file. 'static' supports files    │
│                          and directories. Use --app-dir to control Python    │
│                          import root (defaults to routes file directory).    │
│                          When --host/--port (or --web-host/--web-port) are   │
│                          not explicitly set, host/port from the routes file  │
│                          are used. Python handler signature: handler(*,      │
│                          room: RoomClient, req: web.Request) ->              │
│                          web.StreamResponse. Do not define METHOD/METHODS in │
│                          handler files.                                      │
│                          [default: webserver.yaml]                           │
│ --app-dir          TEXT  Python import root for route handlers (similar to   │
│                          uvicorn --app-dir). Defaults to the routes file     │
│                          directory.                                          │
│ --help                   Show this message and exit.                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent webserver deploy`

```console
$ meshagent webserver deploy --help
                                                                                
 Usage: meshagent webserver deploy [OPTIONS]                                    
                                                                                
 Deploy this webserver as a service, updating an existing service with the same 
 name.                                                                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --service-name                 TEXT     service name                      │
│    --service-description          TEXT     service description               │
│    --service-title                TEXT     a display name for the service    │
│ *  --agent-name                   TEXT     Name of the agent to call         │
│                                            [required]                        │
│                           -f      TEXT     Path to routes file (default:     │
│                                            webserver.yaml). YAML format:     │
│                                            kind: WebServer, version: v1,     │
│                                            host?, port?, routes: [{path,     │
│                                            methods?, python?|static?}].      │
│                                            Route source resolution: '/x' ->  │
│                                            '{cwd}/x'; 'x' -> relative to     │
│                                            routes file. 'static' supports    │
│                                            files and directories. Use        │
│                                            --app-dir to control Python       │
│                                            import root (defaults to routes   │
│                                            file directory). When             │
│                                            --host/--port (or                 │
│                                            --web-host/--web-port) are not    │
│                                            explicitly set, host/port from    │
│                                            the routes file are used. Python  │
│                                            handler signature: handler(*,     │
│                                            room: RoomClient, req:            │
│                                            web.Request) ->                   │
│                                            web.StreamResponse. Do not define │
│                                            METHOD/METHODS in handler files.  │
│                                            [default: webserver.yaml]         │
│    --app-dir                      TEXT     Python import root for route      │
│                                            handlers (similar to uvicorn      │
│                                            --app-dir). Defaults to the       │
│                                            routes file directory.            │
│    --web-host                     TEXT     Host to bind the webserver        │
│                                            [default: 0.0.0.0]                │
│    --web-port                     INTEGER  Port to bind the webserver        │
│                                            [default: 8000]                   │
│    --project-id                   TEXT     A MeshAgent project id. If empty, │
│                                            the activated project will be     │
│                                            used.                             │
│                                            [default:                         │
│                                            203b1bf9-72c9-4022-bfaa-55d6f656… │
│    --room                         TEXT     The name of a room to create the  │
│                                            service for                       │
│    --domain                       TEXT     Domain to create/update route for │
│                                            this deploy (must already target  │
│                                            this room if it exists)           │
│ *  --website-path                 TEXT     Required room storage subpath to  │
│                                            upload route-referenced files     │
│                                            (under the routes file directory) │
│                                            and the routes config file into   │
│                                            and mount at runtime (example:    │
│                                            /website)                         │
│                                            [required]                        │
│    --help                                  Show this message and exit.       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent worker`

```console
$ meshagent worker --help
                                                                                
 Usage: meshagent worker [OPTIONS] COMMAND [ARGS]...                            
                                                                                
 Join a worker agent to a room                                                  
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ join     Join a room and run a worker agent.                                 │
│ service                                                                      │
│ spec     Generate a service spec for deploying a worker.                     │
│ deploy   Deploy a worker service to a project or room.                       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent worker join`

```console
$ meshagent worker join --help
                                                                                
 Usage: meshagent worker join [OPTIONS]                                         
                                                                                
 Join a room and run a worker agent.                                            
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --project-id                             TEXT             A MeshAgent     │
│                                                              project id. If  │
│                                                              empty, the      │
│                                                              activated       │
│                                                              project will be │
│                                                              used.           │
│                                                              [default:       │
│                                                              203b1bf9-72c9-… │
│ *  --room                                   TEXT             Room name       │
│                                                              [required]      │
│    --role                                   TEXT             [default:       │
│                                                              agent]          │
│    --agent-name                             TEXT             Name of the     │
│                                                              worker agent    │
│    --token-from-e…                          TEXT             Name of         │
│                                                              environment     │
│                                                              variable        │
│                                                              containing a    │
│                                                              MeshAgent token │
│    --rule           -r                      TEXT             a system rule   │
│    --rules-file                             TEXT                             │
│    --require-tool…  -rt                     TEXT             the name or url │
│                                                              of a required   │
│                                                              toolkit         │
│    --require-sche…  -rs                     TEXT             the name or url │
│                                                              of a required   │
│                                                              schema          │
│    --model                                  TEXT             Name of the LLM │
│                                                              model to use    │
│                                                              [default:       │
│                                                              gpt-5.4]        │
│    --threading-mo…                          [auto|manual|no  Threading mode: │
│                                             ne]              none (no        │
│                                                              persistence),   │
│                                                              manual (input   │
│                                                              path), or auto  │
│                                                              (LLM-selected   │
│                                                              thread path)    │
│                                                              [default: none] │
│    --thread-dir                             TEXT             Thread          │
│                                                              directory for   │
│                                                              auto mode;      │
│                                                              thread path is  │
│                                                              <thread_dir>/<… │
│                                                              [default:       │
│                                                              .threads]       │
│    --initial-mess…                          [summary|code|n  Initial thread  │
│                                             one]             message mode:   │
│                                                              summary (LLM    │
│                                                              summary), code  │
│                                                              (markdown code  │
│                                                              block), or none │
│                                                              [default: code] │
│    --initial-mess…                          TEXT             Author name     │
│                                                              used for the    │
│                                                              initial thread  │
│                                                              message         │
│                                                              [default:       │
│                                                              worker]         │
│    --decision-mod…                          TEXT             Model used for  │
│                                                              summary         │
│                                                              decisions and   │
│                                                              payload         │
│                                                              summarization   │
│    --require-shell       --no-require-s…                     Enable function │
│                                                              shell tool      │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-require-she… │
│    --require-loca…       --no-require-l…                     Enable local    │
│                                                              shell tool      │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-require-loc… │
│    --require-web-…       --no-require-w…                     Require web     │
│                                                              search tool     │
│                                                              [default:       │
│                                                              no-require-web… │
│    --require-web-…       --no-require-w…                     Require web     │
│                                                              fetch tool      │
│                                                              [default:       │
│                                                              no-require-web… │
│    --require-appl…       --no-require-a…                     Enable apply    │
│                                                              patch tool      │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-require-app… │
│    --key                                    TEXT             an api key to   │
│                                                              sign the token  │
│                                                              with            │
│ *  --queue                                  TEXT             the queue to    │
│                                                              consume         │
│                                                              [required]      │
│    --toolkit-name                           TEXT             optional        │
│                                                              toolkit name to │
│                                                              expose worker   │
│                                                              operations      │
│    --room-rules     -rr                     TEXT             path(s) in room │
│                                                              storage to load │
│                                                              rules from      │
│    --image-genera…                          TEXT             Name of an      │
│                                                              image gen model │
│    --local-shell         --no-local-she…                     Enable local    │
│                                                              shell tool      │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-local-shell] │
│    --shell               --no-shell                          Enable function │
│                                                              shell tool      │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-shell]       │
│    --apply-patch         --no-apply-pat…                     Enable apply    │
│                                                              patch tool      │
│                                                              [default:       │
│                                                              no-apply-patch] │
│    --web-search          --no-web-search                     Enable web      │
│                                                              search tool     │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-web-search]  │
│    --web-fetch           --no-web-fetch                      Enable web      │
│                                                              fetch tool      │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-web-fetch]   │
│    --discover-scr…       --no-discover-…                     Automatically   │
│                                                              add script      │
│                                                              tools from the  │
│                                                              room            │
│                                                              [default:       │
│                                                              no-discover-sc… │
│    --mcp                 --no-mcp                            Enable mcp tool │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-mcp]         │
│    --storage             --no-storage                        Enable storage  │
│                                                              toolkit         │
│                                                              [default:       │
│                                                              no-storage]     │
│    --storage-tool…                          TEXT             Mount local     │
│                                                              path as         │
│                                                              <source>:<moun… │
│    --storage-tool…                          TEXT             Mount room path │
│                                                              as              │
│                                                              <source>:<moun… │
│    --shell-room-m…                          TEXT             Mount room      │
│                                                              storage as      │
│                                                              <source>:<moun… │
│    --shell-projec…                          TEXT             Mount project   │
│                                                              storage as      │
│                                                              <source>:<moun… │
│    --shell-empty-…                          TEXT             Mount empty dir │
│                                                              at              │
│                                                              <mount>[:ro|rw] │
│    --shell-image-…                          TEXT             Mount image as  │
│                                                              <image>=<mount… │
│    --require-stor…       --no-require-s…                     Enable storage  │
│                                                              toolkit         │
│                                                              [default:       │
│                                                              no-require-sto… │
│    --require-read…       --no-require-r…                     Enable read     │
│                                                              only storage    │
│                                                              toolkit         │
│                                                              [default:       │
│                                                              no-require-rea… │
│    --require-time        --no-require-t…                     Enable          │
│                                                              time/datetime   │
│                                                              tools           │
│                                                              [default:       │
│                                                              require-time]   │
│    --require-uuid        --no-require-u…                     Enable UUID     │
│                                                              generation      │
│                                                              tools           │
│                                                              [default:       │
│                                                              no-require-uui… │
│    --use-memory                             TEXT             Use memories    │
│                                                              toolkit for     │
│                                                              <name> or       │
│                                                              <namespace>/<n… │
│    --memory-model                           TEXT             Model name for  │
│                                                              memory LLM      │
│                                                              ingestion       │
│    --database-nam…                          TEXT             Use a specific  │
│                                                              database        │
│                                                              namespace (JSON │
│                                                              list or dotted) │
│    --require-tabl…                          TEXT             Enable table    │
│                                                              read tools for  │
│                                                              these tables    │
│    --require-tabl…                          TEXT             Enable table    │
│                                                              write tools for │
│                                                              these tables    │
│    --require-comp…       --no-require-c…                     Enable computer │
│                                                              use             │
│                                                              [default:       │
│                                                              no-require-com… │
│    --starting-url                           TEXT             Initial URL to  │
│                                                              open when       │
│                                                              starting a      │
│                                                              computer-use    │
│                                                              browser session │
│    --allow-goto-u…                                           Expose the goto │
│                                                              URL helper tool │
│                                                              for computer    │
│                                                              use             │
│    --title                                  TEXT             a display name  │
│                                                              for the agent   │
│    --description                            TEXT             a description   │
│                                                              for the agent   │
│    --working-dir                            TEXT             The default     │
│                                                              working         │
│                                                              directory for   │
│                                                              shell commands  │
│    --skill-dir                              TEXT             an agent skills │
│                                                              directory       │
│    --shell-image                            TEXT             an image tag to │
│                                                              use to run      │
│                                                              shell commands  │
│                                                              in              │
│    --delegate-she…       --no-delegate-…                     Delegate the    │
│                                                              room token to   │
│                                                              shell tools     │
│                                                              [default:       │
│                                                              no-delegate-sh… │
│    --shell-copy-e…                          TEXT             Copy local env  │
│                                                              vars into shell │
│                                                              tool env.       │
│                                                              Accepts         │
│                                                              comma-separated │
│                                                              names and can   │
│                                                              be repeated.    │
│    --shell-set-env                          TEXT             Set env vars in │
│                                                              shell tool env  │
│                                                              as NAME=VALUE.  │
│                                                              Can be          │
│                                                              repeated.       │
│    --log-llm-requ…       --no-log-llm-r…                     log all         │
│                                                              requests to the │
│                                                              llm             │
│                                                              [default:       │
│                                                              no-log-llm-req… │
│    --prompt                                 TEXT             a prompt to use │
│                                                              for the worker  │
│    --help                                                    Show this       │
│                                                              message and     │
│                                                              exit.           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### `meshagent worker spec`

```console
$ meshagent worker spec --help
                                                                                
 Usage: meshagent worker spec [OPTIONS]                                         
                                                                                
 Generate a service spec for deploying a worker.                                
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --service-name                           TEXT             service name    │
│    --service-desc…                          TEXT             service         │
│                                                              description     │
│    --service-title                          TEXT             a display name  │
│                                                              for the service │
│ *  --agent-name                             TEXT             Name of the     │
│                                                              worker agent    │
│                                                              [required]      │
│    --rule           -r                      TEXT             a system rule   │
│    --rules-file                             TEXT                             │
│    --require-tool…  -rt                     TEXT             the name or url │
│                                                              of a required   │
│                                                              toolkit         │
│    --require-sche…  -rs                     TEXT             the name or url │
│                                                              of a required   │
│                                                              schema          │
│    --model                                  TEXT             Name of the LLM │
│                                                              model to use    │
│                                                              [default:       │
│                                                              gpt-5.4]        │
│    --threading-mo…                          [auto|manual|no  Threading mode: │
│                                             ne]              none (no        │
│                                                              persistence),   │
│                                                              manual (input   │
│                                                              path), or auto  │
│                                                              (LLM-selected   │
│                                                              thread path)    │
│                                                              [default: none] │
│    --thread-dir                             TEXT             Thread          │
│                                                              directory for   │
│                                                              auto mode;      │
│                                                              thread path is  │
│                                                              <thread_dir>/<… │
│                                                              [default:       │
│                                                              .threads]       │
│    --initial-mess…                          [summary|code|n  Initial thread  │
│                                             one]             message mode:   │
│                                                              summary (LLM    │
│                                                              summary), code  │
│                                                              (markdown code  │
│                                                              block), or none │
│                                                              [default: code] │
│    --initial-mess…                          TEXT             Author name     │
│                                                              used for the    │
│                                                              initial thread  │
│                                                              message         │
│                                                              [default:       │
│                                                              worker]         │
│    --decision-mod…                          TEXT             Model used for  │
│                                                              summary         │
│                                                              decisions and   │
│                                                              payload         │
│                                                              summarization   │
│    --image-genera…                          TEXT             Name of an      │
│                                                              image gen model │
│    --require-shell       --no-require-s…                     Enable function │
│                                                              shell tool      │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-require-she… │
│    --local-shell         --no-local-she…                     Enable local    │
│                                                              shell tool      │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-local-shell] │
│    --shell               --no-shell                          Enable function │
│                                                              shell tool      │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-shell]       │
│    --apply-patch         --no-apply-pat…                     Enable apply    │
│                                                              patch tool      │
│                                                              [default:       │
│                                                              no-apply-patch] │
│    --web-search          --no-web-search                     Enable web      │
│                                                              search tool     │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-web-search]  │
│    --web-fetch           --no-web-fetch                      Enable web      │
│                                                              fetch tool      │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-web-fetch]   │
│    --discover-scr…       --no-discover-…                     Automatically   │
│                                                              add script      │
│                                                              tools from the  │
│                                                              room            │
│                                                              [default:       │
│                                                              no-discover-sc… │
│    --mcp                 --no-mcp                            Enable mcp tool │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-mcp]         │
│    --storage             --no-storage                        Enable storage  │
│                                                              toolkit         │
│                                                              [default:       │
│                                                              no-storage]     │
│    --storage-tool…                          TEXT             Mount local     │
│                                                              path as         │
│                                                              <source>:<moun… │
│    --storage-tool…                          TEXT             Mount room path │
│                                                              as              │
│                                                              <source>:<moun… │
│    --require-loca…       --no-require-l…                     Require local   │
│                                                              shell tool      │
│                                                              [default:       │
│                                                              no-require-loc… │
│    --require-web-…       --no-require-w…                     Require web     │
│                                                              search tool     │
│                                                              [default:       │
│                                                              no-require-web… │
│    --require-web-…       --no-require-w…                     Require web     │
│                                                              fetch tool      │
│                                                              [default:       │
│                                                              no-require-web… │
│    --require-appl…       --no-require-a…                     Enable apply    │
│                                                              patch tool      │
│                                                              calling         │
│                                                              [default:       │
│                                                              no-require-app… │
│    --shell-room-m…                          TEXT             Mount room      │
│                                                              storage as      │
│                                                              <source>:<moun… │
│    --shell-projec…                          TEXT             Mount project   │
│                                                              storage as      │
│                                                              <source>:<moun… │
│    --shell-empty-…                          TEXT             Mount empty dir │
│                                                              at              │
│                                                              <mount>[:ro|rw] │
│    --shell-image-…                          TEXT             Mount image as  │
│                                                              <image>=<mount… │
│ *  --queue                                  TEXT             the queue to    │
│                                                              consume         │
│                                                              [required]      │
│    --toolkit-name                           TEXT             Toolkit name to │
│                                                              expose          │
│                                                              (optional)      │
│    --room-rules     -rr                     TEXT             Path(s) to      │
│                                                              rules files     │
│                                                              inside the room │
│    --require-stor…       --no-require-s…                     Require storage │
│                                                              toolkit         │
│                                                              [default:       │
│                                                              no-require-sto… │
│    --require-read…       --no-require-r…                     Require         │
│                                                              read-only       │
│                                                              storage toolkit │
│                                                              [default:       │
│                                                              no-require-rea… │
│    --require-time        --no-require-t…                     Enable          │
│                                                              time/datetime   │
│                                                              tools           │
│                                                              [default:       │
│                                                              require-time]   │
│    --require-uuid        --no-require-u…                     Enable UUID     │
│                                                              generation      │
│                                                              tools           │
│                                                              [default:       │
│                                                              no-require-uui… │
│    --use-memory                             TEXT             Use memories    │
│                                                              toolkit for     │
│                                                              <name> or       │
│                                                              <namespace>/<n… │
│    --memory-model                           TEXT             Model name for  │
│                                                              memory LLM      │
│                                                              ingestion       │
│    --database-nam…                          TEXT             Database        │
│                                                              namespace (e.g. │
│                                                              foo::bar)       │
│    --require-tabl…                          TEXT             Require table   │
│                                                              read tool for   │
│                                                              table           │
│                                                              (repeatable)    │
│    --require-tabl…                          TEXT             Require table   │
│                                                              write tool for  │
│                                                              table           │
│                                                              (repeatable)    │
│    --require-comp…       --no-require-c…                     Enable computer │
│                                                              use             │
│                                                              [default:       │
│                                                              no-require-com… │
│    --starting-url                           TEXT             Initial URL to  │
│                                                              open when       │
│                                                              starting a      │
│                                                              computer-use    │
│                                                              browser session │
│    --allow-goto-u…                                           Expose the goto │
│                                                              URL helper tool │
│                                                              for computer    │
│                                                              use             │
│    --title                                  TEXT             a display name  │
│                                                              for the agent   │
│    --description                            TEXT             a description   │
│                                                              for the agent   │
│    --working-dir                            TEXT             The default     │
│                                                              working         │
│                                                              directory for   │
│                                                              shell commands  │
│    --skill-dir                              TEXT             an agent skills │
│                                                              directory       │
│    --shell-image                            TEXT             an image tag to │
│                                                              use to run      │
│                                                              shell commands  │
│                                                              in              │
│    --delegate-she…       --no-delegate-…                     Delegate the    │
│                                                              room token to   │
│                                                              shell tools     │
│                                                              [default:       │
│                                                              no-delegate-sh… │
│    --shell-copy-e…                          TEXT             Copy local env  │
│                                                              vars into shell │
│                                                              tool env.       │
│                                                              Accepts         │
│                                                              comma-separated │
│                                                              names and can   │
│                                                              be repeated.    │
│    --shell-set-env                          TEXT             Set env vars in │
│                                                              shell tool env  │
│                                                              as NAME=VALUE.  │
│                                                              Can be          │
│                                                              repeated.       │
│    --log-llm-requ…       --no-log-llm-r…                     log all         │
│                                                              requests to the │
│                                                              llm             │
│                                                              [default:       │
│                                                              no-log-llm-req… │
│    --prompt                                 TEXT             a prompt to use │
│                                                              for the worker  │
│    --help                                                    Show this       │
│                                                              message and     │
│                                                              exit.           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## `meshagent multi`

```console
$ meshagent multi --help
                                                                                
 Usage: meshagent multi [OPTIONS] COMMAND [ARGS]...                             
                                                                                
 Connect agents and tools to a room                                             
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ spec     Generate a combined service spec from multiple subcommands.         │
│ deploy   Deploy a combined service from multiple subcommands.                │
│ service                                                                      │
│ join     Run multiple join commands together in one process.                 │
╰──────────────────────────────────────────────────────────────────────────────╯
```
