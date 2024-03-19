download-chromium
=================

<img src="static/logo.png" width="48">

This is a web application running on Google App Engine that lets you download the last Chromium builds for Windows, Mac, Linux, Chrome OS and Android.

You can find the Google App Engine instance at https://download-chromium2.uc.r.appspot.com/

This web application is officially listed on https://www.chromium.org/getting-involved/download-chromium

 - Go learn differences between Chromium and Google Chrome at https://chromium.googlesource.com/chromium/src/+/master/docs/chromium_browser_vs_google_chrome.md

### Local Development

 - Prerequisites: python3 python3-pip python3-venv

```bash
sudo apt install python3 python3-pip python3-venv
```

1. Install the Google Cloud SDK via instructions at https://cloud.google.com/sdk/docs/install

2. Make sure that the `app-engine-python` component is installed via instructions located [Here](https://cloud.google.com/appengine/docs/standard/tools/using-local-server?tab=python)

3. Clone the repo:

```bash
git clone https://github.com/Alex313031/download-chromium.git
```

4. Use the instructions [Here](https://cloud.google.com/appengine/docs/standard/tools/using-local-server?tab=python#running_the_local_development_server) to run `dev_appserver.py` and point to the `app.yaml` in the repo.

For example:

```bash
python3 $HOME/google-cloud-sdk/bin/dev_appserver.py $HOME/download-chromium/app.yaml
```

5. Then you can simply open your browser to http://localhost:8080 to view the webpage.

### Deployment

```bash
gcloud config set project <your-project-id>
gcloud app deploy --project <your-project-id>
```
