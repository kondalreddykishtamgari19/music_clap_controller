Aurdino_Code:
==============
replace wifi credentials in line 5 and 6
:Hotspot Name and your password.
Change firebase url in line 30.(which is your realtime database url)
Change Secret key in line 31. which is in database secrets. 

Make sure your laptop and esp32 microcontroller should be in same network which mentioned in the aurdino_code



Music_Clap_Controlled_Folder
============================
Replace "clap.json"  after creating firebase account.


-->Open visual Studio code
-->Click on file
-->Add folder to workspace
-->Open terminal
-->Click on new terminal

To install libraries:
=====================
pip install -r requirements.txt

Takes more than 3 minutes to install dont disturb the terminal while installing.


In app.py
=========
Replace firebase realtime database url in line 12.

click on ctrl+S to save after changes

to execute python file:
=======================
python app.py


