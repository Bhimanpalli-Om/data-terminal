from pydantic import BaseModel
from typing import Optional, List

class StockMeta(BaseModel):
    symbol: str
    identifier: str
    lastPrice: float
    change: float
    pChange: float
    previousClose: float
    finalQuantity: int
    totalTurnover: float
    marketCap: float
    yearHigh: float
    yearLow: float
    iep: float
    chartTodayPath: Optional[str]

class PreOpenQuote(BaseModel):
    price: float
    buyQty: int
    sellQty: int
    iep: Optional[bool] = None

class PreOpenMarket(BaseModel):
    preopen: List[PreOpenQuote]
    IEP: float
    totalTradedVolume: int
    finalPrice: float
    finalQuantity: int
    lastUpdateTime: str
    totalSellQuantity: int
    totalBuyQuantity: int
    atoBuyQty: int
    atoSellQty: int
    Change: float
    perChange: float
    prevClose: float

class StockDetail(BaseModel):
    preOpenMarket: PreOpenMarket

class StockEntry(BaseModel):
    metadata: StockMeta
    detail: StockDetail

class PreOpenData(BaseModel):
    declines: int
    unchanged: int
    data: List[StockEntry]
