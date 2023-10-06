# sdnext-dynamic
This wraps our SDNext image with an entrypoint script that downloads a checkpoint based on an environment variable.

You can use the prebuild docker image as:
```
saladtechnologies/sdnext:dynamic
```

## Environment Variables
| Variable | Description | Default |
| -------- | ----------- | ------- |
| HOST | The host to listen on | 0.0.0.0 |
| PORT | The port to listen on | 7860 |
| CIVITAI_MODEL_VERSION_IDS | A comma-separated list of model version IDs to download. | None |
| LOAD_REFINER | If set to `1`, the SDXL refiner model will be downloaded. | 0 |
| CLI_ARGS | Additional arguments to pass to the `sdnext` launch command. Options can be found with `--help` | None |

## Finding Your Model Version ID (Website)

1. Navigate to the Civit.ai page for the model you want to use
![](images/image1.png)

2. Click the version of the model you want to download
![](images/image2.png)

3. Copy the version ID from the URL
![](images/image3.png)

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