# TeloBot
## Monad-Native telegram & discord bot | Token & NFT mint sniper

## WHAT IS TELOBOT?

In 2025 there is a need to onboard new cryptocurrency investors into already established platforms like Discord, Telegram, Twitter... instead of slowly grinding through user acquisition from ground zero.
You can now use Telobot as a Monad  crypto wallet directly in these 2 platforms: on Telegram as a bot, I assume we are already familiar with TG bots. In Discord you can interact with it in a normal general-chat(recommended only for balance checks and data retrieval) or dm the bot(must join the Telobot server first!), like you would privately message your friend.
Another issue is the rampant use of automation on-chain, evident in many NFT mints, where collections are minted out before the public has even a chance to load metamask to sign the mint transaction. 
Telobot solves this by reducing transaction execution for both token swaps and NFT mints to sub 2 seconds, with regional based instances(EU, NA, ASIA) and upcoming custom rpc support 
This is the reason why Telobot was created (by @telog14) and is available for anyone to modify and reuse.

## HOW DOES TELOBOT WORK?

Telobot is an open-source Monad-native Python Telegram & Discord bot wallet. It leverages Flask & Waitress WSGI server for hosting a webhook endpoint and uses Web3.py to manage on-chain operations: balance queries, token transfers, Uniswap V2 swaps(will soon support V3) + more features after launch.
The repository includes an example nginx.conf for reverse proxy configurations, additionally a .env file for storing sensitive environment variables.
Basic configuration for an HTTP server block that proxies requests to the Flask/Waitress process.
Commented examples(provided by nginx) for an HTTPS server block if you choose to run SSL directly in Nginx.
For Discord, Telobot communicates via the Discord Gateway, a real-time WebSocket connection.
Thanks to Discord Intents, it can detect and process commands in both server text channels and private DMs.
Private keys are never stored in memory and are discarded right after each tx signing, making up for a trustless security management.
Since platforms like Discord and Telegram log all chat's messages, it's recommended to generate a wallet address just for these 2 platforms alone, rotate funds to another wallet every month or so and never store amounts too high on them.
Post launch features include Uniswap v4 integration(with hooks), new Discord slash commands, new Telegram menu button, more methods to retrieve blockchain data, potential integration with various testnet & mainnet protocols on Monad.

## INSTALLATION GUIDE

The repo features two python files so it's relatively easy to set up.
The telegram and discord bots have for 90% the same code, since they have a different approach when communicating to our web server.
Because there is one main.py file for each platform, I'm providing 2 separate guides.

## BEFORE STARTING

Install dependencies found in requirements.txt.
Locate your Python environment directory and add the .env file in the folder, remember to enter your environment variables into it.
To our cloudflare config file, to each discord and telegram python file have been assigned a .service file used to run files on boot
Now we will check each platform's guide together!

## TELEGRAM

Visit https://nginx.org/en/docs and download nginx.
In order to host the HTTPS endpoint, I will be using Cloudflare, because of the no-logging policy with traffic metadata.
Visit Cloudflare and create an account with a strong password, get your own web domain and DNS with Cloudflare if you don't have one and install cloudflared package.
Create a tunnel(i do it manually by logging in, creating a tunnel, binding it to my domain and finally i create a configuration file and run it), edit and run the .config.yml file(add the cloudflared.service file to your system).
Nginx is used as our reverse proxy routing to our custom domain, for each bot session i have a different tunnel paths.
Open Telegram and get your secret token from BotFather; keep this token super safe. If stolen, a malicious actor can gain control of your bot. Remember: you can always change the secret token by talking to BotFather.
Now set the webhook for your Telegram bot. Open the terminal and enter this command:
curl https://api.telegram.org/bot<your_botfather_token>/setWebhook?url=<your_domain>/webhook
Nginx’s reverse proxy is now activated, together with your domain, the webhook is safely configured, and you can start hosting your own version of Telobot.
Start trading on the fastest L1 chain now!

## DISCORD

Discord uses its own gateway, so we do not need to use any of the prior setup, as we run the Discord bot locally and communicate with the Discord gateway directly.
Go to the Discord Developer Portal, create a new bot, go to OAuth2, and save the “client secret” and keep it safe!
Go to OAuth2 → URL Generator.
Select these scopes:

bot
applications.commands
Scroll down and select bot permissions, initially these ones:
Send Messages
Read Message History
Use Slash Commands
Copy the generated invite link and open it in your browser.
Select your server and click Authorize.
Now the bot will appear in the list of members in your Discord server.
Run the discord.py file, and you will have your own version of Telobot in your Discord server.
Initially it's recommended that you manually disable the bot’s server permissions to send messages in any channel, so it won’t answer users in general chat. Alternatively you can just stop certain /command messages from being sent in a channel, but allow ones that don't require private key signing(like /get_balance). The bot will still respond via DMs.
The bot can then message each user through DMs. Users must initiate the conversation first by messaging the bot, not the other way around.
If you only want to use Telobot in your server without creating your own bot, you can invite the public version at this link(for all active and guaranteed to be functioning links, come into my discord):
https://discord.com/oauth2/authorize?client_id=1353643570548047883&permissions=1125899906910208&integration_type=0&scope=bot+applications.commands  

The Discord guide is finished! Happy Sniping! GMoanHard <3

## LINKS

Telegram: GLOBAL https://t.me/tg_Telobot EU1: https://t.me/Mon_Telobot EU2: https://t.me/Mon2_Telobot EU3: https://t.me/Mon3_Telobot NA1: https://t.me/NA_Telobot NA2: https://t.me/NA2_Telobot NA3: https://t.me/NA3_Telobot  
Discord: https://discord.gg/YXWSefe3uE and more invite links will be added

This product is subject to terms and condition found in the official discord server
