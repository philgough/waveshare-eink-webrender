# waveshare-eink-webrender
HTML-based dashboard for home display, that renders to an image to be updated on an e-ink display. 

## Hardware
This runs on the 7.5-inch B&W version 2 waveshare display. I have it running on a RPi model 2 B+.

## Running the server
You will need to include:
- **twitter.txt** this file contains the bearer token for your twitter account
- **cal_url.txt** this file contains the url of the calendar to read. It's set up to read from iCloud, but you need to change `webcal://[url]` to `https://[url]` for it to work

Run the flask server:
```export FLASK_APP=waveshare.py
flask run -host=0.0.0.0```


## Running the client
[1] Your update the url for the flask client, if it's runnning on the same device use `localhost:5000`/
This is stored in `local_url.txt` in the `pi-code/waveshare/script` folder, it is read using:

```
url = ''
with open('local_url.txt', 'r') as url_f:
    url = url_f.readline().strip()
```


[2] Copy the code from `/pi-code/cron/cron-code.txt` to your contab on the Pi. You should use `sudo crontab -e` and paste the code there. You do need to run this python code using `sudo`.

The two scripts that are added to your crontab will be `waveshare-display-noclear.py` - this runs every 30 minutes. It refreshes the dispaly by reading the flask server, rendering the webpage to a .bmp, which is then displayed. The other file is `waveshare-display-clear.py` - it runs at 2:57am and just clears the screen, because I heard this is good for the e-ink displays. Seems worth it in case it is true. 

The other script, `pi-code/waveshare/script/waveshare-display.py`, does both a clear and an update, but is slower, and not necessary every 30 minutes. 

You should also make `pi-code/waveshare/script/waveshare-display-clear.py` and `pi-code/waveshare/script/waveshare-display-noclear.py` executable by running `chmod +x myscript.py`.

You may also have to install `xvfb` using `sudo apt-get install xvfb` on your Pi. 
