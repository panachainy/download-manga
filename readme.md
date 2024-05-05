# download-manga

## development

1. create file `config.json` and add data (example is `ex-config.json`)
2. make i
3. Download follow config.json `make download`
4. convert images to pdfs `make make`
5. merge pdfs to 1 pdf `make merge`

## Download v2

- `make load_config` for feed all urls to download to configs
- `make load_download` for download all manga (handled by golang)

## TODO

- implment SQLite for tracking success or fail in load / convert / per chapter per title

## setup gsheet

https://docs.streamlit.io/develop/tutorials/databases/private-gsheet
