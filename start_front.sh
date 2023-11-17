#docker stop foot_front && docker rm foot_front &&

cd /home/ec2-user/foot &&
git pull &&
docker build -t foot_front:$1 . &&
docker run -d -p 9090:9090 --name foot_front -e TZ=Asia/Seoul foot_front:$1
