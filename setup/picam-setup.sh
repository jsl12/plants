sudo apt-get update -y
sudo apt-get dist-upgrade -y
sudo apt-get upgrade -y

sudo apt install proftpd -y
sudo sed -i '/DefaultRoot /c\DefaultRoot /home/pi' /etc/proftpd/proftpd.conf

sudo apt install python3-picamera -y

sudo apt-get install git -y
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
sudo apt-get install cmake -y
sudo apt-get install python-imaging -y
sudo apt-get install libjpeg-dev -y
make CMAKE_BUILD_TYPE=Debug
sudo make install
export LD_LIBRARY_PATH=.
