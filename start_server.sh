docker stop foot_server && docker rm foot_server &&

cd /home/ec2-user/footserver &&
docker build -t foot_server:$1 . &&
docker run -d -p 9999:9999 --name foot_server -e TZ=Asia/Seoul foot_server:$1
