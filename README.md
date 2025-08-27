# tuna-fusion-agent-samples  

This repository contains sample agent implementations to demonstrate the workflow to deploy agents to `tuna-fusion` runtime.

The following instruction assume you have a properly installed `tuna-fusion` instance. And you can access:

* the GitOps server by `tuna-fusion-gitops-server.default.svc.cluster.local` on port 80
* the executor server by `tuna-fusion-executor.default.svc.cluster.local` on port 80

You can learn more about installation at [project homepage](https://tuna-headquater.github.io/tuna-fusion/latest/).

Before continue, please make sure you have initialized submodules of this repository:


```shell
git submodule update --init --recursive
```


## Migrated samples from `a2a-samples` project

These agents have less code lines and are easy to understand. You use these agents as a start point to validate the deployment workflow. 


| Name                      | Description                                                               | Agent framework |
|---------------------------|---------------------------------------------------------------------------|-----------------|
| helloworld                | Prints "Hello World" in response events                                   | None            |
| travel_planner_agent      | Agents configured with system prompts as travel advisor                   | None            |
| langgraph                 | Simple agent based on LangGraph                                           | LangGraph       |
| semantickernel            | Simple agent based on Semantic Kernel                                     | Semantic Kernel |
| a2a-mcp-without-framework | Simple agent answering questions about a2a protocol using `gitmcp` server | None            |


## Deployment

### Prepare the environment

Create the namespace first:

```shell
kubectl apply -f a2a-samples-ns.yaml
```

Edit `a2a-samples-env.yaml` for global env vars setups. All credentials and settings should be set for Google Gemini, OpenAPI and AzureAI. As the official repo of `a2a-samples` uses one of these services.

Then apply the `AgentEnvironment`:

```shell
kubectl apply -f a2a-samples-env.yaml
```


### Deploy the agents

`AgentDeployment` resource files are located in [thirdparty/a2a-samples-resources](thirdparty/a2a-samples-resources) directory. Let's take `helloworld` agent as an example as it's the only agents that has no extra requirements for credentials of model providers.

First apply the `AgentDeployment` first:

```shell
kubectl apply -f thirdparty/a2a-samples-resources/helloworld.yaml
```

Then add Git remote for `AgentDeployment`'s virtual repository:

```shell
git remote add helloworld http://tuna-fusion-gitops-server.default.svc.cluster.local/repostiroies/namespaces/a2a-samples-ns/agents/helloworld.git
```

Trigger build pipeline for the agent with a git push:

```shell
git add .
git commit -am 'feat: first commit'
```

Example output would be:

```terminaloutput
% git push helloworld
Enumerating objects: 50, done.
Counting objects: 100% (50/50), done.
Delta compression using up to 16 threads
Compressing objects: 100% (40/40), done.
Writing objects: 100% (50/50), 10.57 KiB | 10.57 MiB/s, done.
Total 50 (delta 10), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (10/10)
remote: 🪝 PreReceive Hook called at dir /private/var/folders/hr/4rmk0wyj2t5f2n2j0gw7cfb80000gn/T/gitops2240336506831945185/namespaces/a2a-samples-ns/agents/helloworld.git
remote: Updating references: 100% (1/1)
remote: 🪝 Post receive hook called at dir /private/var/folders/hr/4rmk0wyj2t5f2n2j0gw7cfb80000gn/T/gitops2240336506831945185/namespaces/a2a-samples-ns/agents/helloworld.git
remote: Snapshot created: /var/folders/hr/4rmk0wyj2t5f2n2j0gw7cfb80000gn/T/9b9d431c-f1b9-49b3-a340-46ceba4d953b15923316318943637253
remote: 📦 SourceArchive for repository is created successfully: PodFunctionBuildSpec.SourceArchive(httpZipSource=PodFunction.HttpZipSource(url=http://host.docker.internal:8081/source_archives/d24a7d4d-831d-4c5c-9d3d-01fb657c5859, sha256Checksum=1d43f0bde93f0ded1d6635661d14cffc4e4befca60ea0bcf4c45f6e5ab0a38f7), filesystemZipSource=null, filesystemFolderSource=null)
remote: 💾 FunctionBuild CR is created successfully: helloworld-build-1756258242
remote: ⚒️ Job pod is created successfully: helloworld-build-1756258242-job-wgfx5
remote: + echo Run pre_build.py
remote: Run pre_build.py
remote: + python -m fusion_builder.pre_build
remote: DEBUG:asyncio:Using selector: EpollSelector
remote: INFO:__main__:Configure with http zip source: url='http://host.docker.internal:8081/source_archives/d24a7d4d-831d-4c5c-9d3d-01fb657c5859' sha256Checksum='1d43f0bde93f0ded1d6635661d14cffc4e4befca60ea0bcf4c45f6e5ab0a38f7'
remote: INFO:__main__:Downloading source archive http://host.docker.internal:8081/source_archives/d24a7d4d-831d-4c5c-9d3d-01fb657c5859 to /tmp/tmp1awk_roi
remote: DEBUG:httpcore.connection:connect_tcp.started host='host.docker.internal' port=8081 local_address=None timeout=5.0 socket_options=None
remote: DEBUG:httpcore.connection:connect_tcp.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0xffffa664acf0>
remote: DEBUG:httpcore.http11:send_request_headers.started request=<Request [b'GET']>
remote: DEBUG:httpcore.http11:send_request_headers.complete
remote: DEBUG:httpcore.http11:send_request_body.started request=<Request [b'GET']>
remote: DEBUG:httpcore.http11:send_request_body.complete
remote: DEBUG:httpcore.http11:receive_response_headers.started request=<Request [b'GET']>
remote: DEBUG:httpcore.http11:receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'', [(b'Content-Disposition', b'attachment; filename="d24a7d4d-831d-4c5c-9d3d-01fb657c5859.zip"'), (b'Accept-Ranges', b'bytes'), (b'Content-Type', b'application/json'), (b'Content-Length', b'64658'), (b'Date', b'Wed, 27 Aug 2025 01:30:44 GMT'), (b'Keep-Alive', b'timeout=60'), (b'Connection', b'keep-alive')])
remote: INFO:httpx:HTTP Request: GET http://host.docker.internal:8081/source_archives/d24a7d4d-831d-4c5c-9d3d-01fb657c5859 "HTTP/1.1 200 "
remote: DEBUG:httpcore.http11:receive_response_body.started request=<Request [b'GET']>
remote: DEBUG:httpcore.http11:receive_response_body.complete
remote: DEBUG:httpcore.http11:response_closed.started
remote: DEBUG:httpcore.http11:response_closed.complete
remote: INFO:__main__:Successfully verified SHA256 checksum of the downloaded file
remote: INFO:__main__:Extracting source archive to /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac
remote: DEBUG:httpcore.connection:close.started
remote: DEBUG:httpcore.connection:close.complete
remote: Copy source to deploy
remote: + echo Copy source to deploy
remote: + mkdir -p /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac
remote: + cp -r /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/Containerfile /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/README.md /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/__init__.py /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/__main__.py /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/agent_executor.py /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/test_client.py /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/uv.lock /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac/
remote: + [ -f /workspace/patch_source.sh ]
remote: + echo Patch sources
remote: Patch sources
remote: + sh /workspace/patch_source.sh
remote: + mkdir -p /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac
remote: + cp -f /patch/agent_card.json /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac/agent_card.json
remote: + cp -f /patch/a2a_runtime.json /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac/a2a_runtime.json
remote: + [ -d /configmaps/a2a-samples-ns/helloworld ]
remote: + cp -r /configmaps/a2a-samples-ns/helloworld /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac/configmaps
remote: + [ -d /configmaps/a2a-samples-ns/helloworld ]
remote: + cp -r /configmaps/a2a-samples-ns/helloworld /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac/configmaps
remote: Attempt to install deps
remote: + [ -f /workspace/build_source.sh ]
remote: + echo Attempt to install deps
remote: + [ -f /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/requirements.txt ]
remote: + [ -f /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml ]
remote: + uv pip compile -o /tmp/requirements.txt /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml
remote: Resolved 53 packages in 2.02s
remote: # This file was autogenerated by uv via the following command:
remote: #    uv pip compile -o /tmp/requirements.txt /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml
remote: a2a-sdk==0.3.3
remote:     # via helloworld (/archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml)
remote: annotated-types==0.7.0
remote:     # via pydantic
remote: anyio==4.10.0
remote:     # via
remote:     #   httpx
remote:     #   sse-starlette
remote:     #   starlette
remote: cachetools==5.5.2
remote:     # via google-auth
remote: certifi==2025.8.3
remote:     # via
remote:     #   httpcore
remote:     #   httpx
remote:     #   requests
remote: charset-normalizer==3.4.3
remote:     # via requests
remote: click==8.2.1
remote:     # via
remote:     #   helloworld (/archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml)
remote:     #   uvicorn
remote: dotenv==0.9.9
remote:     # via helloworld (/archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml)
remote: filetype==1.2.0
remote:     # via langchain-google-genai
remote: google-ai-generativelanguage==0.6.18
remote:     # via langchain-google-genai
remote: google-api-core==2.25.1
remote:     # via
remote:     #   a2a-sdk
remote:     #   google-ai-generativelanguage
remote: google-auth==2.40.3
remote:     # via
remote:     #   google-ai-generativelanguage
remote:     #   google-api-core
remote: googleapis-common-protos==1.70.0
remote:     # via
remote:     #   google-api-core
remote:     #   grpcio-status
remote: grpcio==1.74.0
remote:     # via
remote:     #   google-api-core
remote:     #   grpcio-status
remote: grpcio-status==1.74.0
remote:     # via google-api-core
remote: h11==0.16.0
remote:     # via
remote:     #   httpcore
remote:     #   uvicorn
remote: httpcore==1.0.9
remote:     # via httpx
remote: httpx==0.28.1
remote:     # via
remote:     #   helloworld (/archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml)
remote:     #   a2a-sdk
remote:     #   langgraph-sdk
remote:     #   langsmith
remote: httpx-sse==0.4.1
remote:     # via a2a-sdk
remote: idna==3.10
remote:     # via
remote:     #   anyio
remote:     #   httpx
remote:     #   requests
remote: jsonpatch==1.33
remote:     # via langchain-core
remote: jsonpointer==3.0.0
remote:     # via jsonpatch
remote: langchain-core==0.3.75
remote:     # via
remote:     #   langchain-google-genai
remote:     #   langgraph
remote:     #   langgraph-checkpoint
remote:     #   langgraph-prebuilt
remote: langchain-google-genai==2.1.9
remote:     # via helloworld (/archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml)
remote: langgraph==0.6.6
remote:     # via helloworld (/archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml)
remote: langgraph-checkpoint==2.1.1
remote:     # via
remote:     #   langgraph
remote:     #   langgraph-prebuilt
remote: langgraph-prebuilt==0.6.4
remote:     # via langgraph
remote: langgraph-sdk==0.2.3
remote:     # via langgraph
remote: langsmith==0.4.18
remote:     # via langchain-core
remote: orjson==3.11.3
remote:     # via
remote:     #   langgraph-sdk
remote:     #   langsmith
remote: ormsgpack==1.10.0
remote:     # via langgraph-checkpoint
remote: packaging==25.0
remote:     # via
remote:     #   langchain-core
remote:     #   langsmith
remote: proto-plus==1.26.1
remote:     # via
remote:     #   google-ai-generativelanguage
remote:     #   google-api-core
remote: protobuf==6.32.0
remote:     # via
remote:     #   a2a-sdk
remote:     #   google-ai-generativelanguage
remote:     #   google-api-core
remote:     #   googleapis-common-protos
remote:     #   grpcio-status
remote:     #   proto-plus
remote: pyasn1==0.6.1
remote:     # via
remote:     #   pyasn1-modules
remote:     #   rsa
remote: pyasn1-modules==0.4.2
remote:     # via google-auth
remote: pydantic==2.11.7
remote:     # via
remote:     #   helloworld (/archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml)
remote:     #   a2a-sdk
remote:     #   langchain-core
remote:     #   langchain-google-genai
remote:     #   langgraph
remote:     #   langsmith
remote: pydantic-core==2.33.2
remote:     # via pydantic
remote: python-dotenv==1.1.1
remote:     # via
remote:     #   helloworld (/archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml)
remote:     #   dotenv
remote: pyyaml==6.0.2
remote:     # via langchain-core
remote: requests==2.32.5
remote:     # via
remote:     #   google-api-core
remote:     #   langsmith
remote:     #   requests-toolbelt
remote: requests-toolbelt==1.0.0
remote:     # via langsmith
remote: rsa==4.9.1
remote:     # via google-auth
remote: sniffio==1.3.1
remote:     # via anyio
remote: sse-starlette==3.0.2
remote:     # via helloworld (/archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml)
remote: starlette==0.47.3
remote:     # via helloworld (/archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml)
remote: tenacity==9.1.2
remote:     # via langchain-core
remote: typing-extensions==4.15.0
remote:     # via
remote:     #   langchain-core
remote:     #   pydantic
remote:     #   pydantic-core
remote:     #   typing-inspection
remote: typing-inspection==0.4.1
remote:     # via pydantic
remote: urllib3==2.5.0
remote:     # via requests
remote: uvicorn==0.35.0
remote:     # via helloworld (/archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml)
remote: xxhash==3.5.0
remote:     # via langgraph
remote: zstandard==0.24.0
remote:     # via langsmith
remote: + uv pip install --link-mode=copy -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple -r /tmp/requirements.txt --target /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac
remote: Using CPython 3.13.4 interpreter at: .venv/bin/python
remote: Resolved 53 packages in 1.48s
remote: Downloading grpcio (5.7MiB)
remote: Downloading zstandard (4.8MiB)
remote: Downloading google-ai-generativelanguage (1.3MiB)
remote:  Downloading google-ai-generativelanguage
remote:  Downloading zstandard
remote:  Downloading grpcio
remote: Prepared 37 packages in 1.06s
remote: Installed 53 packages in 62ms
remote:  + a2a-sdk==0.3.3
remote:  + annotated-types==0.7.0
remote:  + anyio==4.10.0
remote:  + cachetools==5.5.2
remote:  + certifi==2025.8.3
remote:  + charset-normalizer==3.4.3
remote:  + click==8.2.1
remote:  + dotenv==0.9.9
remote:  + filetype==1.2.0
remote:  + google-ai-generativelanguage==0.6.18
remote:  + google-api-core==2.25.1
remote:  + google-auth==2.40.3
remote:  + googleapis-common-protos==1.70.0
remote:  + grpcio==1.74.0
remote:  + grpcio-status==1.74.0
remote:  + h11==0.16.0
remote:  + httpcore==1.0.9
remote:  + httpx==0.28.1
remote:  + httpx-sse==0.4.1
remote:  + idna==3.10
remote:  + jsonpatch==1.33
remote:  + jsonpointer==3.0.0
remote:  + langchain-core==0.3.75
remote:  + langchain-google-genai==2.1.9
remote:  + langgraph==0.6.6
remote:  + langgraph-checkpoint==2.1.1
remote:  + langgraph-prebuilt==0.6.4
remote:  + langgraph-sdk==0.2.3
remote:  + langsmith==0.4.18
remote:  + orjson==3.11.3
remote:  + ormsgpack==1.10.0
remote:  + packaging==25.0
remote:  + proto-plus==1.26.1
remote:  + protobuf==6.32.0
remote:  + pyasn1==0.6.1
remote:  + pyasn1-modules==0.4.2
remote:  + pydantic==2.11.7
remote:  + pydantic-core==2.33.2
remote:  + python-dotenv==1.1.1
remote:  + pyyaml==6.0.2
remote:  + requests==2.32.5
remote:  + requests-toolbelt==1.0.0
remote:  + rsa==4.9.1
remote:  + sniffio==1.3.1
remote:  + sse-starlette==3.0.2
remote:  + starlette==0.47.3
remote:  + tenacity==9.1.2
remote:  + typing-extensions==4.15.0
remote:  + typing-inspection==0.4.1
remote:  + urllib3==2.5.0
remote:  + uvicorn==0.35.0
remote:  + xxhash==3.5.0
remote:  + zstandard==0.24.0
remote: Run post_build.py
remote: + echo Run post_build.py
remote: + python -m fusion_builder.post_build
remote: DEBUG:asyncio:Using selector: EpollSelector
remote: kube_config_path not provided and default location (~/.kube/config) does not exist. Using inCluster Config. This might not work.
remote: DEBUG:kubernetes.client.rest:response body: {"apiVersion":"fusion.tuna.ai/v1","kind":"PodFunctionBuild","metadata":{"creationTimestamp":"2025-08-27T01:30:42Z","finalizers":["podfunctionbuilds.fusion.tuna.ai/finalizer"],"generation":1,"managedFields":[{"apiVersion":"fusion.tuna.ai/v1","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:finalizers":{"v:\"podfunctionbuilds.fusion.tuna.ai/finalizer\"":{}},"f:ownerReferences":{"k:{\"uid\":\"1a6b6283-a7a8-4beb-963e-e95b1b4c8ba8\"}":{}}}},"manager":"podFunctionBuildReconciler","operation":"Apply","time":"2025-08-27T01:30:44Z"},{"apiVersion":"fusion.tuna.ai/v1","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:finalizers":{"v:\"podfunctionbuilds.fusion.tuna.ai/finalizer\"":{}},"f:ownerReferences":{"k:{\"uid\":\"1a6b6283-a7a8-4beb-963e-e95b1b4c8ba8\"}":{}}},"f:status":{"f:jobPod":{"f:logs":{},"f:podName":{},"f:podPhase":{}},"f:phase":{}}},"manager":"podFunctionBuildReconciler","operation":"Apply","subresource":"status","time":"2025-08-27T01:30:44Z"},{"apiVersion":"fusion.tuna.ai/v1","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:ownerReferences":{".":{},"k:{\"uid\":\"1a6b6283-a7a8-4beb-963e-e95b1b4c8ba8\"}":{}}},"f:spec":{".":{},"f:podFunctionName":{},"f:sourceArchive":{".":{},"f:httpZipSource":{".":{},"f:sha256Checksum":{},"f:url":{}}},"f:ttlSecondsAfterFinished":{}}},"manager":"fabric8-kubernetes-client","operation":"Update","time":"2025-08-27T01:30:42Z"},{"apiVersion":"fusion.tuna.ai/v1","fieldsType":"FieldsV1","fieldsV1":{"f:status":{"f:deployArchive":{".":{},"f:filesystemFolderSource":{".":{},"f:path":{}}}}},"manager":"OpenAPI-Generator","operation":"Update","subresource":"status","time":"2025-08-27T01:30:49Z"}],"name":"helloworld-build-1756258242","namespace":"a2a-samples-ns","ownerReferences":[{"apiVersion":"fusion.tuna.ai/v1","blockOwnerDeletion":false,"controller":true,"kind":"PodFunction","name":"helloworld-function","uid":"1a6b6283-a7a8-4beb-963e-e95b1b4c8ba8"}],"resourceVersion":"2757547","uid":"ab3e29f8-855c-45cc-9938-93d9844599ac"},"spec":{"podFunctionName":"helloworld-function","sourceArchive":{"httpZipSource":{"sha256Checksum":"1d43f0bde93f0ded1d6635661d14cffc4e4befca60ea0bcf4c45f6e5ab0a38f7","url":"http://host.docker.internal:8081/source_archives/d24a7d4d-831d-4c5c-9d3d-01fb657c5859"}},"ttlSecondsAfterFinished":600},"status":{"deployArchive":{"filesystemFolderSource":{"path":"/archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac"}},"jobPod":{"logs":"+ echo Run pre_build.py\nRun pre_build.py\n+ python -m fusion_builder.pre_build\nDEBUG:asyncio:Using selector: EpollSelector\nINFO:__main__:Configure with http zip source: url='http://host.docker.internal:8081/source_archives/d24a7d4d-831d-4c5c-9d3d-01fb657c5859' sha256Checksum='1d43f0bde93f0ded1d6635661d14cffc4e4befca60ea0bcf4c45f6e5ab0a38f7'\nINFO:__main__:Downloading source archive http://host.docker.internal:8081/source_archives/d24a7d4d-831d-4c5c-9d3d-01fb657c5859 to /tmp/tmp1awk_roi\nDEBUG:httpcore.connection:connect_tcp.started host='host.docker.internal' port=8081 local_address=None timeout=5.0 socket_options=None\nDEBUG:httpcore.connection:connect_tcp.complete return_value=\u003chttpcore._backends.anyio.AnyIOStream object at 0xffffa664acf0\u003e\nDEBUG:httpcore.http11:send_request_headers.started request=\u003cRequest [b'GET']\u003e\nDEBUG:httpcore.http11:send_request_headers.complete\nDEBUG:httpcore.http11:send_request_body.started request=\u003cRequest [b'GET']\u003e\nDEBUG:httpcore.http11:send_request_body.complete\nDEBUG:httpcore.http11:receive_response_headers.started request=\u003cRequest [b'GET']\u003e\nDEBUG:httpcore.http11:receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'', [(b'Content-Disposition', b'attachment; filename=\"d24a7d4d-831d-4c5c-9d3d-01fb657c5859.zip\"'), (b'Accept-Ranges', b'bytes'), (b'Content-Type', b'application/json'), (b'Content-Length', b'64658'), (b'Date', b'Wed, 27 Aug 2025 01:30:44 GMT'), (b'Keep-Alive', b'timeout=60'), (b'Connection', b'keep-alive')])\nINFO:httpx:HTTP Request: GET http://host.docker.internal:8081/source_archives/d24a7d4d-831d-4c5c-9d3d-01fb657c5859 \"HTTP/1.1 200 \"\nDEBUG:httpcore.http11:receive_response_body.started request=\u003cRequest [b'GET']\u003e\nDEBUG:httpcore.http11:receive_response_body.complete\nDEBUG:httpcore.http11:response_closed.started\nDEBUG:httpcore.http11:response_closed.complete\nINFO:__main__:Successfully verified SHA256 checksum of the downloaded file\nINFO:__main__:Extracting source archive to /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac\nDEBUG:httpcore.connection:close.started\nDEBUG:httpcore.connection:close.complete\nCopy source to deploy\n+ echo Copy source to deploy\n+ mkdir -p /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac\n+ cp -r /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/Containerfile /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/README.md /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/__init__.py /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/__main__.py /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/agent_executor.py /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/test_client.py /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/uv.lock /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac/\n+ [ -f /workspace/patch_source.sh ]\n+ echo Patch sources\nPatch sources\n+ sh /workspace/patch_source.sh\n+ mkdir -p /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac\n+ cp -f /patch/agent_card.json /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac/agent_card.json\n+ cp -f /patch/a2a_runtime.json /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac/a2a_runtime.json\n+ [ -d /configmaps/a2a-samples-ns/helloworld ]\n+ cp -r /configmaps/a2a-samples-ns/helloworld /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac/configmaps\n+ [ -d /configmaps/a2a-samples-ns/helloworld ]\n+ cp -r /configmaps/a2a-samples-ns/helloworld /archive/deployments/ab3e29f8-855c-45cc-9938-93d9844599ac/configmaps\nAttempt to install deps\n+ [ -f /workspace/build_source.sh ]\n+ echo Attempt to install deps\n+ [ -f /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/requirements.txt ]\n+ [ -f /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml ]\n+ uv pip compile -o /tmp/requirements.txt /archive/sources/ab3e29f8-855c-45cc-9938-93d9844599ac/pyproject.toml\n","podName":"helloworld-build-1756258242-job-wgfx5","podPhase":"Running"},"phase":"Running"}}
remote:
remote: + echo Done!
remote: Done!
remote: ⏳ Waiting for final status of PodFunctionBuild with timeout of 3 mins
remote: ✅ FunctionBuild CR is completed successfully
To http://localhost:8081/repositories/namespaces/a2a-samples-ns/agents/helloworld.git
 * [new branch]      main -> main
```


### Agent endpoints

You can notice output indicates that `FunctionBuild` CR is completed successfully. So you can access this simple agent through `executor` endpoint:

```text
http://tuna-fusion-executor.default.svc.cluster.local/a2a/namespaces/a2a-samples-ns/agents/helloworld/
```

To be specific, The agent is ready to be used at:

```text
http://tuna-fusion-executor.default.svc.cluster.local/a2a/namespaces/a2a-samples-ns/agents/helloworld/.well-known/agent.json
```


