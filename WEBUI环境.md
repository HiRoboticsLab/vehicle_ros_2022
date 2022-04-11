```shell
# 网页文件
sudo docker pull nginx

sudo docker run -it -d --restart always -p 8080:80 -v /home/jetbot/Desktop/vehicle/ui/webviz/html:/usr/share/nginx/html --name webviz nginx

sudo docker run -it -d --restart always -p 80:80 -v /home/jetbot/Desktop/vehicle/ui/ctrl/dist:/usr/share/nginx/html --name webtool nginx
```