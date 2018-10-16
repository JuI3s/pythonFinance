import urllib2
from BeautifulSoup import BeautifulSoup

url = 'https://finance.yahoo.com/quote/^GSPC/options?p=%5EGSPC&date=1552608000'
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)

results = soup.findAll('tbody')

print(results)

# Results are BeautifulSoup tags


# calls = results[0]
# puts = results[1]

# callStrike = []
# callLastPrice = []
# callBid = []
# callAsk = []
# callExpiration = []
# callInTheMoney = []
# callErrors = []

# putStrike = []
# putLastPrice = [] 
# putBid = []
# putAsk = []
# putExpiration = [] 
# putInTheMoney = []
# putErrors = []

# for option in calls:
# 	attr = option.findAll('td')
# 	callStrike.append(attr[2])
# 	callLastPrice.append(attr[3])
# 	callBid.append(attr[4])
# 	callAsk.append(attr[5])

# for option in puts:
# 	attr = option.findAll('td')
# 	putStrike.append(attr[2])
# 	putLastPrice.append(attr[3])
# 	putBid.append(attr[4])
# 	putAsk.append(attr[5])




# Example tag format for each option
# <td class="data-col0 Ta(start) Pstart(10px)" data-reactid="60"><a class="Fz(s) Ell C($c-fuji-blue-1-b)" href="/quote/SPX181221C00100000?p=SPX181221C00100000" title="SPX181221C00100000" data-reactid="61">SPX181221C00100000</a></td>
# <td class="data-col1 Ta(end) Pstart(7px)" data-reactid="62">2018-10-11 10:21AM EDT</td>
# <td class="data-col2 Ta(end) Pstart(7px)" data-reactid="63"><a href="/quote/^GSPC/options?strike=false&amp;straddle=false" data-symbol="^GSPC" data-reactid="64">100.00</a></td>
# <td class="data-col3 Ta(end) Pstart(7px)" data-reactid="65">2,670.26</td>
# <td class="data-col4 Ta(end) Pstart(7px)" data-reactid="66">2,649.20</td>
# <td class="data-col5 Ta(end) Pstart(7px)" data-reactid="67">2,653.80</td>
# <td class="data-col6 Ta(end) Pstart(7px)" data-reactid="68"><span class="Trsdu(0.3s)  C($dataRed)" data-reactid="69">-73.31</span></td>
# <td class="data-col7 Ta(end) Pstart(7px)" data-reactid="70"><span class="Trsdu(0.3s)  C($dataRed)" data-reactid="71">-2.82%</span></td>
# <td class="data-col8 Ta(end) Pstart(7px)" data-reactid="72">6</td>
# <td class="data-col9 Ta(end) Pstart(7px)" data-reactid="73">3,520</td>
# <td class="data-col10 Ta(end) Pstart(7px) Pend(6px)" data-reactid="74">0.00%</td>