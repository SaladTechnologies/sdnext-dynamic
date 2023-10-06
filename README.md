# sdnext-dynamic
This wraps our SDNext image with an entrypoint script that downloads a checkpoint based on an environment variable.

You can use the prebuild docker image as:
```
saladtechnologies/sdnext:dynamic
```

## Environment Variables
| Variable | Description | Default |
| -------- | ----------- | ------- |
| HOST | The host to listen on. Use `[::]` on Salad. | 0.0.0.0 |
| PORT | The port to listen on. This should match the port you configure for Salad networking. | 7860 |
| CIVITAI_MODEL_VERSION_IDS | A comma-separated list of model version IDs to download. ex `128713` for just [Dreamshaper 8](https://civitai.com/models/4384?modelVersionId=128713) or `128713,166808` for Dreamshaper and [Arterior](https://civitai.com/models/112229/arterior-digital-art-style). The rightmost value will be the default checkpoint when the server starts. | None |
| LOAD_REFINER | If set to `1`, the SDXL refiner model will be downloaded. | 0 |
| CLI_ARGS | Additional arguments to pass to the `sdnext` launch command. Options can be found with `--help` | None |

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