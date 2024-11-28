token=$(cat config.json | jq -r '.pcard_bot')
url=https://yartbot.ycloud.eazify.net:8443/pcardhook

curl --location --request POST "https://api.telegram.org/bot$token/setWebhook" \
--header 'Content-Type: application/json' \
--data-raw "{
    \"url\": \"$url\",
    \"allowed_updates\" : ['message','edited_message']
}"

token=$(cat config.json | jq -r '.flower_bot')
url=https://yartbot.ycloud.eazify.net:8443/flowerhook

curl --location --request POST "https://api.telegram.org/bot$token/setWebhook" \
--header 'Content-Type: application/json' \
--data-raw "{
    \"url\": \"$url\",
    \"allowed_updates\" : ['message','edited_message']
}"