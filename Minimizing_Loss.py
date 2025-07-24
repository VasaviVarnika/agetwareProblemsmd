def minimize(prices):
    n=len(prices)
    minimumLoss=float('inf')
    buyYear=-1
    sellYear=-1
    indexed_prices=[(prices[i],i) for i in range(n)]
    sorted_IP=sorted(indexed_prices)
    
    for i in range(len(sorted_IP)-1):
        currSellPrice,currSellidx=sorted_IP[i]
        currBuyPrice,currBuyidx=sorted_IP[i+1]
        if currBuyidx<currSellidx:
            loss=currBuyPrice-currSellPrice
            if loss<minimumLoss:
                minimumLoss=loss
                buyYear=currBuyidx+1
                sellYear=currSellidx+1
    return minimumLoss,buyYear,sellYear
prices=[20,15,7,2,13]
minimumLoss,buyYear,sellYear=minimize(prices)
print(f"minLoss={minimumLoss}, buyYear:{buyYear},sellYear: {sellYear}")
