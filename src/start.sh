rm -rf picamera1 picamera2
echo "remove picamera1, picamera2"
mkfifo picamera1
# mkfifo picamera2
echo "make picamera1 & 2"
nc -l 8080 -v > picamera1 &
echo "8080 pipe name: picamera1"
#nc -l 8081 -v > picamera2 & 
serverip=$(ipconfig getifaddr en0)
echo "get server ip: ${serverip}"
echo "run the program and wait for 5 seconds ..."
python3 run_model_example.py &
sleep 10
#echo "start streaming video on rpi"
echo 123
# ssh -l pi 192.168.50.243 "echo 12345"
# ssh -l pi 192.168.50.243 "~/Documents/stream.sh ${serverip} 8080"
#ssh -l pi 192.168.50.243 "raspivid -n -w 640 -h 480 -o - -t 0 -b 2000000 | nc ${serverip} 8080"
#rpiIP1=$1
#rpiIP2=$2
#ssh -l pi $1 "raspivid -n -w 320 -h 240 -o - -t 0 -b 2000000 | nc ${server} 8080"
#ssh -l pi $2 "raspivid -n -w 320 -h 240 -o - -t 0 -b 2000000 | nc ${server} 8080"