import os
import time
import requests
import logging
from dotenv import load_dotenv
from web3 import Web3
import discord
from discord.ext import commands
from eth_account import Account
import secrets

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

erc721_nft_mint_contract_abi = [{"inputs":[],"name":"AllowlistStageNotActive","type":"error"},{"inputs":[],"name":"AlreadyInitialized","type":"error"},{"inputs":[],"name":"ApprovalCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"ApprovalQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"BalanceQueryForZeroAddress","type":"error"},{"inputs":[],"name":"CannotExceedMaxSupply","type":"error"},{"inputs":[],"name":"InvalidAllowlistStageTime","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"InvalidProof","type":"error"},{"inputs":[],"name":"InvalidPublicStageTime","type":"error"},{"inputs":[],"name":"InvalidQueryRange","type":"error"},{"inputs":[],"name":"InvalidStageTime","type":"error"},{"inputs":[],"name":"MaxSupplyCannotBeGreaterThan2ToThe64thPower","type":"error"},{"inputs":[],"name":"MaxSupplyCannotBeIncreased","type":"error"},{"inputs":[],"name":"MaxSupplyCannotBeLessThanCurrentSupply","type":"error"},{"inputs":[],"name":"MintERC2309QuantityExceedsLimit","type":"error"},{"inputs":[],"name":"MintToZeroAddress","type":"error"},{"inputs":[],"name":"MintZeroQuantity","type":"error"},{"inputs":[],"name":"NewOwnerIsZeroAddress","type":"error"},{"inputs":[],"name":"NoHandoverRequest","type":"error"},{"inputs":[],"name":"NotCompatibleWithSpotMints","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[],"name":"OwnerQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"OwnershipNotInitializedForExtraData","type":"error"},{"inputs":[],"name":"PayoutRecipientCannotBeZeroAddress","type":"error"},{"inputs":[],"name":"PublicStageNotActive","type":"error"},{"inputs":[],"name":"RequiredValueNotMet","type":"error"},{"inputs":[],"name":"RoyaltyOverflow","type":"error"},{"inputs":[],"name":"RoyaltyReceiverIsZeroAddress","type":"error"},{"inputs":[],"name":"SequentialMintExceedsLimit","type":"error"},{"inputs":[],"name":"SequentialUpToTooSmall","type":"error"},{"inputs":[],"name":"SpotMintTokenIdTooSmall","type":"error"},{"inputs":[],"name":"TokenAlreadyExists","type":"error"},{"inputs":[],"name":"TransferCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"TransferFromIncorrectOwner","type":"error"},{"inputs":[],"name":"TransferToNonERC721ReceiverImplementer","type":"error"},{"inputs":[],"name":"TransferToZeroAddress","type":"error"},{"inputs":[],"name":"URIQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"Unauthorized","type":"error"},{"inputs":[],"name":"WalletLimitExceeded","type":"error"},{"anonymous":False,"inputs":[{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"indexed":False,"internalType":"struct AllowlistStage","name":"stage","type":"tuple"}],"name":"AllowlistStageSet","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"approved","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":False,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_fromTokenId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_toTokenId","type":"uint256"}],"name":"BatchMetadataUpdate","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"toTokenId","type":"uint256"},{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"}],"name":"ConsecutiveTransfer","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"string","name":"_contractURI","type":"string"}],"name":"ContractURIUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[],"name":"MagicDropTokenDeployed","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"newMaxSupply","type":"uint256"}],"name":"MaxSupplyUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"pendingOwner","type":"address"}],"name":"OwnershipHandoverCanceled","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"pendingOwner","type":"address"}],"name":"OwnershipHandoverRequested","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"newPayoutRecipient","type":"address"}],"name":"PayoutRecipientSet","type":"event"},{"anonymous":False,"inputs":[{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],"indexed":False,"internalType":"struct PublicStage","name":"stage","type":"tuple"}],"name":"PublicStageSet","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"receiver","type":"address"},{"indexed":False,"internalType":"uint256","name":"bps","type":"uint256"}],"name":"RoyaltyInfoUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"qty","type":"uint256"}],"name":"TokenMinted","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_walletLimit","type":"uint256"}],"name":"WalletLimitUpdated","type":"event"},{"inputs":[],"name":"BPS_DENOMINATOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PROTOCOL_FEE_BPS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PROTOCOL_FEE_RECIPIENT","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cancelOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"pendingOwner","type":"address"}],"name":"completeOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"contractNameAndVersion","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"contractURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"internalType":"uint256","name":"toTokenId","type":"uint256"}],"name":"emitBatchMetadataUpdate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"explicitOwnershipOf","outputs":[{"components":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint64","name":"startTimestamp","type":"uint64"},{"internalType":"bool","name":"burned","type":"bool"},{"internalType":"uint24","name":"extraData","type":"uint24"}],"internalType":"struct IERC721A.TokenOwnership","name":"ownership","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"name":"explicitOwnershipsOf","outputs":[{"components":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint64","name":"startTimestamp","type":"uint64"},{"internalType":"bool","name":"burned","type":"bool"},{"internalType":"uint24","name":"extraData","type":"uint24"}],"internalType":"struct IERC721A.TokenOwnership[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAllowlistStage","outputs":[{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"internalType":"struct AllowlistStage","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getConfig","outputs":[{"components":[{"internalType":"uint256","name":"maxSupply","type":"uint256"},{"internalType":"uint256","name":"walletLimit","type":"uint256"},{"internalType":"string","name":"baseURI","type":"string"},{"internalType":"string","name":"contractURI","type":"string"},{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],"internalType":"struct PublicStage","name":"publicStage","type":"tuple"},{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"internalType":"struct AllowlistStage","name":"allowlistStage","type":"tuple"},{"internalType":"address","name":"payoutRecipient","type":"address"},{"internalType":"address","name":"royaltyRecipient","type":"address"},{"internalType":"uint96","name":"royaltyBps","type":"uint96"}],"internalType":"struct SetupConfig","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPublicStage","outputs":[{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],"internalType":"struct PublicStage","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"address","name":"_owner","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"qty","type":"uint256"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"mintAllowlist","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"qty","type":"uint256"}],"name":"mintPublic","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"result","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"pendingOwner","type":"address"}],"name":"ownershipHandoverExpiresAt","outputs":[{"internalType":"uint256","name":"result","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"payoutRecipient","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"requestOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"royaltyAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"royaltyBps","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"salePrice","type":"uint256"}],"name":"royaltyInfo","outputs":[{"internalType":"address","name":"receiver","type":"address"},{"internalType":"uint256","name":"royaltyAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"internalType":"struct AllowlistStage","name":"stage","type":"tuple"}],"name":"setAllowlistStage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newBaseURI","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newContractURI","type":"string"}],"name":"setContractURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newMaxSupply","type":"uint256"}],"name":"setMaxSupply","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newPayoutRecipient","type":"address"}],"name":"setPayoutRecipient","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],"internalType":"struct PublicStage","name":"stage","type":"tuple"}],"name":"setPublicStage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newReceiver","type":"address"},{"internalType":"uint96","name":"newBps","type":"uint96"}],"name":"setRoyaltyInfo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newWalletLimit","type":"uint256"}],"name":"setWalletLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"maxSupply","type":"uint256"},{"internalType":"uint256","name":"walletLimit","type":"uint256"},{"internalType":"string","name":"baseURI","type":"string"},{"internalType":"string","name":"contractURI","type":"string"},{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],"internalType":"struct PublicStage","name":"publicStage","type":"tuple"},{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"internalType":"struct AllowlistStage","name":"allowlistStage","type":"tuple"},{"internalType":"address","name":"payoutRecipient","type":"address"},{"internalType":"address","name":"royaltyRecipient","type":"address"},{"internalType":"uint96","name":"royaltyBps","type":"uint96"}],"internalType":"struct SetupConfig","name":"config","type":"tuple"}],"name":"setup","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"start","type":"uint256"},{"internalType":"uint256","name":"stop","type":"uint256"}],"name":"tokensOfOwnerIn","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"totalMintedByUser","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"result","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"walletLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]

