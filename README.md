# QRCodeForContact
 By this app admin can generate QR code and user can fill their details and if anyone scan it it will show details.
 
1. Clone this repository into a folder on your computer
2. Download Python
3. Open terminal inside the folder with code.
4. Type pip install -r requirements.txt in the terminal window to install all the requirements to run the app.
5. Type python manage.py runserver to start a localhost server for the app.
6. The API is started and now you can use the API routes to give requests.

----------------------------

# Steps to host Website on AWS

##  Create a free tier eligible EC2 instance
     - Security group rules of EC2:
     - SSH - My IP and Meet's IP
     - HTTP - allow all
     - HTTPs - allow all
     - Allow all traffic on port 800
     - Clone your code from github

## Commands to configure server:
```
sudo apt-get update
```

- Afterwards, we're gonna install python3 as well as Nginx .
```
sudo apt install python3-venv libpq-dev nginx curl
```
```
Install pip
```
```
- wget https://bootstrap.pypa.io/get-pip.py
```

```
- sudo python3 get-pip.py
```

- Create virtual Environment

```
-  sudo apt install python3-venv
```
```
-  python3 -m venv myenv
```
```
-  source myenv/bin/activate
```

## Go to the directory where requirements.txt file is and run folloeing command
```
- pip install -r requirements.txt  (It will install all the requirements)
```

### Make sure that your port 8000 is open for all to connect, check your security rules of instance
### Now allow permission

```
- sudo ufw allow 8000
```

- Now run the server with that specific port no
```
- python3 manage.py runserver 0.0.0.0:8000
```

### Now take public IP of your ec2 and add port number and check on browser
  - http://34.242.1.63:8000/
 
  
### Go to constant.py file and give your end url
  - Your website url is "http://www.sarathiqrcodesolutions.co.in/view_all_details/get_qr_code_details/"

    

  ![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/e148228d-1e75-4e77-a48a-5228bd8157ab)


### Go to super_user.py and change '\\' to '/'  

- There are total 2 changes in the file

![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/6168f734-d3f5-4e3d-bf63-87e96c3dd940)



![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/e5f3460f-f1ee-410e-96d3-43d570a07056)



### You need to map your EC2 instance's IP address on Godaddy

- When you run your website url "http://www.sarathiqrcodesolutions.co.in/view_all_details/get_qr_code_details/" , it will show Nginx page.

  ![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/f28910d6-333b-4b7c-9b29-f68a8fa712e4)





- Which means Your registered url is mapped to your server
- Now, you need to do reverse proxy on Nginx
- You need to give your server public Ip along with port number so Nginx will forward any request to your server id

- Go to this file
```
- cd /etc/nginx/sites-available
```
```
- nano default
```


- Add server block to the default file as shown below:

  ```
  server {
    listen 80;
    server_name www.sarathiqrcodesolutions.co.in;

    location / {
        proxy_pass http://34.242.1.63:8000;  # Assuming Django development serve>
        proxy_set_header Host $host;
    #    proxy_set_header X-Real-IP $remote_addr;
    }

   #   location /static/ {
   #      alias /path/to/your/static/files;  # Path to your static files
   # }
  }

  ```


![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/0ad71c73-93f3-4a8f-9e9c-0e0bb2f8b636)




## Now restart Nginx to see the changes

```
- sudo systemctl stop nginx
```
```
-  sudo systemctl status nginx
```
```
-  sudo systemctl start nginx
```

# Now restart the server 

```
-  cd
```
```
-  cd qrCodeForContact/
```
```
-  cd QRCodeWithContact/
```
```
-  python3 manage.py runserver 0.0.0.0:8000
```


![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/a44fefcd-1a94-4438-8c2b-33d431c86430)



### Useful Articles:
- https://www.programink.com/django-tutorial/django-deployment.html

- https://awstip.com/how-to-deploy-django-application-on-aws-ubuntu-ec2-25a24ca439e2

### Commands History:

