# CAMSCAN

Some object detections on a IP Camera feed using an Google Coral Edge TPU

### How to run?
```sh
docker build -t camscan:dev .
docker run -it --privileged  camscan:dev # Needs to run with the privileged flag to have access to the tpu
```