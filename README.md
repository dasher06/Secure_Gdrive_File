# Secure GDrive Link Encryptor and Decryptor

This is a simple project I built to share **Google Drive files** in a secure way. Instead of just sending someone a direct link to a file, this app **encrypts** the link using a **10-digit password** that only the sender and receiver know. 

The receiver can then use that password on a web page to unlock and access the file.

---

## How to Run the Project

### Here’s how you can run this project on your local machine:

1. Clone the repo to your computer
2. Install the required Python packages using `pip install -r requirements.txt`
3. Go to **Google Cloud ** :
   - Create a new project
   - Enable the Google Drive API
   - Configure the OAuth Consent Screen
   - Create OAuth Client ID credentials
   - Download the `client_secrets.json` file and place it in the root folder
   - Run the script using `python Encrypted_Link.py`

4. A browser window will open to authenticate your **Google Drive**
   - Once authenticated, a list of your Drive files will appear in the terminal
   - Choose a file by entering its number
   - Enter a 10-digit password (this is your custom encryption key)

5. The script:
   - Gives public permission to the file
   - Encrypts the file link using your password
   - Sends an email with a special decryption page and password
   - The receiver opens the link, enters the password, and gets the original file

### How to Deploy on Google Cloud Run

1. Here's how to deploy the app using Cloud Run:
   - Make sure you have a Google Cloud project set up
   - Enable the **Cloud Run**, **Cloud Build**, and **Artifact Registry APIs**
   - Install and set up the Google Cloud CLI
   - Authenticate with: `gcloud auth login`
   - Make sure your project is selected: `gcloud config set project [PROJECT_ID]`

2. In your project folder, run:
   - `gcloud builds submit --tag gcr.io/[PROJECT_ID]/secure-gdrive`

3. Deploy to Cloud Run with:
   - `gcloud run deploy secure-gdrive --image gcr.io/[PROJECT_ID]/secure-gdrive --platform managed --region [YOUR_REGION] --allow-unauthenticated`

4. After deployment, you’ll get a public URL like:
   - https://secure-gdrive-[random].run.app

**Share this URL with the encrypted query string for access**

## How the project works?

1. You select a file from your **Google Drive**.
2. The app gives that file public permissions so that anyone with the link can view or edit it.
3. You choose a 10-digit number as a password.
4. The link gets encrypted using that password.
5. An email is sent to someone with:
   - A secure page link (where they can decrypt the file)
   - The password needed to unlock it
6. The receiver visits the link, enters the password, and gets the original **Google Drive file**.

---

## How I ran the project (deployment steps)

### 1. Localhost (basic testing)

At first, I just ran the Python Flask app on my own computer. I opened a terminal and ran:

python Encrypted_Link.py

This started the web server at:

http://127.0.0.1:5000/decrypt_link

This worked fine for testing, but only I could access it since it was local.

---

### 2. Ngrok (making it temporarily public)

To let someone else access it over the internet, I used ngrok. After installing it, I ran:

ngrok http 5000

Ngrok gave me a public URL (This links do not work right now!):

https://secure-decryptor-1068809376566.us-central1.run.app/decrypt_link?encrypted=gAAAAABoV_6h-28TYpIJehShsPnfESGRAaXWLMhSsXC1kfINaxaL-4dPT1Lsuba7OSvJgk0U5XgpXLmKuAXPBqmA6ap5m-MH_66UW9HMQ117N1HHpWDRmuPTJxCwfYj0bTX_uW1CsfHr8nXQo_Vm6_1rvn4NWvOwYpBj92HyepVK4PC_rDYZ6J8=

Now, anyone with that link could open the web page. But, the program terminal from my end should be active and also the cert is not signed by a valid authority.

---

### 3. Render (permanent public access)

I later deployed the app on Render.com, which is a free hosting service for web apps to make it permanent.

I pushed my code to GitHub, connected the GitHub repo to Render.

It was fine but there was too much code alteration and my original code was changed so much including the o/p. But Render built the app and gave me a live URL

Something like (This link do not work right now!):

https://encryptedlinkapp.onrender.com/decrypt_link?encrypted=gAAAAABoVWml-d0XY_H9foOHshdv4WE11_l7Bony0O2AGPYcKtF2UfE49_8yMbcEyJKKtv8W1KnRuDOF47_hP-oMBWQqYlf4bLy-nicouNw_IT5HVfU3dBHimdZ9KrW5CgEczV3GA3CK86yHihpxrrjmjz4pR83AFQ==

This made the app available 24/7 without needing to keep my computer on.

---

### 4. Google Cloud Platform (current attempt)

Right now, the project is deployed on Google Cloud Platform (GCP) using Cloud Run because, I don't want code alteration like render. I created a Dockerfile for the app, built the container, and deployed it using the gcloud command line tool.

This is the sample live URL on how the output looks. You can check it by clicking the link below,

🔓 Decryption Page:

https://email-link-encryption-1068809376566.us-central1.run.app/decrypt_link?encrypted=gAAAAABoitaIj1z0f2zVW2wLOPVAknYV76n3z_S05YRbn4DHVvDVM2tNIhVJbOMZEOfwQrtv-iimHoLpNj1aNm4Dp5zAzgvXV81ObXzt2-NfYebmagNpJcJVmCOZokJenMyKLt6B7Tm5mob7BL6D-bBpZHgmOlyuUlTimu4-NndsSZI5xaOvmtU=

When prompted, enter the decryption key below:

🔐 Decryption Key: 1234567890

Now, this makes the process easier because, the server is live 24/7 and i was able to deploy the program without any alteration and error.

---

## What's in the Project

Here are the main files:

- `Encrypted_Link.py`: The main Python script with Flask routes and logic
- `requirements.txt`: Lists the Python packages needed
- `Dockerfile`: Tells Google Cloud how to build and run the app
- `.gitignore`: Makes sure secret files and unnecessary folders (like venv) aren't uploaded
- `templates/decrypt_link.html`: The HTML template for the decryption form
- `.dockerignore`: Prevents specified files from being copied into Docker build context

## Technologies Used

- Python 3
- Flask
- Cryptography (Fernet)
- PyDrive
- Gmail SMTP
- Ngrok
- Render
- Docker
- Google Cloud Platform (Cloud Run)

---

## Acknowledgements

Special thanks to my both uncle **Kiru Veerappan** and **Udhayan Nagarajan** for encouraging and guiding me in building this project .  

---

Created by Trinab Shan

GitHub: @dasher06

Thank You










