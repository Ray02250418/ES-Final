rm -rf picamera1
rm -rf picamera2
sleep 5
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
nc -l 8085 -v > picamera1 &
nc -l 8083 -v > picamera2
