# Paper Trading Setup

Փորձարկիր թրեյդինգը **առանց իրական փող կորցնելու**։ Իրական շուկայի գներով, fake փողով։

## Ինչու սկսել սրանով

- Day trader-ների 70-90%-ը կորցնում է փողը (SEC, ESMA վիճակագրություն)
- Մինչև իրական փող դնելը, պետք է 3-6 ամիս paper trading անել
- Եթե paper-ով չես կարող կայուն շահել, real-ով էլ չես կարող

## Setup

```bash
pip install -r requirements.txt
```

## 1. Paper Trader (իրական գներ, fake փող)

Սկսում ես $1000-ով։ Գները իրականն են yfinance-ից։

```bash
python paper_trader.py status                  # նայել portfolio
python paper_trader.py buy AAPL 2              # գնել 2 share Apple
python paper_trader.py sell AAPL 1             # վաճառել 1 share
python paper_trader.py reset                   # reset $1000-ի
```

State-ը պահվում է `portfolio.json`-ում։

## 2. Backtest (պատմական տվյալներով փորձարկում)

Փորձարկիր ստրատեգիան անցյալի վրա, մինչև իրականում օգտագործել։

```bash
python backtest.py --symbol SPY --period 2y --fast 20 --slow 50 --capital 1000
```

Կտեսնես՝ ստրատեգիան շահեց՞, թե պարզ "գնել ու պահել"-ից վատ էր։ **Հաճախ վատ է** — դա կարևոր դաս է։

## 3. Risk Calculator (քանի՞ share գնել)

Պրոֆեսիոնալները **1 գործարքից 1-2%-ից ավել չեն ռիսկ անում**։

```bash
python risk.py --account 1000 --risk 1 --entry 150 --stop 145
```

Կասի՝ քանի share գնել, որ եթե stop-loss-ը գործի, $10-ից ավել չկորցնես։

## Հաջորդ քայլերը

1. **2-4 շաբաթ** paper trading՝ ամեն օր ստուգիր `status`
2. Փորձիր մի քանի ստրատեգիա backtest-ով
3. Գրիր օրագիր՝ ինչու բացեցիր ամեն trade-ը (emotion vs. logic)
4. Միայն եթե 3+ ամիս դրական ես paper-ով՝ մտածիր real փողի մասին
5. Իրական փողով սկսիր **այնքանով, որքան պատրաստ ես ամբողջությամբ կորցնել**

## Կարևոր

Այս setup-ը **սովորելու գործիք է**, ոչ թե եկամտի աղբյուր։ Ոչ ոք չի կարող երաշխավորել օրեկան շահ։
