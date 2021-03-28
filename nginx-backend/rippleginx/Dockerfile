FROM nginx:1.15
WORKDIR /etc/nginx/conf.d/
COPY servers .
CMD ["nginx", "-g", "daemon off;"]