```
sudo apt-get update
sudo apt install python3-venv libpq-dev nginx curl
sudo systemctl status nginx
pip install -r requirements.txt
sudo install pip3
git clone https://github.com/meet21mit21/qrCodeForContact.git
ls
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo apt install python3-venv
python3 -m venv myenv
source myenv/bin/activate
history
pip install -r requirements.txt
cd qrCodeForContact/
cd QRCodeWithContact/
ls
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000
sudo systemctl status nginx
python3 manage.py runserver 0.0.0.0:8000
sudo ufw allow 8000
python3 manage.py runserver 0.0.0.0:8000
sudo ufw allow 8000
python3 manage.py runserver 0.0.0.0:8000
python manage.py runserver
python3 manage.py runserver 0.0.0.0:8000
history
ls
cd QrCodeGenerator/
nano common.py
nano constants.py
nano super_user.py
python3 manage.py runserver 0.0.0.0:8000
cd ..
python3 manage.py runserver 0.0.0.0:8000
cd
cd /etc/nginx/sites-available
sudo nano default
```

### To run the server / process in the background we can use 'tmux'
- When you close the terminal, the server will go down and so will your website. For that we can use 'tmux', which allows you to run your server in the background and you can close the terminal.

- Install tmux
```
sudo apt update
```

```
sudo apt install tmux
```

 - Start a New tmux Session:
 - type tmux to start a new tmux session

 ```
  tmux
 ```

- Run Your Process:
- Inside the tmux session, run your desired process as if you were in a regular terminal session. For example

  ```
  python3 manage.py runserver 0.0.0.0:8000
  ```

- Detach from tmux Session:
- To detach from the tmux session while keeping your process running, press the following key combination:
- Press 'ctrl+b' together and after that release it and press 'd'
- This will return you to your regular terminal prompt.

- Now you can close your terminal and your server will run in the background

- Reattach to the tmux Session:
- To reattach to the tmux session and continue interacting with your process, use the following command:
- tmux attach

- If you close your terminal while inside a tmux session (by detaching from the session using Ctrl-b, d), the processes running within that tmux session will continue to run in the background. Closing the terminal in this scenario will not terminate the processes running within the tmux session.
- However, if you exit the tmux session itself (by typing exit or closing the terminal window), the tmux session and any processes running within it will be terminated.

  
- In summary:
- Detaching from a tmux session and closing the terminal will not terminate the processes within the tmux session.
- Exiting the tmux session and closing the terminal will terminate the tmux session and any processes within it.
- If you want your server to continue running even after you close the terminal, you should keep the tmux session active by detaching from it rather than exiting it.


- You have evrything on the server and (code, dependencies etc), then you just have to start vertual environment from where your venv file is.
- In this case run "source myenv/bin/activate" command from where your myenv file is located.
- This will activate virtual environment.
- Then go to code directory to run your server. (go in 'tmux' first).


## To kill the process on port 
- "sudo fuser -k -n tcp 8000"  (change port number according to your usecase)



## Generate ssl certificate for secure https connection
- sudo apt install certbot python3-certbot-nginx -y
- sudo apt-get update
- sudo apt-get install certbot python3-certbot-nginx -y
- sudo certbot --nginx -d your-domain.com     (Change domain name to www.sarathiqrcodesolutions.co.in)

## Change the nginx config
- go to sudo nano /etc/nginx/sites-available/default
- change your EC2 ip address in proxy pass

  
````
server {
 listen 443 ssl default_server;
        #listen [::]:443 ssl default_server;

  server_name www.sarathiqrcodesolutions.co.in;

  location / {
      proxy_pass http://EC2 IP:8000;  # Assuming Django development serve>
      proxy_set_header Host $host;

      proxy_set_header X-Real-IP $remote_addr;
  }

 #   location /static/ {
 #      alias /path/to/your/static/files;  # Path to your static files
 # }

   # listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/www.sarathiqrcodesolutions.co.in/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/www.sarathiqrcodesolutions.co.in/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}




#server {
   # if ($host = www.sarathiqrcodesolutions.co.in) {
    #    return 301 https://$host$request_uri;
   # } # managed by Certbot


  #listen 80;
  #server_name www.sarathiqrcodesolutions.co.in;
 #   return 404; # managed by Certbot


#}
server {
    listen 80;
    server_name www.sarathiqrcodesolutions.co.in;  # Add your domain and www subdomain if needed

    # Redirect all HTTP requests to HTTPS
    return 301 https://$host$request_uri;
}

````

## Autorenewal of ssl certificate after 90 days
- sudo crontab -l

