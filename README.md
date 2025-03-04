# TeloBot
Monad-Native telegram and discord bot &amp; crypto wallet

## WHAT IS TELOBOT?
In 2025 there is a need to onboard new cryptocurrency investors into already established platforms like Discord, Telegram, Twitter... instead of slowly grinding through user acquisition from ground zero.  
You can now use a crypto wallet directly in these 2 platforms: on Telegram as a bot, I assume we are already familiar with TG bots. In Discord you can interact with it in a normal general-chat(recommended only for balance checks and data retrieval) or dm the bot(must join the Telobot server first!), like you would privately message your friend.  
This is the reason why Telobot was created (by @telog14) and is available for anyone to modify and reuse.  

## Onto the technicals, how does Telobot work?
Telobot is an open-source Monad-native Python Telegram & Discord bot wallet. It leverages Flask & Waitress WSGI server for hosting a webhook endpoint on Windows(uvicorn being among the main Linux alternatives to waitress) and uses Web3.py to manage on-chain operations: balance queries, token transfers, Uniswap V2 swaps + more features after launch.    
The repository includes an example nginx.conf for reverse proxy configurations, additionally a .env file for storing sensitive environment variables.   
Basic configuration for an HTTP server block that proxies requests to the Flask/Waitress process.  
Commented examples(provided by nginx) for an HTTPS server block if you choose to run SSL directly in Nginx.  
For Discord, Telobot communicates via the Discord Gateway, a real-time WebSocket connection.  
Thanks to Discord Intents, it can detect and process commands in both server text channels and private DMs.  
Private keys are never stored in memory and are discarded right after each tx signing, making up for a trustless security management.  
Since platforms like Discord and Telegram log all chat's messages, it's recommended to generate a wallet address just for these 2 platforms alone, and never store too high crypto amounts on them.  
Post launch features include Uniswap v4 integration(with hooks), in-wallet private key generation, more methods to retrieve blockchain data(waiting for Infura's Monad endpoint to be live), integration with various testnet & mainnet protocols on Monad.  


## INSTALLATION GUIDE
The repo features two python files so it's relatively easy to set up.  
The telegram and discord bots have for 90% the same code, since they have a different approach when communicating to our web server.  
Because there is one main.py file for each platform, I'm providing 2 separate guides.  


## BEFORE STARTING
Install dependencies found in requirements.txt.  
Locate your Python environment directory and add the .env file in the folder, remember to enter your environment variables into it.  
Now we will check each platform's guide together!  

## TELEGRAM
Go to https://nginx.org/en/docs/windows.html and download nginx for Windows, since Waitress requires a Windows distribution to work.  
Alternatively, you can use uvicorn to run the server on Linux.  
In order to host the HTTPS endpoint, I will be using ngrok.  
Go to ngrok.com and create an account with a super-strong password, then set up 2FA(mandatory).  
Go into the settings and disable observability(mandatory).  
Download ngrok, follow the installation process at https://dashboard.ngrok.com/get-started/setup/windows. Run the command to add your authtoken to the default ngrok.yml configuration file.  
Visit the “domains” tab on the website and claim your static HTTPS endpoint token (ends with ngrok-free.app).  
Run the ngrok.exe file and enter this command:  
`ngrok http 80 --url=your_static_endpoint-free.app`  
Replace the "https_endpoint" in the nginx.conf file with this ngrok domain endpoint and save the nginx file.  
Like I said, you can use any HTTPS domain you prefer, but if you’re hosting via ngrok only, you don’t necessarily need Nginx for a basic setup.  
Open Telegram and get your secret token from BotFather; keep this token super safe. If stolen, a malicious actor can gain control of your bot. Remember: you can always change the secret token by talking to BotFather.  
Now you have to set the webhook for your Telegram bot. Open the command prompt and insert this command:  
`curl https://api.telegram.org/bot<your_botfather_token>/setWebhook?url=<your_domain>/webhook`   
Replace your_botfather_token with your Telegram secret token and your_ngrok_domain with the ngrok domain.  
An SSL certificate is not needed when hosting through ngrok, so we will skip this step for now.  
Alternatively open PowerShell and get yourself an SSL certificate if you prefer your own domain with HTTPS.   
After, locate your Nginx repository by navigating to it, for example:  
`cd C:\Users\path\nginx-1.27.3 # (use your current nginx version)`  
Now run the Python file containing the Telegram bot code.  
Finally, open PowerShell again, locate your Nginx directory (cd C:\Users\path\nginx-1.27.3) and enter "start nginx".  
Nginx’s reverse proxy is now activated, together with your domain, the webhook is safely configured, and you can start hosting your own version of Telobot.  
Start trading on the fastest L1 chain now!  

## DISCORD
Discord uses its own gateway, so we do not need to use any of the prior setup, as we run the Discord bot locally and communicate with the Discord gateway directly.  
Go to the Discord Developer Portal, create a new bot, go to OAuth2, and save the “client secret” and keep it safe!  
Go to OAuth2 → URL Generator.  
Select these scopes:  
- bot  
- applications.commands  
Scroll down and select bot permissions, initially these ones:  
- Send Messages  
- Read Messages  
- Use Slash Commands  
Copy the generated invite link and open it in your browser.  
Select your server and click Authorize.  
Now the bot will appear in the list of members in your Discord server.  
Run the discord.py file, and you will have your own version of Telobot in your Discord server.  
Initially it's recommended that you manually disable the bot’s server permissions to send messages in any channel, so it won’t answer users in general chat. Alternatively you can just stop certain /command messages from being sent in a channel, but allow ones that don't require private key signing(like /get_balance). The bot will still respond via DMs.  
The bot can then message each user through DMs. Users must initiate the conversation first by messaging the bot, not the other way around.  
If you only want to use Telobot in your server without creating your own bot, you can invite the public version at this link:  
https://discord.com/oauth2/authorize?client_id=1341228397610926171  
The Discord guide is finished! Happy MonTrading! Gnad <3  

## LINKS
Telegram: https://t.me/tg_Telobot
Discord: https://discord.gg/YXWSefe3uE