erc1155_nft_mint_contract_abi = [{"inputs":[],"name":"AccountBalanceOverflow","type":"error"},{"inputs":[],"name":"AllowlistStageNotActive","type":"error"},{"inputs":[],"name":"AlreadyInitialized","type":"error"},{"inputs":[],"name":"ArrayLengthsMismatch","type":"error"},{"inputs":[],"name":"CannotExceedMaxSupply","type":"error"},{"inputs":[],"name":"InsufficientBalance","type":"error"},{"inputs":[],"name":"InvalidAllowlistStageTime","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"InvalidProof","type":"error"},{"inputs":[],"name":"InvalidPublicStageTime","type":"error"},{"inputs":[],"name":"InvalidStageTime","type":"error"},{"inputs":[],"name":"MaxSupplyCannotBeGreaterThan2ToThe64thPower","type":"error"},{"inputs":[],"name":"MaxSupplyCannotBeIncreased","type":"error"},{"inputs":[],"name":"MaxSupplyCannotBeLessThanCurrentSupply","type":"error"},{"inputs":[],"name":"NewOwnerIsZeroAddress","type":"error"},{"inputs":[],"name":"NoHandoverRequest","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[],"name":"NotOwnerNorApproved","type":"error"},{"inputs":[],"name":"PayoutRecipientCannotBeZeroAddress","type":"error"},{"inputs":[],"name":"PublicStageNotActive","type":"error"},{"inputs":[],"name":"RequiredValueNotMet","type":"error"},{"inputs":[],"name":"RoyaltyOverflow","type":"error"},{"inputs":[],"name":"RoyaltyReceiverIsZeroAddress","type":"error"},{"inputs":[],"name":"TransferToNonERC1155ReceiverImplementer","type":"error"},{"inputs":[],"name":"TransferToZeroAddress","type":"error"},{"inputs":[],"name":"Unauthorized","type":"error"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"WalletLimitExceeded","type":"error"},{"anonymous":False,"inputs":[{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"indexed":False,"internalType":"struct AllowlistStage","name":"stage","type":"tuple"}],"name":"AllowlistStageSet","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":False,"internalType":"bool","name":"isApproved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_fromTokenId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_toTokenId","type":"uint256"}],"name":"BatchMetadataUpdate","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"string","name":"_contractURI","type":"string"}],"name":"ContractURIUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[],"name":"MagicDropTokenDeployed","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_tokenId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_oldMaxSupply","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_newMaxSupply","type":"uint256"}],"name":"MaxSupplyUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"pendingOwner","type":"address"}],"name":"OwnershipHandoverCanceled","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"pendingOwner","type":"address"}],"name":"OwnershipHandoverRequested","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"newPayoutRecipient","type":"address"}],"name":"PayoutRecipientSet","type":"event"},{"anonymous":False,"inputs":[{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],"indexed":False,"internalType":"struct PublicStage","name":"stage","type":"tuple"}],"name":"PublicStageSet","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"receiver","type":"address"},{"indexed":False,"internalType":"uint256","name":"bps","type":"uint256"}],"name":"RoyaltyInfoUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"qty","type":"uint256"}],"name":"TokenMinted","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"indexed":False,"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"name":"TransferBatch","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"TransferSingle","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"string","name":"value","type":"string"},{"indexed":True,"internalType":"uint256","name":"id","type":"uint256"}],"name":"URI","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_tokenId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_walletLimit","type":"uint256"}],"name":"WalletLimitUpdated","type":"event"},{"inputs":[],"name":"BPS_DENOMINATOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PROTOCOL_FEE_BPS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PROTOCOL_FEE_RECIPIENT","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"result","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"owners","type":"address[]"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"}],"name":"balanceOfBatch","outputs":[{"internalType":"uint256[]","name":"balances","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"qty","type":"uint256[]"}],"name":"batchBurn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"qty","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cancelOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"pendingOwner","type":"address"}],"name":"completeOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"contractNameAndVersion","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"contractURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"internalType":"uint256","name":"toTokenId","type":"uint256"}],"name":"emitBatchMetadataUpdate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getAllowlistStage","outputs":[{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"internalType":"struct AllowlistStage","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getConfig","outputs":[{"components":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"maxSupply","type":"uint256"},{"internalType":"uint256","name":"walletLimit","type":"uint256"},{"internalType":"string","name":"baseURI","type":"string"},{"internalType":"string","name":"contractURI","type":"string"},{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],"internalType":"struct PublicStage","name":"publicStage","type":"tuple"},{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"internalType":"struct AllowlistStage","name":"allowlistStage","type":"tuple"},{"internalType":"address","name":"payoutRecipient","type":"address"},{"internalType":"address","name":"royaltyRecipient","type":"address"},{"internalType":"uint96","name":"royaltyBps","type":"uint96"}],"internalType":"struct SetupConfig","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getPublicStage","outputs":[{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],"internalType":"struct PublicStage","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"address","name":"_owner","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"qty","type":"uint256"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mintAllowlist","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"qty","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mintPublic","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"result","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"pendingOwner","type":"address"}],"name":"ownershipHandoverExpiresAt","outputs":[{"internalType":"uint256","name":"result","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"payoutRecipient","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"requestOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"royaltyAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"royaltyBps","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"salePrice","type":"uint256"}],"name":"royaltyInfo","outputs":[{"internalType":"address","name":"receiver","type":"address"},{"internalType":"uint256","name":"royaltyAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeBatchTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"internalType":"struct AllowlistStage","name":"stage","type":"tuple"}],"name":"setAllowlistStage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"isApproved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newBaseURI","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newContractURI","type":"string"}],"name":"setContractURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"newMaxSupply","type":"uint256"}],"name":"setMaxSupply","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newPayoutRecipient","type":"address"}],"name":"setPayoutRecipient","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],"internalType":"struct PublicStage","name":"stage","type":"tuple"}],"name":"setPublicStage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newReceiver","type":"address"},{"internalType":"uint96","name":"newBps","type":"uint96"}],"name":"setRoyaltyInfo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"newWalletLimit","type":"uint256"}],"name":"setWalletLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"maxSupply","type":"uint256"},{"internalType":"uint256","name":"walletLimit","type":"uint256"},{"internalType":"string","name":"baseURI","type":"string"},{"internalType":"string","name":"contractURI","type":"string"},{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],"internalType":"struct PublicStage","name":"publicStage","type":"tuple"},{"components":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"internalType":"struct AllowlistStage","name":"allowlistStage","type":"tuple"},{"internalType":"address","name":"payoutRecipient","type":"address"},{"internalType":"address","name":"royaltyRecipient","type":"address"},{"internalType":"uint96","name":"royaltyBps","type":"uint96"}],"internalType":"struct SetupConfig","name":"config","type":"tuple"}],"name":"setup","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"totalMinted","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"totalMintedByUser","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"uri","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"walletLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]


