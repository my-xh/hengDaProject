###### 操作环境：百度云服务器
###### 系统版本：CentOS7.8 x86_64
###### 部署方式：Django + Nginx + uWSGI
###### 特别说明：相对路径默认为项目根目录
***


## 一、安装Python3.7.1
### 1. 安装依赖
- yum -y install gcc
- yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel mysql-devel python-devel
### 2. 下载解压
- wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz
- tar -zxvf Python-3.7.1.tgz
### 3. 编译安装
- cd Python-3.7.1/
- ./configure --prefix=/usr/local/python3
- make && make install
### 4. 建立软链接
- ln -s /usr/local/python3/bin/python3.7 /usr/bin/python3
- ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
### 5. 测试
- python3 -V
- pip3 -V
- pip3 install --upgrade pip
***


## 二、安装配置Mysql
### 1. 下载安装
- wget -i -c http://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
- yum -y install mysql80-community-release-el7-3.noarch.rpm
- yum -y install mysql-community-server
### 2. 设置不区分大小写
- sed -i '/\\[mysqld\\]/a\lower_case_table_names=1' /etc/my.cnf
- #删除设置：sed -i '/lower_case_table_names=1/d' /etc/my.cnf
### 3. 启动服务
- systemctl start mysqld.service
### 4. 查看并修改密码
- grep "password" /var/log/mysqld.log
- mysql -uroot -p
- **`ALTER USER 'root'@'localhost' IDENTIFIED BY '符合规则的新密码';`**
- **`SHOW VARIABLES LIKE 'validate_password%';`**
- 关闭用户名检测：**`set global validate_password.check_user_name=0;`**
- 设置密码验证策略：**`set global validate_password.policy=0;`**
- 设置最少密码长度：**`set global validate_password.length=4;`**
- **`ALTER USER 'root'@'localhost' IDENTIFIED BY '简单新密码';`**
### 5. 创建数据库
- **`CREATE DATABASE pythonweb;`**
***


## 三、安装Python第三方库
### 1. 复制项目
- yum -y install lrzsz
- 通过XShell传输项目压缩包：rz
- unzip hengDaProject.zip
- mv hengDaProject /usr/local/
### 2. 安装requirement
- cd /usr/local/hengDaProject/
- pip3 install wheel
- pip3 install -r requirement.txt
### 3. 安装依赖
- yum -y install mesa-libGL
***


## 四、解决移植问题
### 1. 迁移数据库表
- python3 manage.py createcachetable
- python3 manage.py makemigrations
- python3 manage.py migrate
- 通过XShell传输sql文件：rz
- **`USE pythonweb;`**
- **`SOURCE pythonweb.sql;`**
### 2. 收集静态文件
- python3 manage.py collectstatic
### 3. 重建索引
- mv /usr/local/hengDaProject/templates/search/indexes/newsApp/MyNews_text.txt !#^:h/mynews_text.txt
- python3 manage.py rebuild_index
### 4. 修改路径分隔符
- sed -E -i "s#(\\<[a-zA-Z0-9]\*\\>)\\\\\\#\1/#g" /usr/local/hengDaProject/\*App/\*.py
### 5. 安装配置Tesseract-OCR
- yum -y install tesseract
- 简体中文语言包：yum -y install tesseract-langpack-chi_sim
- 阿拉伯数字语言包：yum -y install tesseract-langpack-ara.noarch
- 检查语言包：tesseract --list-langs
### 6. 解决Django2与UEditor兼容性问题
#### 问题描述
>render() got an unexpected keyword argument 'renderer'

>Exception Location:	/usr/local/python3/lib/python3.7/site-packages/django/forms/boundfield.py in as_widget, line 93
- sed -E -i '93s/\\<(.*)\\>/# \1/' /usr/local/python3/lib/python3.7/site-packages/django/forms/boundfield.py
### 7. 测试
- python3 manage.py runserver 0.0.0.0:8080
***


## 五、安装配置uWSGI
### 1. 安装
- pip3 install uwsgi
### 2. 建立软链接
- ln -s /usr/local/python3/bin/uwsgi /usr/bin/uwsgi
### 3. 配置
- mkdir webconfig
- vim webconfig/uwsgi.ini
```
# uwsgi使用配置文件启动
[uwsgi]
# 项目目录
chdir=/usr/local/hengDaProject/
# 指定项目的application
module=hengDaProject.wsgi:application
# 指定sock的文件路径       
socket=/usr/local/hengDaProject/webconfig/uwsgi.sock
# 进程个数       
workers=5
pidfile=/usr/local/hengDaProject/webconfig/uwsgi.pid
# 指定IP端口       
http=0.0.0.0:8080
# 指定静态文件
static-map=/static=/usr/local/hengDaProject/static
# 启动uwsgi的用户名和用户组
uid=root
gid=root
# 启用主进程
master=true
# 当服务停止的时候自动移除unix Socket和pid文件
vacuum=true
# 如果可能的话，序列化接受的内容
thunder-lock=true
# 启用线程
enable-threads=true
# 设置自中断时间
harakiri=30
# 设置缓冲
post-buffering=4096
# 设置日志目录
daemonize=/usr/local/hengDaProject/webconfig/uwsgi.log
```
### 4. 测试
- uwsgi --ini webconfig/uwsgi.ini
### 常用命令
- 启动：uwsgi --ini webconfig/uwsgi.ini
- 停止：uwsgi --stop webconfig/uwsgi.pid
- 重新加载配置：uwsgi --reload webconfig/uwsgi.pid
- 监控日志：tail -f webconfig/uwsgi.log
***


