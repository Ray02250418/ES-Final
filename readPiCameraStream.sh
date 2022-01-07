rm -rf picamera1
rm -rf picamera2
if [ -p picamera1 ]
then 
    rm -rf picamera1
fi
if [ -p picamera2 ]
then 
    rm -rf picamera2
fi
mkfifo picamera1
mkfifo picamera2
nc -l 8080 -v > picamera1 &
nc -l 8081 -v > picamera2
