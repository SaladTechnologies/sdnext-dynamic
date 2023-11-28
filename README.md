# sdnext-dynamic
This wraps our SDNext image with an entrypoint script that downloads a checkpoint at runtime based on an environment variable.

You can use the prebuilt docker image at:
```
saladtechnologies/sdnext:dynamic
```
### "Baked" Images
If you want an image with the model preloaded, you can use one of the "baked" images. These are built with the `build-baked` script, and will not need to download the models at runtime.

- `saladtechnologies/sdnext:sdxl1.0` - Preloaded with SDXL [Base](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) and [Refiner](https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0)
- `saladtechnologies/sdnext:dreamshaper8` - Preloaded with [DreamShaper 8](https://civitai.com/models/4384?modelVersionId=128713)
- `saladtechnologies/sdnext:rundiffusionxl-beta` - Preloaded with [RunDiffusion XL Beta](https://civitai.com/models/120964?modelVersionId=131579) and [SDXL Refiner](https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0)

## Build your own image

### Without a model preloaded

The "baked" images use this one as a base

```shell
## Usage: ./build [--push]
./scripts/build
```

### With a model preloaded

```shell
# Usage: ./build [--push] [--civitai-version-ids 122143,128713] [--load-refiner] [--load-sdxl-base] [--tag tag]
./scripts/build-baked --civitai-version-ids 122143,128713
```

### Original SDXL + Refiner

```shell
./scripts/build-sdxl
```

## Environment Variables
| Variable | Description | Default |
| -------- | ----------- | ------- |
| HOST | The host to listen on. Use `[::]` on Salad. You may need to use an ipv4 address like `0.0.0.0` for local development | `[::]` |
| PORT | The port to listen on. This should match the port you configure for Salad networking. | 7860 |
| CIVITAI_MODEL_VERSION_IDS | A comma-separated list of model version IDs to download. ex `128713` for just [Dreamshaper 8](https://civitai.com/models/4384?modelVersionId=128713) or `128713,166808` for Dreamshaper and [Arterior](https://civitai.com/models/112229/arterior-digital-art-style). This supports Checkpoints, VAEs, and Controlnets. The rightmost checkpoint value will be the default checkpoint when the server starts, and the rightmost vae value will be the default vae when the server starts. | None |
| LOAD_SDXL_BASE | If set to `1`, the SDXL base model will be downloaded. | 0 |
| LOAD_REFINER | If set to `1`, the SDXL refiner model will be downloaded. | 0 |
| CLI_ARGS | Additional arguments to pass to the `sdnext` launch command. Options can be found with `--help` | None |
| EXTENSIONS | A comma separated list of extensions to load, each in the format of `name\|repoUrl`. e.g. `deforum\|https://github.com/deforum-art/sd-webui-deforum`  | None |

## Built-in Exec Probes
An exec probe is a command that is run periodically to check the health or readiness of the container. It returns a zero exit code if the container is healthy, and a non-zero exit code if the container is unhealthy. You can configure the maximum number of retries and the interval between retries using either the portal or the [Create Container Group API](https://docs.salad.com/reference/create_container_group). Learn more about health probes in [the docs](https://docs.salad.com/docs/health-probes).

### Startup Probe

This probe will return a zero exit code when the server is ready to accept connections. It will return a non-zero exit code if the server is not ready to accept connections.  Keep in mind it can take quite a while to download the models, so be sure to set a generous number of retries and a long interval, or your container will never start taking traffic, and will be continually reallocated.

**Portal**
```shell
python /probes/readiness.py
```

**API**
```json
["python", "/probes/readiness.py"]
```

### Liveness Probe

This probe will return a zero exit code when the server has not encountered any memory problems. It will return a non-zero exit code if the server has run out of, or is about to run out of, memory.

**Portal**
```shell
python /probes/healthcheck.py
```

**API**
```json
["python", "/probes/healthcheck.py"]
```

## Finding Your Model Version ID (Website)

1. Navigate to the Civit.ai page for the model you want to use
![](images/image1.png)

2. Click the version of the model you want to download
![](images/image2.png)

3. Copy the version ID from the URL
![](images/image3.png)

**OR**

2. Copy the link from the download button
![](images/image5.png)

3. Paste the link into a text editor and copy the model version ID from the URL
```
https://civitai.com/api/download/models/128713
```

For this url, the model version id is `128713`.

## Finding Your Model Version ID (API)

1. Navigate to the Civit.ai page for the model you want to use
![](images/image1.png)

2. Grab the model ID from the URL
![](images/image4.png)

3. Use the API to get the model versions
```shell
curl  -X GET \
  'https://civitai.com/api/v1/models/4384'
```

You'll get a JSON response that includes a `.modelVersions` field:

```
"modelVersions": [
    {
      "id": 128713,
      "modelId": 4384,
      "name": "8",
      "createdAt": "2023-07-29T15:56:46.392Z",
      "updatedAt": "2023-08-01T13:38:21.400Z",
      "trainedWords": [],
      "trainingStatus": null,
      "trainingDetails": null,
      "baseModel": "SD 1.5",
      "baseModelType": "Standard",
      "earlyAccessTimeFrame": 0,
      "description": "<ul><li><p>Better at handling Character LoRA</p></li><li><p>Better at photorealism without sacrificing range (can still do art and anime pretty well, even if you might have to increase weight)</p></li><li><p>Better at NSFW</p></li></ul>",
      "vaeId": null,
      "stats": {
        "downloadCount": 157806,
        "ratingCount": 673,
        "rating": 4.9
      },
      "files": []
      ...
    }
]
```

Find the model version you want to use and copy the `id` field.


## Deploying on Salad (Portal)

As an example, we're going to deploy the Dreamshaper XL model

### Create a Deployment

![](images/setup1.png)

1. Name your deployment
2. Select the `saladtechnologies/sdnext:dynamic` image
3. Select how many vCPUs you need. For this we'll use 2
4. Select how much RAM you need. Since we plan on using the refiner model, we'll use 30GB

![](images/setup2.png)

5. Select your GPUs. For an SDXL based model, we'll want GPUs with at least 16GB of VRAM.

![](images/setup3.png)

6. Click "edit" on the Networking section, and enable networking for port 7860 (the default port for SDNext).

![](images/setup4.png)

7. Click "edit" on the Environment Variables section, and add the following variables:
    - `HOST` with a value of `[::]`
    - `CIVITAI_MODEL_VERSION_IDS` with a value of `126688`
    - `LOAD_REFINER` with a value of `1`

![](images/setup5.png)

8. Click "Deploy" to finish creating your deployment. Then, click "Start" to start it.

### Your Finished Deployment

![](images/deployment-info.png)

With the environment configured like this:

![](images/deployed-env.png)
