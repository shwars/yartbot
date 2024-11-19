token=7815987129:AAETncqCKgJ_pcAyKgv7mHg_rX-qfvfxizk
url=https://yartbot.ycloud.eazify.net:8443/pcardhook

curl --location --request POST "https://api.telegram.org/bot$token/setWebhook" \
--header 'Content-Type: application/json' \
--data-raw "{
    \"url\": \"$url\",
    \"allowed_updates\" : ['message','edited_message']
}"