# Contracts and Setup
# Recipient is the Telobot reserve wallet
recipient = web3.to_checksum_address("0x7588b77A593FF3cF7dE4F565De3Adfcb993A11F4")
Router_02 = web3.to_checksum_address("0xfb8e1c3b833f9e67a71c859a132cf783b645e436")
v2_router_contract = web3.eth.contract(address = Router_02, abi = Router02_abi)


user_sessions = {}

'''  RETRIEVE USER SESSION   '''
# This function retrieves an existing user session or creates a new one if none exists for the given channel. The session stores user-specific settings such as slippage and swap parameters
def get_user_session(channel):
    if channel not in user_sessions:
        user_sessions[channel] = {
            "slippage": 3.0, # Default is 3% if the user hasn't set a slippage yet
            "token_in": None,
            "token_out": None,
            "amount_in": None,
            "wallet_address_global": None,
            "gasprice_ingwei_global": 63,
            "nft_contract_address": None,
            "nft_mint_price": 0, # Default is 0 equating to free minting if the user hasn't set a mint price yet
        }
    return user_sessions[channel]


# Send a given text message to a specified Discord channel
async def send_message(channel, text):
    await channel.send(text)



''' # GENERATE PRIVATE KEY & ADDRESS'''
# The /generate_address_and_pvkey command enables the user to generate a private key and wallet pair with maximum level of entropy
async def handle_address_and_privatekey(text, chat_id):
    if text == "/generate_address_and_pvkey":
        seed_string = secrets.token_hex(32)
        acct1 = Account.create(seed_string)
        await send_message(chat_id, acct1.address)
        await send_message(chat_id, acct1.key.hex())



