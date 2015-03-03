# streaming-upload

Small web server built using webapp2 and MongoDB to handle uploading large files
through the means of streaming.

## Data Model

Collection - File

```
{
    'timestamp': time.time(),
    'path': path,
    'size': size,
    'checksum': Binary(checksum, MD5_SUBTYPE),
}
```

## TODO:

* Handle cleaning up old or corrupt files
