import os
import time
import requests
import logging
from dotenv import load_dotenv
from web3 import Web3
import discord
from discord.ext import commands


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    
# Discord Bot Setup variables
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  
rpc_url = 'https://testnet-rpc.monad.xyz'
web3 = Web3(Web3.HTTPProvider(rpc_url))


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


# ABIs
Router02_abi = [{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
erc20_abi = [{"constant": False, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "success", "type": "bool"}],"type": "function"}, {"constant": True, "inputs": [{"name": "_owner", "type": "address"}, {"name": "_spender", "type": "address"}], "name": "allowance", "outputs": [{"name": "remaining", "type": "uint256"}], "type": "function"},{"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}]


# Contracts and Setup
Router_02 = web3.to_checksum_address("0xfb8e1c3b833f9e67a71c859a132cf783b645e436")
v2_router_contract = web3.eth.contract(address = Router_02, abi = Router02_abi)

user_sessions = {}

# This function retrieves an existing user session or creates a new one if none exists for the given channel. The session stores user-specific settings such as slippage and swap parameters
def get_user_session(channel):
    if channel not in user_sessions:
        user_sessions[channel] = {
            "slippage": 3.0, # Default is 3% if the user hasn't set slippage yet
            "swap_data": {
                "token_in": None,
                "token_out": None,
                "amount_in": None,
                "owner_address": None
            }
        }
    return user_sessions[channel]

# Send a given text message to a specified Discord channel
async def send_message(channel, text):
    await channel.send(text)


# Handler Functions

# This async function handles the /get_balance command to retrieve the MON balance for a given wallet address by calling the RPC endpoint and parsing the result
async def handle_get_balance(text, channel):
    parts = text.split()
    if len(parts) != 2:
        await send_message(channel, "Use /get_balance to retrieve MON balance of any wallet address\n"
        "Send the command /get_balance followed by a wallet address.\n"
        "Example: \n"
        "/get_balance 0x2792617eD35bE902b0aD3faE8d19DF68A20785d2")
        return

    user_address = parts[1].strip()
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [user_address, "latest"],
        "id": 1
    }

    response = requests.post(rpc_url, json=payload, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        result = response.json().get('result')
        if result:
            balance_in_wei = int(result, 16)
            balance_in_mon = balance_in_wei / (10**18)
            await send_message(channel, f"Balance: {balance_in_mon} MON")
        else:
            await send_message(channel, f"Error: {response.status_code}, {response.text}")

# This async function handles the /build_swap command, allowing the user to set tx params for the swap. These parameters are stored in the user's session for later execution
async def handle_build_swap(text, channel):
    parts = text.split()
    if len(parts) != 5:
        await send_message(channel, "Build swap is used to set your transaction parameters before performing a swap (/swap), if successful, your parameters will be permanently saved until you change them.\n"
        "Write the command /build_swap followed by the CA(contract address) of the token you're selling, CA token you're buying, amount and your wallet address.\n\n"
        "Use the same format of this example\n/build_swap 0x760AfE86e5de5fa0Ee542fc7B7B713e1c5425701 0xfe140e1dce99be9f4f15d657cd9b7bf622270c50 0.001 0x0cc01114443f85c9a0933a308efaa863a78d24a4")
        return
    
    

    session = get_user_session(channel)
    swap_data = session["swap_data"]  # user-specific

    swap_data["token_in"] = parts[1].strip()
    swap_data["token_out"] = parts[2].strip()
    swap_data["amount_in"] = parts[3].strip()
    swap_data["owner_address"] = parts[4].strip()

    await send_message(channel, "Swap parameters successfully saved.\n In order to swap, write /swap your_private_key in the same message\n Example:\n/swap 0x5840c7f3e9768c9d74d2029ee3fdd9b984c2150db797ea...")

# This async function handles the /slippage command, enabling the user to set a custom slippage percentage in their session(default slippage is set to 3%)
async def handle_slippage(text, channel):
    parts = text.split()
    if len(parts) != 2:
        await send_message(channel, "Set your slippage by sending the command /slippage followed by a number(2 = 2% slippage)\n\n"
        "Example:\n"
        "/slippage 1")
        return

    session = get_user_session(channel)

    try:
        new_slippage = float(parts[1])
        session["slippage"] = new_slippage
        await send_message(channel, f"Slippage for your session is now {new_slippage}%")
    except ValueError:
        await send_message(channel, "Invalid slippage value. Must be a number")

# This async function handles the /swap command. It increases the allowance to infinity(max), simulates a tx to register an approximate output amount, then computes slippage, builds the swap values and finally sends it to the blockchain through Uni v2 router
async def handle_swap(text, channel):
    parts = text.split()
    if len(parts) != 2:
        await send_message(channel, "To swap, write /swap and your private key in the same message\n"
        "Example:\n"
        "/swap 0x5840c7f3e9768c9d74d2029ee3fdd9b984c2150db797ea...")
        return

    private_key = parts[1].strip()
    session = get_user_session(channel)
    swap_data = session["swap_data"]  
    slippage = session["slippage"]    

    if not all([
        swap_data["token_in"], 
        swap_data["token_out"], 
        swap_data["amount_in"], 
        swap_data["owner_address"]]):
        send_message(channel, "Set your tarnsaction parameters first by using /build_swap")
        return

    # Convert user data
    token_in_address = web3.to_checksum_address(swap_data["token_in"])
    token_out_address = web3.to_checksum_address(swap_data["token_out"])
    owner_address = web3.to_checksum_address(swap_data["owner_address"])
    amount_in_wei = web3.to_wei((swap_data["amount_in"]), "ether") 
    

    # 1) Increase allowance to infinite 
    max_allowance = (2**256) - 1
    token_contract = web3.eth.contract(address=token_in_address, abi=erc20_abi)

    # Build the approval transaction
    approve_tx = token_contract.functions.approve(
        Router_02,
        max_allowance
    ).build_transaction({
        "from": owner_address,
        "gas": 50000,
        "gasPrice": web3.to_wei("50", "gwei"),
        "nonce": web3.eth.get_transaction_count(owner_address),
    })
    
    # Sign & send approval
    signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, private_key)
    approve_hash = web3.eth.send_raw_transaction(signed_approve_tx.raw_transaction)

    # Wait for the approval receipt
    approval_receipt = web3.eth.wait_for_transaction_receipt(approve_hash)
    if approval_receipt.status == 1:
        await send_message(channel, "Token approval successful") 
    else:
        await send_message(channel, "Approval failed")


    # 2) Simulate call 
    amounts_out = v2_router_contract.functions.getAmountsOut(
        amount_in_wei,
        [token_in_address, token_out_address]
    ).call({"from": owner_address})
    
    # Slippage calculation from "amounts_out"
    amount_out_min = int(amounts_out[-1])
    amount_out_minimum = int(amount_out_min * ((100 - slippage) / 100))

    # Tx Deadline(5 minutes)
    deadline = int(time.time()) + 300  

    # 3) Build swap tx
    swap_tx = v2_router_contract.functions.swapExactTokensForTokens(
        amount_in_wei,                # amountIn
        amount_out_minimum,               # amountOutMin
        [token_in_address, token_out_address],  # path array
        owner_address,                   # to
        deadline                      # deadline
    ).build_transaction({
        "from": owner_address,
        "gas": 300000,
        "gasPrice": web3.to_wei("50", "gwei"),
        "nonce": web3.eth.get_transaction_count(owner_address),
    })

    # Sign & send final swap
    try:
        signed_swap = web3.eth.account.sign_transaction(swap_tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_swap.raw_transaction)
        logger.info(f"Swap tx hash: {web3.to_hex(tx_hash)}")
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            await send_message(channel, f"Swap successful! Tx hash: https://monad-testnet.socialscan.io/tx/{web3.to_hex(tx_hash)}") 
        else:
            await send_message(channel,"Swap transaction failed.")
    except Exception as e:
        await send_message(channel, f"Error sending swap transaction: {e}")

# This async function handles the /send_mon command, allowing the user to transfer MON tokens to another address using a specified private key
async def handle_send_mon(text, channel):
    parts = text.split()
    if len(parts) != 4:
        await send_message(channel, "To send MON, enter the command /send_mon followed by the destination address, amount of MON and your private key \n\n"
        "Example:\n"
        "/send_mon 10 0x0d108541070760A491Aea42Dd403E0519C279B7c 0x06dc34eb467f1b6088bc0c4b462ac18783da1d4ef0d853b...")
        return

    amount_input = parts[1].strip()
    raw_recipient_addres = parts[2].strip()
    private_key = parts[3].strip()

    user_account = web3.eth.account.from_key(private_key)
    from_address = user_account.address
    to_address = web3.to_checksum_address(raw_recipient_addres)
    amount_in_wei = web3.to_wei(float(amount_input), 'ether') 
    nonce = web3.eth.get_transaction_count(from_address)
    tx_data = {
        'chainId': 10143, 
        'type': '0x2',
        'nonce': nonce,
        'from': from_address,
        'to': to_address,
        'value': amount_in_wei,
        'maxFeePerGas': web3.to_wei('50', 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei('10', 'gwei'),
    }

    gas_estimated = web3.eth.estimate_gas(tx_data)
    tx_data['gas'] = gas_estimated

    try:
        signed_tx = web3.eth.account.sign_transaction(tx_data, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            await send_message(channel, f"Tx successful: https://monad-testnet.socialscan.io/tx/{web3.to_hex(tx_hash)}")
        else:
            await send_message(channel, "MON transfer transaction failed.")
    except Exception as e:
        await send_message(channel, f"Error sending MON: {e}")

# Discord Bot Event Handlers

# This async event is called when the bot has successfully connected to Discord and is ready to start receiving and processing messages
@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")


# This async event is triggered whenever a message is sent in a channel that the bot has access to. It checks for specific commands (prefixed with '/') and routes them to the corresponding handler functions
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    text_raw = message.content.strip()
    text_lower = text_raw.lower()

    if text_lower == "/start":
        await send_message(message.channel,
            "Gmonad! Welcome to Telobot, an open source Python Telegram & Discord wallet native to Monad, developed and maintained by @telog14 on X, with the help of the Monad developer community.\n\n"
            "## Links:\nGithub repository:https://github.com/telog14/TeloBot\nTelegram bot:...\nDiscord bot & server: https://discord.gg/YXWSefe3uE\n\n"
            "## Tutorial\n"
            "Currently through this bot you can send MON to another wallet, check MON balance of any address, build a swap, set slippage and swap through Uniswap v2 pools \n"
            "List of commands:\n /start, /build_swap, /get_balance, /send_mon, /slippage, /swap\n\n"
            "## Terms and Conditions\n This software is provided 'as is' without warranty of any kind, express or implied. \n The creator disclaims all liability for damages resulting from the use or inability to use the software.\n By using this software, you agree that you do so at your own risk.\n"
            "Hope you enjoy it 💜🦔"
        )
        return

    if text_lower.startswith("/slippage"):
        await handle_slippage(text_raw, message.channel)
        return

    if text_lower.startswith("/get_balance"):
        await handle_get_balance(text_raw, message.channel)
        return

    if text_lower.startswith("/build_swap"):
        await handle_build_swap(text_raw, message.channel)
        return

    if text_lower.startswith("/swap"):
        await handle_swap(text_raw, message.channel)
        return

    if text_lower.startswith("/send_mon"):
        await handle_send_mon(text_raw, message.channel)
        return

# Main & Discord bot running logger
if __name__ == '__main__':
    logger.info("Discord bot running") 
    bot.run(TOKEN)