'''GET BALANCE'''
# The /get_balance command enables the user to retrieve the MON balance for a given wallet address by calling the RPC endpoint and parsing the result
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



'''  SWAP  '''
# This function handles the /swap command. It increases the allowance to infinity(max), simulates a tx to register an approximate output amount, then computes slippage and fee, builds the swap values and finally sends it to the blockchain through Uni v2 router, then pays the fee to the reserve wallet
async def handle_swap(text, channel):
    parts = text.split()
    if len(parts) != 2:
        await send_message(channel, "To swap, write /swap and your private key in the same message\n"
        "Example:\n"
        "/swap 0x5840c7f3e9768c9d74d2029ee3fdd9b984c2150db797ea...")
        return

    private_key = parts[1].strip()
    session = get_user_session(channel)  
    slippage = int(session["slippage"])    

    if not all([
        session["token_in"], 
        session["token_out"], 
        session["amount_in"], 
        session["wallet_address_global"],
        session["gasprice_ingwei_global"]]):
        await send_message(channel, "Set your transaction parameters first by building all parameters individually")
        return

    token_in = str(web3.to_checksum_address(session["token_in"]))
    token_out = str(web3.to_checksum_address(session["token_out"]))
    amount_in = web3.to_wei(float(session["amount_in"]), "ether")
    wallet_address = str(web3.to_checksum_address(session["wallet_address_global"])) 
    gas_price = float(session["gasprice_ingwei_global"])


    # 1) Increase allowance to infinite 
    max_allowance = (2**256) - 1
    token_contract = web3.eth.contract(address = token_in, abi = erc20_abi)
    nonce = web3.eth.get_transaction_count(wallet_address)
    
    # Build the approval transaction
    approve_tx = token_contract.functions.approve(
        Router_02,
        max_allowance
    ).build_transaction({
        "from": wallet_address,
        "gas": 50000,
        "gasPrice": web3.to_wei(gas_price, "gwei"),
        "nonce": nonce,
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
        amount_in,
        [token_in, token_out]
    ).call({"from": wallet_address})
    
    # Slippage calculation from "amounts_out"
    amount_out_min = int(amounts_out[-1])
    amount_out_minimum = int(amount_out_min * ((100 - slippage) / 100))

    # Tx Deadline(5 minutes)
    deadline = int(time.time()) + 300  
    nonce1 = web3.eth.get_transaction_count(wallet_address)

    # 3) Build swap tx
    swap_tx = v2_router_contract.functions.swapExactTokensForTokens(
        amount_in,                
        amount_out_minimum,              
        [token_in, token_out],  
        wallet_address,                   
        deadline                      
    ).build_transaction({
        "from": wallet_address,
        "gas": 300000,
        "gasPrice": web3.to_wei(gas_price, "gwei"),
        "nonce": nonce1,
    })

    gas_estimated = web3.eth.estimate_gas(swap_tx)
    swap_tx['gas'] = gas_estimated
    
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
        return

    # Pay for the fee(0.005 MON flat fee)
    nonce2 = web3.eth.get_transaction_count(wallet_address)
    fee_tx_data = {
        'chainId': 10143, 
        'type': '0x2',
        'nonce': nonce2,
        'from': wallet_address,
        'to': recipient,
        'value': web3.to_wei(0.005, "ether"),
        'maxFeePerGas': web3.to_wei('52', 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei('11', 'gwei'),
        'gas': 21000
    }

    fee_signed_tx = web3.eth.account.sign_transaction(fee_tx_data, private_key)
    fee_tx_hash = web3.eth.send_raw_transaction(fee_signed_tx.raw_transaction)



 

'''  SEND MON  '''
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
        'maxFeePerGas': web3.to_wei('52', 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei('11', 'gwei'),
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




# SET COMMANDS LIST:

'''SET SLIPPAGE'''
# This async function handles the /slippage command, enabling the user to set a custom slippage percentage in their session(default slippage is set to 3%)
async def handle_set_slippage(text, channel):
    parts = text.split()
    if text == "/set_slippage":
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
        await send_message(channel, "Invalid slippage value, please try again")


'''  TOKEN_IN  '''
# The /set_swap_token_in command enables the user to set the token contract address used to swap
async def handle_set_swap_token_in(text, channel):
    parts = text.split()
    if text == "/set_swap_token_in" :
        await send_message(channel, "enter the contract address of the token you own and want to SELL")
        return
    
    session = get_user_session(channel)

    try:
        user_token_in = str(parts[1])
        session["token_in"] = user_token_in
        await send_message(channel, f"The CA of the token you will SELL is {user_token_in}")
    except ValueError:
        await send_message(channel, "Invalid contract address, please try again")

'''  TOKEN OUT  '''
# The /set_swap_token_in command enables the user to set the incoming contract address token, received after the swap is executed
async def handle_set_swap_token_out(text, channel):
    parts = text.split()
    if text == "/set_swap_token_out" :
        await send_message(channel, "enter the contract address of the token you want to BUY")
        return
    
    session = get_user_session(channel)

    try:
        user_token_out = str(parts[1])
        session["token_out"] = user_token_out
        await send_message(channel, f"The CA of the token you will BUY is {user_token_out}")
    except ValueError:
        await send_message(channel, "Invalid contract address, please try again")



'''   AMOUNT IN   '''
# The /set_swap_amount_in command enables the user to set the amount of token_in they wish to swap 
async def handle_set_swap_amount_in(text, channel):
    parts = text.split()
    if text == "/set_swap_amount_in" :
        await send_message(channel, "Enter the amount of tokens you own and want to sell")
        return
    
    session = get_user_session(channel)

    try:
        user_amount_in = float(parts[1])
        session["amount_in"] = user_amount_in
        await send_message(channel, f"The amount of tokens you will swap is  {user_amount_in}")
    except ValueError:
        await send_message(channel, "Invalid amount, please try again")


''' WALLET ADDRESS'''
# The /set_wallet_address_global command enables the user to set the wallet address used to snipe mints or swap
async def handle_set_wallet_address_global(text, channel):
    parts = text.split()
    if text == "/set_wallet_address_global" :
        await send_message(channel, "enter the wallet address you will use to mint or swap")
        return
    
    session = get_user_session(channel)

    try:
        user_wallet_address = str(parts[1])
        session["wallet_address_global"] = user_wallet_address
        await send_message(channel, f"Your wallet is saved as: {user_wallet_address}")
    except ValueError:
        await send_message(channel, "Invalid wallet address, please try again")





''' GWEI GAS  '''
# The /set_gas_global command enables the user to set the gas price used for the transaction, in gwei
async def handle_set_gas_global(text, channel):
    parts = text.split()
    if text == "/set_gas_global" :
        await send_message(channel, "enter the gas price in GWEI(higher GWEI means faster tx execution)")
        return
    
    session = get_user_session(channel)

    try:
        user_gasprice_gwei = int(parts[1])
        session["gasprice_ingwei_global"] = user_gasprice_gwei
        await send_message(channel, f"Gwei has been set to {user_gasprice_gwei}")
    except ValueError:
        await send_message(channel, "Invalid gas price, please try again")




'''NFT MINT PRICE'''
# This function handles the /set_nft_mint_price, enabling the user to set the price for the nft mint, in MON
async def handle_set_nft_mint_price(text, channel):
    parts = text.split()
    if text == "/set_nft_mint_price" :
        await send_message(channel, "enter the mint price of the nft you want to mint")
        return
    
    session = get_user_session(channel)

    try:
        user_nft_mint_price = float(parts[1])
        session["nft_mint_price"] = user_nft_mint_price
        await send_message(channel, f"The mint price has been set to {user_nft_mint_price}")
    except ValueError:
        await send_message(channel, "Invalid nft mint price, please try again")



'''NFT CONTRACT ADDRESS'''
# This function handles the /set_nft_contract_address command, enabling the user to set the contract address of the nft collection they wish to mint. 
# The address can be set to either ERC-721 or ERC-1155 token standard
async def handle_set_nft_contract_address(text, channel):
    parts = text.split()
    
    if len(parts) < 2:
        await send_message(channel, "Enter the command /set_nft_contract_address followed by the contract address of the nft collection you want to mint, in the same message. Example: /set_nft_contract_address 0xf1be82ec22644a3a4ecd374f77d3009e045d6882")
        return
    
    session = get_user_session(channel)
    
    try:
        user_nft_wallet_address = str(parts[1])
        session["nft_contract_address"] = user_nft_wallet_address
        await send_message(channel, f"The contract address of the NFT you want to mint is {user_nft_wallet_address}")
    except IndexError:
        await send_message(channel, "Invalid NFT contract address, please try again.")



'''  SHOW TX DATA  '''
# The /show_tx_data command enables the user to verify the correct transaction parameters stored in "user_session", before executing a transaction.
# SWAP, NFT MINTS & OTHER sections have been ordered for improved readability
async def handle_show_tx_data(text, channel):
    if text == "/show_tx_data":
        session = get_user_session(channel)	
        slippage = session["slippage"]
        token_in = session["token_in"]
        token_out = session["token_out"]
        amount_in = session["amount_in"]
        wallet_address_global = session["wallet_address_global"]
        gasprice_ingwei_global = session["gasprice_ingwei_global"]
        nft_contract_address = session["nft_contract_address"]
        nft_mint_price = session["nft_mint_price"]
        await send_message(channel, "Full Transaction Data\n\n"
        "SWAP: \n"
        f"slippage = {slippage} \n"
        f"token in = {token_in} \n"
        f"token out = {token_out} \n"
        f"swap amount = {amount_in} \n\n"
        "GLOBAL DATA:\n"
        f"wallet address *global* = {wallet_address_global} \n"
        f"gas price in gwei *global* = {gasprice_ingwei_global} \n\n"
        "NFT MINT:\n"
        f"nft mint price = {nft_mint_price} \n"
        f"nft contract address = {nft_contract_address} \n\n"
        "NOTE: 'wallet address' and 'gas price in gwei' must always be filled. \n"
        " 'nft mint price' and 'nft contract address' must be filled only for nft mints")




'''   MINT ERC-721   '''
# This function handles the /snipe_nft_mint_erc721 command, enabling the user to snipe any MagicEden ERC-721 public mint. First we make sure all paramaters have been imported correctly, then we check that the user has enough balance for fees. After that we execute the mint tx and calculate the outgoing fee to our reserve wallet address
async def handle_snipe_nft_mint_erc721(text, channel):
    parts = text.split()
    if len(parts) != 2:
        await send_message(channel, "To mint an NFT, enter the command /snipe_nft_mint_erc721 followed by your private key \n\n"
        "Example:\n"
        "/snipe_mint_nft_erc721 0x5840c7f3e9768c9d74d2029ee3fdd9b984c2150db797ea...")
        return

    private_key = parts[1].strip()
    session = get_user_session(channel)

    # 1) Get raw values from session
    gas_global_raw = session["gasprice_ingwei_global"]
    wallet_address_global_raw = session["wallet_address_global"]
    nft_contract_address_raw = session["nft_contract_address"]
    nft_mint_price_raw = session["nft_mint_price"]  

    # 2) Check if any are None
    if any(param is None for param in [gas_global_raw, wallet_address_global_raw, nft_contract_address_raw, nft_mint_price_raw]):
        await send_message(channel, "Set your transaction parameters first by building all parameters individually: gas price, wallet address, NFT CA, and NFT mint price.")
        return

    # 3) Convert values to make sure None is not returned
    gas_price = web3.to_wei(float(gas_global_raw), 'gwei')
    wallet_address_global = web3.to_checksum_address(wallet_address_global_raw)
    nft_contract_address1 = web3.to_checksum_address(nft_contract_address_raw)
    nft_mint_price = web3.to_wei(float(nft_mint_price_raw), "ether")
    erc721_contract = web3.eth.contract(address = web3.to_checksum_address(nft_contract_address1), abi = erc721_nft_mint_contract_abi)


    # Do a balance retrieval to make sure the user has enough MON to pay for fees,if the mint price is 1 >= MON, the balance must be at least 5% more than mint price, if it isn't the tx is reverted.
    # If the mint price is less than 1 mon we make sure the user has at least an additional 0.05 MON, if he does, we apply a 0.025 MON flat fee, otherwise we apply a 2.5% fixed rate fee
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [wallet_address_global, "latest"],
        "id": 1
    }

    response = requests.post(rpc_url, json=payload, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        result = response.json().get('result')
        user_balance = int(result, 16)
    else: 
        await send_message(channel, "wallet balance retrieval failed, please try sending the transaction again")
        return
    
    perc_difference = int(nft_mint_price * 105 // 100)  
    
    if user_balance < perc_difference and user_balance != 0:
        await send_message(channel, "not enough balance")
        return

    
    additional_balance = web3.to_wei(0.05, 'ether')  
    
    if (user_balance - nft_mint_price) < additional_balance:
        await send_message(channel, "not enough balance, need at least 0.05 MON in addition to your NFT mint price")
        return

    
    # Estimate gas for the nft smart contract
    qty = 1
    nonce = web3.eth.get_transaction_count(wallet_address_global)

    gas_estimate = erc721_contract.functions.mintPublic(
        wallet_address_global,
        qty
    ).estimate_gas({
        'from': wallet_address_global,
        'value': nft_mint_price
    })    


    # 4) Build transaction for the public mint function
    tx_mint = erc721_contract.functions.mintPublic(wallet_address_global, qty).build_transaction({
        'chainId': 10143,
        'from': wallet_address_global,
        'nonce': nonce,
        'gas': gas_estimate,           
        'maxFeePerGas': gas_price,
        'maxPriorityFeePerGas': gas_price,
        'value': nft_mint_price     
    })


    # Sign and send the tx
    signed_mint = web3.eth.account.sign_transaction(tx_mint, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_mint.raw_transaction)
    await send_message(channel, "Transaction Submitted")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    

    if tx_receipt.status == 1:
        await send_message(channel, f"Mint successful! Tx hash: https://monad-testnet.socialscan.io/tx/{web3.to_hex(tx_hash)}")
    else:
        await send_message(channel, f"Mint failed. {web3.to_hex(tx_hash)}\n "
        "Reasons:\n"
        "1)Incorrect contract address or mint price \n"
        "2)Gas too low\n "
        "3)Mint didn't start or already ended\n"
        "4) Not enough balance")
        return
    
    nonce1 = web3.eth.get_transaction_count(wallet_address_global)
    mon_1 = web3.to_wei(1, "ether")

    # 5) Pay the fee. If the mint price is less than 1 MON, fee is a flat 0.025 MON in Wei
    if nft_mint_price < mon_1:
        fee = web3.to_wei(0.025, 'ether')
    else:
        fee = int(nft_mint_price * 0.025)

    tx_data = {
        'chainId': 10143, 
        'type': '0x2',
        'nonce': nonce1,
        'from': wallet_address_global,
        'to': recipient,
        'value': fee,
        'gas': 21000,
        'maxFeePerGas': web3.to_wei('52', 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei('11', 'gwei'),
    }
    

    # Sign and send
    tx_fee = web3.eth.account.sign_transaction(tx_data, private_key)
    tx_hash_fee = web3.eth.send_raw_transaction(tx_fee.raw_transaction)


'''   MINT ERC-1155   '''
# This function handles the /snipe_nft_mint_erc1155 command, enabling the user to snipe any MagicEden ERC-1155 public mint. First we make sure all paramaters have been imported correctly, then we check that the user has enough balance for fees. After that we execute the mint tx and calculate the outgoing fee to our reserve wallet address

async def handle_snipe_nft_mint_erc1155(text, channel):

    parts = text.split()
    if len(parts) != 2:
        await send_message(channel, "To mint an NFT, enter the command /snipe_mint_nft_erc1155 followed by your private key \n\n"
        "Example:\n"
        "/snipe_nft_mint_erc1155 0x5840c7f3e9768c9d74d2029ee3fdd9b984c2150db797ea...")
        return

    private_key = parts[1].strip()
    session = get_user_session(channel)

    # First we import tx parameters (raw) and then we make sure they aren't defined as "None", after that we convert and cast them into float/string
    gas_global_raw = session["gasprice_ingwei_global"]
    wallet_address_global_raw = session["wallet_address_global"]
    nft_contract_address_raw = session["nft_contract_address"]
    nft_mint_price_raw = session["nft_mint_price"]  

    # Check if any are None
    if any(param is None for param in [gas_global_raw, wallet_address_global_raw, nft_contract_address_raw, nft_mint_price_raw]):
        await send_message(channel, "Set your transaction parameters first by building all parameters individually: gas price, wallet address, NFT CA, and NFT mint price.")
        return

    # Convert parameters to float/string, they shouldn't be "None" by this point
    gas_price = web3.to_wei(float(gas_global_raw), 'gwei')
    wallet_address_global = web3.to_checksum_address(wallet_address_global_raw)
    nft_contract_address = web3.to_checksum_address(nft_contract_address_raw)
    nft_mint_price = web3.to_wei(float(nft_mint_price_raw), "ether")   
    erc1155_contract = web3.eth.contract(address=web3.to_checksum_address(nft_contract_address), abi = erc1155_nft_mint_contract_abi)

    # As with ERC-721 mint, we do a balance retrieval to make sure the user has enough MON to pay for fees,if the mint price is 1 >= MON, the balance must be at least 5% more than mint price, if it isn't the tx is reverted.
    # If the mint price is less than 1 mon we make sure the user has at least an additional 0.05 MON, if he does, we apply a 0.025 MON flat fee, otherwise we apply a 2.5% fixed rate fee
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [wallet_address_global, "latest"],
        "id": 1
    }

    response = requests.post(rpc_url, json=payload, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        result = response.json().get('result')
        user_balance = int(result, 16)
    else: 
        await send_message(channel, "wallet balance retrieval failed, please try sending the transaction again")
        return
    
    
    perc_difference = int(nft_mint_price * 105 // 100)    

    if user_balance < perc_difference and user_balance != 0:
        await send_message(channel, "not enough balance")
        return

    additional_balance = web3.to_wei(0.05, 'ether')  
    
    if (user_balance - nft_mint_price) < additional_balance:
        await send_message(channel, "not enough balance, need at least 0.05 MON in addition to your NFT mint price")
        return

    
    qty = 1
    token_id = 0
    nonce = web3.eth.get_transaction_count(wallet_address_global)

    # Estimate gas
    gas_estimate = erc1155_contract.functions.mintPublic(
        wallet_address_global,
        token_id,
        qty,
        b''
    ).estimate_gas({
        'from': wallet_address_global,
        'value': nft_mint_price
    })


    # Build transaction for the "mintPublic" function
    tx_mint = erc1155_contract.functions.mintPublic(
        wallet_address_global,  
        token_id,        
        qty,             
        b''             
    ).build_transaction({
        'chainId': 10143,
        'from': wallet_address_global,
        'nonce': nonce,
        'gas':  gas_estimate, 
        'maxFeePerGas': gas_price,
        'maxPriorityFeePerGas': gas_price,
        'value': nft_mint_price
    })


    # Sign and send
    signed_mint = web3.eth.account.sign_transaction(tx_mint, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_mint.raw_transaction)
    await send_message(channel, "Transaction Submitted")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    

    if tx_receipt.status == 1:
        await send_message(channel, f"Mint successful! Tx hash: https://monad-testnet.socialscan.io/tx/{web3.to_hex(tx_hash)}")
    else:
        await send_message(channel, f"Mint failed. {web3.to_hex(tx_hash)}\n "
        "Reasons:\n"
        "1)Incorrect contract address or mint price \n"
        "2)Gas too low\n "
        "3)Mint didn't start or already ended\n"
        "4) Not enough balance")
        return
    
    nonce1 = web3.eth.get_transaction_count(wallet_address_global)
    mon_1 = web3.to_wei(1, "ether")

    # If the mint price is less than 1 MON, fee is a flat 0.025 MON in Wei
    if nft_mint_price < mon_1:
        fee = web3.to_wei(0.025, 'ether')
    else:
        fee = int(nft_mint_price * 0.025)
 
    tx_data = {
        'chainId': 10143, 
        'type': '0x2',
        'nonce': nonce1,
        'from': wallet_address_global,
        'to': recipient,
        'value': fee,
        'gas': 21000,
        'maxFeePerGas': web3.to_wei('52', 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei('11', 'gwei'),
    }

    

    # Sign and send the tx
    tx_fee = web3.eth.account.sign_transaction(tx_data, private_key)
    tx_hash_fee = web3.eth.send_raw_transaction(tx_fee.raw_transaction)


# Discord Bot Event Handlers

# This async event is called when the bot has successfully connected to Discord and is ready to start receiving and processing messages
@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")


# This async event is triggered whenever a message is sent in a channel that the bot has access to. It checks for specific commands and routes them to the corresponding handler functions
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    text_raw = message.content.strip()
    text_lower = text_raw.lower()

    if text_lower == "/start":
        await send_message(message.channel,
            "Gmonad! Welcome to Telobot, an open source Python Telegram & Discord wallet native to Monad, developed and maintained by @telog14 on X, with the help of the Monad developer community.\n\n"
            "## Links:\nGithub repository: https://github.com/telog14/TeloBot\nTelegram bot(multiple instances): https://t.me/tg_Telobot\n All sessions:  @tg_Telobot , @Mon_Telobot , @Mon2_Telobot \nDiscord bot & server: https://discord.gg/YXWSefe3uE\n\n"
            "## Tutorial: https://discord.com/channels/1197113518391054376/1343278692255662123/1346561615746830486\n"
            "Click the tutorial link that takes you into my discord Channel\n"
            "Don't feel overwhelmed, if you only need to snipe nfts or only swaps, just focus just on your product of interest, afterwards explore the rest of the suite \n"
            "# List of commands with descriptions: https://discord.com/channels/1197113518391054376/1343278692255662123/1350301029001854976\n " 
            "/start\n"
            "/generate_address_and_pvkey \n" 
            "## SNIPE NFT MINT\n" 
            "/set_wallet_address_global\n"
            "/set_gas_global \n"
            "/set_nft_mint_price \n"
            "/set_nft_contract_address\n"
            "/snipe_nft_mint_erc721 \n" 
            "/snipe_nft_mint_erc1155\n" 
            "## INSTANT SWAP\n"
            "/set_slippage\n"
            "/set_swap_token_in\n"
            "/set_swap_token_out\n"
            "/set_swap_amount_in\n" 
            "## VERIFY TX DATA\n"
            "/show_tx_data\n"
            "## GENERAL WALLET UTILITIES\n"
            "/get_balance\n"
            "/send_mon\n\n"
            "## 'global' commands like /set_wallet_address_global and /set_gas_global, must be set only once and are valid for both nft mints and swaps\n"
            "## Terms and Conditions\n This software is provided 'as is' without warranty of any kind, express or implied. \n The creator disclaims all liability for damages resulting from the use or inability to use the software.\n By using this software, you agree that you do so at your own risk.\n"
            "Hope you enjoy it 💜🦔")
        return

    if text_lower.startswith("/get_balance"):
        await handle_get_balance(text_raw, message.channel)
        return

    if text_lower.startswith("/swap"):
        await handle_swap(text_raw, message.channel)
        return
    
    if text_raw == "/generate_address_and_pvkey":
        await handle_address_and_privatekey(text_raw, message.channel)
        return
    
    if text_lower.startswith("/send_mon"):
        await handle_send_mon(text_raw, message.channel)
        return    
    
    # SET TOKEN IN
    if text_lower.startswith("/set_swap_token_in"):
        await handle_set_swap_token_in(text_raw, message.channel)
        return 
    
        # SET TOKEN OUT
    if text_lower.startswith("/set_swap_token_out"):
        await handle_set_swap_token_out(text_raw, message.channel)
        return 
    
    if text_lower.startswith("/set_swap_amount_in"):
        await handle_set_swap_amount_in(text_raw, message.channel)
        return
    
    if text_lower.startswith("/set_slippage"):
        await handle_set_slippage(text_raw, message.channel)
        return
    

    if text_raw == "/show_tx_data":
        await handle_show_tx_data(text_raw, message.channel)
        return
    
    if text_lower.startswith("/set_wallet_address_global"):
        await handle_set_wallet_address_global(text_raw, message.channel)
        return 
    
    if text_lower.startswith("/set_gas_global"):
        await handle_set_gas_global(text_raw, message.channel)
        return 
    
    if text_lower.startswith("/set_nft_mint_price"):
        await handle_set_nft_mint_price(text_raw, message.channel)
        return 
    
    if text_lower.startswith("/set_nft_contract_address"):
        await handle_set_nft_contract_address(text_raw, message.channel)
        return 
    
    if text_lower.startswith("/snipe_nft_mint_erc721"):
        await handle_snipe_nft_mint_erc721(text_raw, message.channel)
        return 
    
    if text_lower.startswith("/snipe_nft_mint_erc1155"):
        await handle_snipe_nft_mint_erc1155(text_raw, message.channel)
        return

# Main & Discord bot running logger
if __name__ == '__main__':
    logger.info("Discord bot running") 
    bot.run(TOKEN)