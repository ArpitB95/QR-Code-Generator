# qrCodeForContact
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

## Commands to configure server:
- sudo apt-get update

- afterward, we gonna install python3 as well as apache2 .
- sudo apt install python3-venv libpq-dev nginx curl

- Install pip
- wget https://bootstrap.pypa.io/get-pip.py
- sudo python3 get-pip.py

- Create virtual Environment
-  sudo apt install python3-venv
-  python3 -m venv myenv
-  source myenv/bin/activate


## Go to the directory where requirements.txt file is and run folloeing command
- pip install -r requirements.txt  (It will install all the requirements)

## Make sure that your port 8000 is open for all to connect, check your security rules of instance
## Now allow permission
- sudo ufw allow 8000

- Now run the server with that specific port no
- python3 manage.py runserver 0.0.0.0:8000

  ## Now take public IP of your ec2 and add port number and check on browser
  - http://34.242.1.63:8000/
 
  
  ## Go to constant.py file and give your end url
  - Your website url is "http://www.sarathiqrcodesolutions.co.in/view_all_details/get_qr_code_details/"
  - 

  ![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/e148228d-1e75-4e77-a48a-5228bd8157ab)


## Go to super_user.py and change \\ to /  
- There are total 2 changes in the file

![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/6168f734-d3f5-4e3d-bf63-87e96c3dd940)



![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/e5f3460f-f1ee-410e-96d3-43d570a07056)



## You need to map your EC2 instance's IP address on Godaddy
- When you run your website url "http://www.sarathiqrcodesolutions.co.in/view_all_details/get_qr_code_details/" , it will show Nginx page.

  ![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/f28910d6-333b-4b7c-9b29-f68a8fa712e4)





- Which means Your registered url is mapped to your server
- Now, you need to do reverse proxy on Nginx
- You need to give your server public Ip along with port number so Nginx will forward any request to your server id

- Go to this file
- cd /etc/nginx/sites-available
- nano default 
- Add server block to the default file as shown below:

  ````
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

  ````

![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/0ad71c73-93f3-4a8f-9e9c-0e0bb2f8b636)




## Now restart Nginx to see the changes
- sudo systemctl stop nginx
-  sudo systemctl status nginx
-  sudo systemctl start nginx

# Now restart the server 
-  cd
-  cd qrCodeForContact/
-  cd QRCodeWithContact/
-  python3 manage.py runserver 0.0.0.0:8000

![image](https://github.com/ArpitB95/QR-Code-Generator/assets/110182832/a44fefcd-1a94-4438-8c2b-33d431c86430)



