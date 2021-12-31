from math import ceil

from django.shortcuts import render
from django.views import View

from tracker.presenters.transaction_presenter import TransactionPresenter
from tracker.presenters.transaction_paginator import TransactionPaginator


TRANSACTIONS_PER_PAGE = 10


class TransactionsView(View):
    def get(self, request):
        # TODO: Replace hard-coded transactions with transactions from the database
        # also implement pagination logic
        transactions = [
            {'function': 'empty', 'status': 1, 'TxHash': '0x497a69c7052a78bad5dc4689ca5b48534b80e44ee79d3d388c6f1b7f515291b8', 'timestamp': '2021/08/22, 20:52:04', 'to': '0xabD4741948374b1f5DD5Dd7599AC1f85A34cAcDD', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_Profiles', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00205456, 'TxTokens': {}},
            {'function': 'swapExactETHForTokens', 'status': 1, 'TxHash': '0x8f63d262c193e281263bb7696c3cfad247634440d4d5ac5f154db10eaea48058', 'timestamp': '2021/08/22, 20:55:43', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 10.0, 'TxFee': 0.00123149, 'TxTokens': {'Serendale_JewelToken': 89110543313088510014, 'ONE': -10.0}},
            {'function': 'swapExactETHForTokens', 'status': 0, 'TxHash': '0xfe560b7312cc71789f1dec1e6a4a7f4288108f7e0db03f5fae58fb51fdfd0315', 'timestamp': '2021/08/22, 20:57:23', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 5000.0, 'TxFee': 0.0002915, 'TxTokens': {}},
            {'function': 'swapExactETHForTokens', 'status': 0, 'TxHash': '0xba9aa59b1d4b9eb57f3db457b7b64c8f867636a92077b3b78a73095aee86b996', 'timestamp': '2021/08/22, 20:58:00', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 5000.0, 'TxFee': 0.0002915, 'TxTokens': {}},
            {'function': 'swapExactETHForTokens', 'status': 1, 'TxHash': '0xd8342d111363b4f5b9380cc190feb0dc10604718c9b5809b81ddfa2787e72926', 'timestamp': '2021/08/22, 20:58:55', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 5000.0, 'TxFee': 0.00123149, 'TxTokens': {'Serendale_JewelToken': 5719527964089995841858, 'ONE': -5000.0}},
            {'function': 'approve', 'status': 1, 'TxHash': '0xd8aeb845859b811e786dd2fc35accaacc796b5910519d2165e016923226d5cdc', 'timestamp': '2021/08/22, 21:00:10', 'to': '0x72Cb10C6bfA5624dD07Ef608027E366bd690048F', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_JewelToken', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00044475, 'TxTokens': {}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0xd369f05a3b4654df301d2d79f6af5edf6791e5ed8a685407ab789d181283c998', 'timestamp': '2021/08/22, 21:00:32', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.0013576, 'TxTokens': {'Serendale_JewelToken': -10000000000000000000000, 'ONE': 10082397957569914279806}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0x2ef1efffdffd6ad3a1ca6db3a5fde71596500d4ad507c1f4f64a2edea56bca6f', 'timestamp': '2021/08/22, 21:05:34', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00135736, 'TxTokens': {'Serendale_JewelToken': -1000000000000000000000, 'ONE': 1758374571503925494360}},
            {'function': 'swapExactETHForTokens', 'status': 1, 'TxHash': '0x98f0cc953a1d65db13eb42f5080681212695a45c24b79d3975cfdda441b5b32a', 'timestamp': '2021/08/22, 21:07:22', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 5000.0, 'TxFee': 0.00135309, 'TxTokens': {'Serendale_JewelToken': 2409732209804260124410, 'ONE': -5000.0}},
            {'function': 'swapExactETHForTokens', 'status': 1, 'TxHash': '0x7f84a1dc9d91d2e83c6f87f33e6134d8daef2fcbd0ad095bdedb050b5da99495', 'timestamp': '2021/08/22, 21:09:32', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 5000.0, 'TxFee': 0.00135309, 'TxTokens': {'Serendale_JewelToken': 2648708406465588011327, 'ONE': -5000.0}},
            {'function': 'swapExactETHForTokens', 'status': 1, 'TxHash': '0x375a6e4c81f24db266b4af5f6f15a45c4e475b51f6e99ae7418f4d19c71b9dce', 'timestamp': '2021/08/22, 21:12:29', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 5000.0, 'TxFee': 0.00123149, 'TxTokens': {'Serendale_JewelToken': 1621671734971001132746, 'ONE': -5000.0}},
            {'function': 'swapExactETHForTokens', 'status': 1, 'TxHash': '0x8398819f3a830495815440a184a3b644853d144e4943713dc2bef4d9bb7a1838', 'timestamp': '2021/08/22, 21:17:49', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 4000.0, 'TxFee': 0.00135309, 'TxTokens': {'Serendale_JewelToken': 931938842284299750577, 'ONE': -4000.0}},
            {'function': 'swapExactETHForTokens', 'status': 1, 'TxHash': '0x67600177a2dc359879f9f7648dd7b67b97b2dad4f789e7f429fdf433438ca595', 'timestamp': '2021/08/22, 21:23:16', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 500.0, 'TxFee': 0.00135309, 'TxTokens': {'Serendale_JewelToken': 244678693999706676722, 'ONE': -500.0}},
            {'function': 'approve', 'status': 1, 'TxHash': '0x13fd3c10c0cb7b3a408cef0c06f6a867c5410ef83586624cfd7c7a90a4f3094c', 'timestamp': '2021/08/22, 21:32:27', 'to': '0x72Cb10C6bfA5624dD07Ef608027E366bd690048F', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_JewelToken', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00044475, 'TxTokens': {}},
            {'function': 'enter', 'status': 1, 'TxHash': '0xab3c188189184730ad00d807a577b0e1202a848a67534e2c9adaf961921695ab', 'timestamp': '2021/08/22, 21:32:38', 'to': '0xA9cE83507D872C5e1273E745aBcfDa849DAA654F', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_Bank', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00088101, 'TxTokens': {'Serendale_Bank': 100000000000000000000, 'Serendale_JewelToken': -100000000000000000000}},
            {'function': 'addLiquidityETH', 'status': 1, 'TxHash': '0xed306a85a0915f28c457ac225405d8ba907f5a7610e8ee4598cb132d5f983def', 'timestamp': '2021/08/22, 21:34:43', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 40.0, 'TxFee': 0.0018203100000000001, 'TxTokens': {'Serendale_JewelToken': -13416513661512055948, 'Jewel LP Token (JEWEL-LP)': 22976183246988234382, 'ONE': -40.0}},
            {'function': 'approve', 'status': 1, 'TxHash': '0x71ea8e298e48c842f160c2acd60627dffddf5fd9a2f5609c31e28143092b46f7', 'timestamp': '2021/08/22, 21:35:26', 'to': '0xEb579ddcD49A7beb3f205c9fF6006Bb6390F138f', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Jewel LP Token (JEWEL-LP)', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00044354, 'TxTokens': {}},
            {'function': 'deposit', 'status': 1, 'TxHash': '0x2bd47b9eb7a8ba239e91b72b7a5a4034623f9a253fa01329b9f91a6175013338', 'timestamp': '2021/08/22, 21:35:55', 'to': '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_MasterGardener', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.0016628, 'TxTokens': {'Jewel LP Token (JEWEL-LP)': -22976183246988234382}},
            {'function': 'swapExactETHForTokens', 'status': 1, 'TxHash': '0x2d9d7217cde6bc0bf44e89be908a5eded7252419f19419e18152164ced0dda1f', 'timestamp': '2021/08/22, 21:54:30', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 50.0, 'TxFee': 0.00123137, 'TxTokens': {'Serendale_JewelToken': 23902080834681083883, 'ONE': -50.0}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0x1a24f8416c9e6bf92e559fe6083ac02ad934e095eabf119d771c727623f38560', 'timestamp': '2021/08/22, 22:18:45', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00123576, 'TxTokens': {'Serendale_JewelToken': -500000000000000000000, 'ONE': 1015349184940900931570}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0xc08d796dab3bd6ca8ca550267c1175540ec41a4bb327292d0dc553a9d2b2bf44', 'timestamp': '2021/08/22, 22:21:10', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00123576, 'TxTokens': {'Serendale_JewelToken': -250000000000000000000, 'ONE': 521025481108775289557}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0x86aad7f99cacdeb9d9c377faab36a1c0d673995a54f80d36b9d5534fd5798838', 'timestamp': '2021/08/22, 22:36:42', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00123576, 'TxTokens': {'Serendale_JewelToken': -1000000000000000000000, 'ONE': 1720131379450908485848}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0xcff29a319a31b12c73c4d5b2d8c3a27b21196f66997438b86e8c364b9ef8fa49', 'timestamp': '2021/08/22, 22:40:47', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00135736, 'TxTokens': {'Serendale_JewelToken': -1000000000000000000000, 'ONE': 1819302554033104267224}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0x5416461b47de3077b70db01c3b33d692f3225689556ed6c2cce32cc1a5a160ac', 'timestamp': '2021/08/22, 22:44:01', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00123576, 'TxTokens': {'Serendale_JewelToken': -500000000000000000000, 'ONE': 971600100924408795098}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0x4d88cc1f42e09f4f4b5af06a2f5b06c6d2c29e51455caf516c735b9a6ac449b6', 'timestamp': '2021/08/22, 22:45:54', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.0013576, 'TxTokens': {'Serendale_JewelToken': -5000000000000000000000, 'ONE': 10035723813504311645975}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0xb3fc0d59145e63b1ecd8c403347e7efecee9de310cded04000448a3ccee18825', 'timestamp': '2021/08/22, 22:48:53', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00135736, 'TxTokens': {'Serendale_JewelToken': -500000000000000000000, 'ONE': 995695770931703469714}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0x78fcc3d20128f697ca2e179975a1d12b282fbb81e11fc3b531f91a5ab9c86dee', 'timestamp': '2021/08/22, 23:03:09', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00134827, 'TxTokens': {'Serendale_JewelToken': -1000000000000000000000, 'ONE': 2045762870250171677691}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0x20101d9c92f22ed4de25412e72c82dd6f497055a19a90b928fef49488075d9b1', 'timestamp': '2021/08/22, 23:05:12', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00134827, 'TxTokens': {'Serendale_JewelToken': -2000000000000000000000, 'ONE': 4145259055287125009163}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0xa33c68a34a21fc5196f688fe31e392bfbc5fd1ac5b979a64edf8a14e839c537c', 'timestamp': '2021/08/22, 23:12:11', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00134851, 'TxTokens': {'Serendale_JewelToken': -5783800000000000000000, 'ONE': 11806972106774775949345}},
            {'function': 'addLiquidityETH', 'status': 1, 'TxHash': '0x2ec82c4f74e54d302d3b3da67750bf99ed76f928b9edfbb34b73b28b90c779e4', 'timestamp': '2021/08/22, 23:43:07', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 205.09484417166732, 'TxFee': 0.00181036, 'TxTokens': {'Serendale_JewelToken': -100000000000000000000, 'Jewel LP Token (JEWEL-LP)': 141768810699638944995, 'ONE': -205.09484417166732}},
            {'function': 'deposit', 'status': 1, 'TxHash': '0xe0f7fb44f9661775e80d31adb1d85ee5400339fce3ffbee221a7342f994bf7f6', 'timestamp': '2021/08/22, 23:43:43', 'to': '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_MasterGardener', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.0046178, 'TxTokens': {'Serendale_JewelToken': 1174643787758260800, 'Jewel LP Token (JEWEL-LP)': -141768810699638944995}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0x0213ac1cf6285791abfde0f557802db7add105e78485e52d1c606e138f0c446e', 'timestamp': '2021/08/22, 23:44:56', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00134851, 'TxTokens': {'Serendale_JewelToken': -6000000000000000000000, 'ONE': 12168875358176380701756}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0x05476fd04ce03528b863afbf5ca7331bbce8b709da9d6e214202b841dbf12c16', 'timestamp': '2021/08/23, 07:17:24', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00134827, 'TxTokens': {'Serendale_JewelToken': -1000000000000000000000, 'ONE': 2796057019280209278608}},
            {'function': 'addLiquidityETH', 'status': 1, 'TxHash': '0x515d258597e58deae35c5c1801418868ed8565f6df919394232646a203b432d9', 'timestamp': '2021/08/23, 07:23:46', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 279.09744871102237, 'TxFee': 0.00181254, 'TxTokens': {'Serendale_JewelToken': -100000000000000000000, 'Jewel LP Token (JEWEL-LP)': 165252096623359801044, 'ONE': -279.09744871102237}},
            {'function': 'deposit', 'status': 1, 'TxHash': '0x8abe766f50f09a67646638b9a3aa0ba90b811f35f421912ca03373b1a8884b3d', 'timestamp': '2021/08/23, 07:24:08', 'to': '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_MasterGardener', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00410887, 'TxTokens': {'Serendale_JewelToken': 12365143182050225410, 'Jewel LP Token (JEWEL-LP)': -165252096623359801044}},
            {'function': 'swapETHForExactTokens', 'status': 1, 'TxHash': '0x5b4ed14bc09a65a9a6be0e81a884cc530c511955c1dd8d5f17df3f7b7dde9469', 'timestamp': '2021/08/23, 09:33:16', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 456.00048865173306, 'TxFee': 0.00123595, 'TxTokens': {'Serendale_JewelToken': 200000000000000000000, 'ONE': -456.00048865173306}},
            {'function': 'addLiquidityETH', 'status': 1, 'TxHash': '0x38b9ba62e95f9e7147255a0fa46ac4da99bf53d521b96b68efbd91ac5b588b38', 'timestamp': '2021/08/23, 11:38:26', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 1548.8928986231685, 'TxFee': 0.00181266, 'TxTokens': {'Serendale_JewelToken': -1000000000000000000000, 'Jewel LP Token (JEWEL-LP)': 1230030811429437248148, 'ONE': -1548.8928986231685}},
            {'function': 'deposit', 'status': 1, 'TxHash': '0xd24411f0d67ce69ea8074a4f4749993161e9da22dafa6af329b8c9346008652b', 'timestamp': '2021/08/23, 11:39:15', 'to': '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_MasterGardener', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00410887, 'TxTokens': {'Serendale_JewelToken': 11409393967737883573, 'Jewel LP Token (JEWEL-LP)': -1230030811429437248148}},
            {'function': 'swapExactETHForTokens', 'status': 1, 'TxHash': '0xc1a6fb74d73e9414d74eb071fa1574b0850404ae5b9534efb966f9e81e1bae6f', 'timestamp': '2021/08/23, 14:18:33', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 500.0, 'TxFee': 0.00103444, 'TxTokens': {'Serendale_JewelToken': 320194293290631111036, 'ONE': -500.0}},
            {'function': 'claimReward', 'status': 1, 'TxHash': '0x5cba1b13b6509f4667174c6ce40f34a0093812e437d2f3dbbbcea6699b0a09e1', 'timestamp': '2021/08/23, 14:20:31', 'to': '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_MasterGardener', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.0035646000000000002, 'TxTokens': {'Serendale_JewelToken': 30199191420386537002}},
            {'function': 'claimReward', 'status': 1, 'TxHash': '0x003e71f38bad90b80fd9512570e478672eba6af632ce5968f7f070780b215a72', 'timestamp': '2021/08/23, 14:20:39', 'to': '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_MasterGardener', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.0035646000000000002, 'TxTokens': {'Serendale_JewelToken': 20824514654463823}},
            {'function': 'swapExactETHForTokens', 'status': 1, 'TxHash': '0x7f5132bc6ac76d255bd9df7ac68fe9d8efbc6fe7c29342ef1b95968bc32245b4', 'timestamp': '2021/08/23, 17:37:58', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 200.0, 'TxFee': 0.00115604, 'TxTokens': {'Serendale_JewelToken': 127266381771135523311, 'ONE': -200.0}},
            {'function': 'addLiquidityETH', 'status': 1, 'TxHash': '0xeac90b4a8a7975396b466ec44893ad375333bca1cb94d6421a18f3123c186b96', 'timestamp': '2021/08/23, 17:41:11', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 15.670332757096302, 'TxFee': 0.00199929, 'TxTokens': {'Serendale_JewelToken': -10000000000000000000, 'Jewel LP Token (JEWEL-LP)': 12364456159545597149, 'ONE': -15.670332757096302}},
            {'function': 'deposit', 'status': 1, 'TxHash': '0x9c77994a608e195b5af0caab44eeb7f0f790f7d4c0414418b6711349fea9de17', 'timestamp': '2021/08/23, 17:42:20', 'to': '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_MasterGardener', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00410875, 'TxTokens': {'Serendale_JewelToken': 34284227966222908476, 'Jewel LP Token (JEWEL-LP)': -12364456159545597149}},
            {'function': 'claimReward', 'status': 1, 'TxHash': '0xaaab9de86d6c7305cde69853a43b1db8cb94b1e0567c7d26081fefdfdc9f10e9', 'timestamp': '2021/08/23, 20:33:16', 'to': '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_MasterGardener', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.0035646000000000002, 'TxTokens': {'Serendale_JewelToken': 30671930928876207352}},
            {'function': 'claimReward', 'status': 1, 'TxHash': '0xa1802ce14f8ff8650512555b8e74726c17eeb501bd5a7a8295a9ff5de4c479d6', 'timestamp': '2021/08/24, 09:40:41', 'to': '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_MasterGardener', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.0035646000000000002, 'TxTokens': {'Serendale_JewelToken': 130964733379131796392}},
            {'function': 'addLiquidityETH', 'status': 1, 'TxHash': '0x6e18eef2a1529d4b42c740191f2a969b6231dc0a3f14858d6890fe50571f0345', 'timestamp': '2021/08/24, 10:32:15', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 844.0472834766838, 'TxFee': 0.00181266, 'TxTokens': {'Serendale_JewelToken': -500000000000000000000, 'Jewel LP Token (JEWEL-LP)': 641268873721622814789, 'ONE': -844.0472834766838}},
            {'function': 'deposit', 'status': 1, 'TxHash': '0xb689f2bfcc52bc9352a0d5efca3a83e5f6c25b30bc2b0edd5f1f2be34c99358b', 'timestamp': '2021/08/24, 10:32:50', 'to': '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_MasterGardener', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00410887, 'TxTokens': {'Serendale_JewelToken': 7586264744926876475, 'Jewel LP Token (JEWEL-LP)': -641268873721622814789}},
            {'function': 'claimReward', 'status': 1, 'TxHash': '0x362b1a89878c3af1ec264b24c820fabf90a22d1d3e3c60318dc7e0aec5cdcbe7', 'timestamp': '2021/08/24, 22:22:51', 'to': '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_MasterGardener', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.0035646000000000002, 'TxTokens': {'Serendale_JewelToken': 141419779032898227366}},
            {'function': 'swapExactTokensForETH', 'status': 1, 'TxHash': '0xf514db8a26f470869f4555cda89ebcb56e1acdeeea43c2eb2fa2eaaae1de025c', 'timestamp': '2021/08/24, 22:27:17', 'to': '0x24ad62502d1C652Cc7684081169D04896aC20f30', 'from': '0xD83d5EBBE238aEfB7802506aC8386882b5CC8186', 'to_mapped': 'Serendale_UniswapV2Router02', 'from_mapped': 'USER', 'value': 0.0, 'TxFee': 0.00134827, 'TxTokens': {'Serendale_JewelToken': -1000000000000000000000, 'ONE': 2104022881041779429054}}
        ]

        # TODO: Add logic to find the total page numbers from the DB
        current_page = int(request.GET["page"])
        total_pages = ceil(len(transactions) / TRANSACTIONS_PER_PAGE)
        pagination_presenter = TransactionPaginator(total_pages, current_page)
        
        start = (current_page - 1) * TRANSACTIONS_PER_PAGE
        presenters = [TransactionPresenter(transactions[i]) for i in range(start, start + TRANSACTIONS_PER_PAGE)]

        return render(request, "transactions/get.html", {"transactions": presenters, "paginator": pagination_presenter})
