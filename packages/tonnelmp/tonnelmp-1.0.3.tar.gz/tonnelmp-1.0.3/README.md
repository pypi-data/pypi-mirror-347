# ***Tonnel Marketplace API***

This is a simple module that will help you interacting with Tonnel Marketplace API. Tested almost every API myself so you dont have to blindly test it.

## Installing

```python
pip install tonnelmp
```

## Where to get Auth Data

You can do it pretty simply. Go to [market.tonnel.network](https://market.tonnel.network/), login to your account, then open browser console (ctrl + shift + c on windows)
navigate to Application tab -> Storage -> Local Storage -> https://market.tonnel.network/ -> web-initData -> copy the value next to it

## Some returns examples:

#### Gift example:

```python
from tonnelmp import getGifts
print(getGifts(gift_name="toy bear", limit=1))
```

**Output (list object with dicts):**

```python
[
	{
	'gift_num': 35531,
	'customEmojiId': '5289634279544876303',
	'gift_id': 4840785,
	'name': 'Toy Bear',
	'model': 'Zebra (1.5%)',
	'asset': 'TON',
	'symbol': 'Rabbit (0.2%)',
	'backdrop': 'Burgundy (2%)',
	'availabilityIssued': 0,
	'availabilityTotal': 0,
	'backdropData': {},
	'message_in_channel': 0,
	'price': 12.9,
	'status': 'forsale',
	'limited': False,
	'auction': None,
	'export_at': '2025-05-28T12:25:01.000Z'
	}
]
```

gift_num - telegram gift number
customEmojiId - telegram custom emoji id
gift_id - tonnel gift id
name - gift name
model - gift model
asset - asset name
symbol - symbol name
backdrop - backdrop name
price - price in TON without 10% fee.
status - status of the gift - forsale / auction (not sure about auction sorry)
auction - either None or auction data in dict
export_at - time of when the gift has been placed for sale / auction

#### Balances example:

```python
from tonnelmp import info
print(info(authData="your_auth_data"))
```

**Output:**

```python
{
	'status': 'success',
	'balance': 123.123123123, # your ton balance
	'memo': ' ... ', # your memo
	'transferGift': False, # false = internal purchase
	'usdtBalance': 123.123123123, # your usdt balance
	'tonnelBalance': 123.123123123, # your tonnel balance
	'referrer': 123123123, # your referrer telegram id
	'photo_url': ' ... ', # your telegram pfp url
	'name': ' ... ' # your telegram name
}
```

## Gift Class

Can wrap gift dict

#### Attributes

- .gift_num
- .gift_id
- .name
- .model
- .backdrop
- .symbol
- .price
- .status
- .asset
- .auction

.. and more

#### Example

```python
from tonnelmp import Gift, getGifts()
gift = Gift(getGifts(limit=1, sort="latest")[0])
print(gift.name, gift.gift_num, gift.gift_id, gift.price)
```

**Output:**

```python
Winter Wreath 23548 4848019 9.8
```

## Functions:

#### getGifts()

```python
getGifts(gift_name: str, model: str, backdrop: str, symbol: str, gift_num: int, page: int, limit: int, sort: str, price_range: list | int, asset: str, user_auth: str) -> list
```

- Returns a list with dict objects containing gifts details.
- Available options:
  *sort (Default="price_asc"):* `"price_asc", "price_desc", "latest", "mint_time", "rarity", "gift_id_asc", "gift_id_desc"`
  *asset (Default="TON"):* `"TON", "USDT", "TONNEL"`
- limit arg maximum = 30 (as far as i know)

#### getAuctions()

```python
getAuctions(gift_name: str, model: str, backdrop: str, symbol: str, gift_num: int, page: int, limit: int, sort: str, price_range: list | int=0, asset: str, user_auth: str="") -> list
```

- Get auctions with optional filters. Doesnt require anything at all.
- Available options:
  *sort:* `"ending_soon", "latest", "highest_bid", "latest_bid"`
  *limit maximum* = 30
  *asset:* `"TON", "USDT", "TONNEL"`

#### myGifts() - requires auth

```python
myGifts(listed: bool, page: int, limit: int, user_auth: str) -> list:
```

- Returns a list with dict objects containing gifts details.
- **Required: `user_auth`**
- Available options:
  *listed (Default=True):* `True / False.` If False, will return unlisted gifts.

#### listForSale() - requires auth

```python
listForSale(gift_id: int, price: int | float, user_auth: str) -> dict
```

- List for sale a gift with known gift_id *(tonnel gift_id, **not telegram gift_num**; can be retrieved from myGifts()/getGifts())*
- Returns dict object with status. Either success or error.
- **Required: `user_auth, gift_id, price`**

#### cancelSale() - requires auth

```python
cancelSale(gift_id: int,user_auth: str) -> dict
```

- Cancel sale of the gift with known gift_id
- Returns dict object with status. Either success or error.
- **Required: `user_auth, gift_id`**

#### saleHistory() - requires auth

*idk why but this function requires auth :D you can try putting empty authData, maybe i've done something wrong*

```python
saleHistory(authData: str, page: int, limit: int, type: str, gift_name: str, model: str, backdrop: str, sort: str) -> list
```

- Returns a list with dict objects containing gifts details.
- **Required: `authData`**
- Available options:
  *sort (Default="latest"):* `"latest", "price_asc", "price_desc", "gift_id_asc", "gift_id_desc"`
  *type (Default="ALL"):* `"ALL", "SALE", "INTERNAL_SALE", "BID"`
- limit maximum = 50

#### info() - requires auth

```python
info(authData: str) -> dict
```

- Returns a dict object containing your balances, memo, referrer etc.
- **Requires: `authData`**

#### buyGift() - requires auth

```python
buyGift(gift_id: int, price: int | float, authData: str) -> dict
```

- Buy a gift with known gift_id and price in TON. // price - raw price (you dont have to multiply it by 1.1). both params can be retrieved from getGifts()
- **Requires: `gift_id, price, authData`**
- Returns dict object with status. Either success or error.

#### createAuction() - requires auth

```python
createAuction(gift_id: int, starting_bid: int | float, authData: str, duration: int) -> dict
```

- Create auction for the gift with known gift_id.
- **Requires: `gift_id, starting_bid, authData, duration`**
- Returns dict object with status. Either success or error.
- Available options:
  *duration (Default=1):* Duration in hours. Can be one of these options - `[1, 2, 3, 6, 12, 24]`

#### cancelAuction() - requires auth

```python
cancelAuction(auction_id: str, authData: str) -> dict
```

- Cancel auction with known auction_id (can be retrieved from getAuctions() or mygifts())
- **Requires: `auction_id, authData`**
- Returns dict object with status. Either success or error

## Examples

Getting gift floor for *Toy Bear* with model *Wizard*:

```python
from tonnelmp import Gift, getGifts
gift = Gift(getGifts(gift_name="toy bear", model="wizard", limit=1, sort="price_asc")[0]) 
print(gift.price) # this will print raw price (without 10% fee), remember that
```

Buying gift

```python
from tonnelmp import buyGift
myAuthData = " ... your auth data here ... "
print(buyGift(gift_id=123123, price=123.12, authData=myAuthData)) # will print status. This will buy gift NOT FOR 123.12 TON. Tonnel adds up 10%, so the final price will be 123.12 * 1.1, again, remember that.
```

Listing gift for sale

```python
from tonnelmp import listForSale
myAuthData = " ....... "
print(listForSale(gift_id=123, price=123, user_auth=myAuthData)
```

## TODO + info

currently there are at least 5 functions missing - mintGift(), returnGift(), giftGift(), payFee(), placeBid()
also willing to add multiple gift buys, creating buy orders etc.

if you use this module please send your feedback [to my telegram](https://t.me/perfectlystill)

donations (will buy some tonnel whiskey thank you):

- ton: `UQC9f1mTuu2hKuBP_0soC5RVkq2mLp8uiPBBhn69vadU7h8W`
