<div align="center">
  <a href="https://github.com/HideyoshiNakazone/hideyoshi.com">
    <img src="https://drive.google.com/uc?export=view&id=1ka1kTMcloX_wjAlKLET9VoaRTyRuGmxQ" width="100" height="100" allow="autoplay"\>
  </a>
</div>

# storage-hideyoshi.com

Made for managing files in Storage Services, currently only supporting AWS S3. This project was made for the [hideyoshi.com project](https://github.com/HideyoshiNakazone/hideyoshi.com), but all code in this repo is distributed freely by the GPLv3 License.

This project implements endpoints for manipulation of files in Storage Services and implements a worker for treatment of files and virus checking.
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- Server Configuration:

    `ALLOWED_ORIGINS`: Url of the allowed origins;

    `SERVER_HOST`: FastAPI server ip

    `SERVER_PORT`: FastAPI server port

- Redis Configuration:

    `REDIS_HOST`: Redis Host

    `REDIS_PORT`: Redis Port
    
    `REDIS_PASSWORD`: Redis Password

- Storage Service Configuration:

    `STORAGE_TYPE`: Currently only supports `s3`

    - S3 Configuration:

        `AWS_ACCESS_KEY_ID`

        `AWS_SECRET_ACCESS_KEY`

        `AWS_REGION_NAME`

        `AWS_BUCKET_NAME`

        `EXPIRES_IN`

- Virus Checker Configuration:

    `VIRUS_CHECKER_TYPE`: Currently only supports `total_virus`

    `VIRUS_CHECKER_API_KEY`

## Usage

All dependencies can be installed via poetry:

```bash
poetry install --no-dev
```

For the execution of REST Server:

```bash
poetry run ./run-queue.sh
```

For the execution of the Queue Worker:

```bash
poetry run ./run-queue.sh --queue
```

## API Reference

#### Get file read link

```http
  GET /file
```

| Parameter      | Type     | Description                          |
| :--------      | :------- | :-------------------------           |
| `username`     | `string` | **Required**. Username of file owner |
| `file_postfix` | `string` | **Required**. Type of desired file   |

Returns:

```json
{
    "presigned_url": string
}
```

#### Get file write link

```http
  POST /file
```

| Parameter      | Type     | Description                          |
| :--------      | :------- | :-------------------------           |
| `username`     | `string` | **Required**. Username of file owner |
| `file_postfix` | `string` | **Required**. Type of desired file   |
| `file_type`    | `string` | **Required**. File format            |

Returns:

```json
{
    "presigned_url": string,
    "file_key": string
}
```

#### Delete file

```http
  DELETE /file
```

| Parameter      | Type     | Description                          |
| :--------      | :------- | :-------------------------           |
| `username`     | `string` | **Required**. Username of file owner |
| `file_postfix` | `string` | **Required**. Type of desired file   |

#### Process file

```http
  POST /file/process
```

| Parameter      | Type     | Description                          |
| :--------      | :------- | :-------------------------           |
| `username`     | `string` | **Required**. Username of file owner |
| `file_postfix` | `string` | **Required**. Type of desired file   |


## Authors

- [@HideyoshiNakazone](https://github.com/HideyoshiNakazone)