## 六、安装配置Nginx
### 1. 安装
- yum -y install nginx
### 2. 启动服务器
- nginx
### 3. 拷贝uwsgi_params文件
- 从 https://github.com/nginx/nginx/blob/master/conf/uwsgi_params 获取
- vim webconfig/uwsgi_params
```
uwsgi_param  QUERY_STRING       $query_string;
uwsgi_param  REQUEST_METHOD     $request_method;
uwsgi_param  CONTENT_TYPE       $content_type;
uwsgi_param  CONTENT_LENGTH     $content_length;

uwsgi_param  REQUEST_URI        $request_uri;
uwsgi_param  PATH_INFO          $document_uri;
uwsgi_param  DOCUMENT_ROOT      $document_root;
uwsgi_param  SERVER_PROTOCOL    $server_protocol;
uwsgi_param  REQUEST_SCHEME     $scheme;
uwsgi_param  HTTPS              $https if_not_empty;

uwsgi_param  REMOTE_ADDR        $remote_addr;
uwsgi_param  REMOTE_PORT        $remote_port;
uwsgi_param  SERVER_PORT        $server_port;
uwsgi_param  SERVER_NAME        $server_name;
```
### 4. 添加自定义配置文件
- vim webconfig/hengDa_nginx.conf
```
# the upstream component nginx needs to connect to
upstream hengDaProject {
    server unix:/usr/local/hengDaProject/webconfig/uwsgi.sock;   # 这里是通过socket方式访问django项目，也是我们的最终目的。uwsgi.sock文件会自动创建，我们只需要指定前面的路径到我们项目即可
    # server 0.0.0.0:8080;          # for a web port socket (we'll use this first)
}

# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    # the domain name it will serve for
    server_name 网站域名;      # IP地址或者域名
    access_log /usr/local/hengDaProject/webconfig/access.log main; # Nginx日志配置
    error_log /usr/local/hengDaProject/webconfig/error.log;
    charset     utf-8;
    gzip_types text/plain application/x-javascript text/css text/javascript application/x-httpd-php application/json text/json image/jpeg image/gif image/png application/octet-stream; # >支持压缩的类型

    error_page 404 /404.html; # 错误页面
    error_page 500 502 503 504 /50x.html; # 错误页面

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /usr/local/hengDaProject/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /usr/local/hengDaProject/static; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  hengDaProject;     # 指定django
        include     /usr/local/hengDaProject/webconfig/uwsgi_params;   # 这里是我们上一步创建的uwsgi_params文件，指定路径
        uwsgi_connect_timeout 30; # 设置连接uWSGI超时时间
    }
}
```
### 5. 建立软链接
- ln -s /usr/local/hengDaProject/webconfig/hengDa_nginx.conf /etc/nginx/conf.d/
### 6. 重启服务器
- nginx -s reload
### 常用命令
- 启动：nginx
- 停止：nginx -s stop
- 重新加载配置：nginx -s reload
- 检查配置：nginx -t
- 设置开机启动：systemctl enable nginx
- 取消开机启动：systemctl disable nginx
- 监控日志：tail -f webconfig/access.log webconfig/error.log
***


## 七、尾声
### 1. 关闭uWSGI测试端口
- sed -E -i 's/(http=.*)/# \1/' webconfig/uwsgi.ini
### 2. 修改域名
- sed -E -i 's/(([0-9]{1,3}\\.){3}[0-9]{1,3}:[0-9]{4})/网站域名/g' \*App/templates/\*.html
- sed -E -i 's/(([0-9]{1,3}\\.){3}[0-9]{1,3}:[0-9]{4})/网站域名/g' test/*.py
### 3. 更新二维码
- cd test
- python3 generateQRImg.py
- cd ..
### 4. 修改备案号
- sed -E -i "s/(版权所有 \\| ).*号/\1备案号/" templates/base.html
### 4. 修改邮箱配置
- sed -E -i "s/(EMAIL_PART = )[^ ]\*/\1端口号/" hengDaProject/settings.py
- sed -E -i "s/(EMAIL_HOST_USER = )[^ ]\*/\1'企业QQ邮箱账号'/" hengDaProject/settings.py
- sed -E -i "s/(EMAIL_HOST_PASSWORD = )[^ ]\*/\1'授权码'/" hengDaProject/settings.py
### 5. 关闭Debug模式
- sed -E -i 's/(DEBUG = ).*/\1False/' hengDaProject/settings.py
***

