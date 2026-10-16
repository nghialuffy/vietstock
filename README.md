# vietstock

Thư viện Python phía client để kết nối, chuẩn hoá và phân tích dữ liệu thị trường
chứng khoán Việt Nam.

> `vietstock` là một package độc lập. Nó không phải bản phân phối, bản kế thừa hay
> bản thay thế của bất kỳ package nào khác.

## Tính năng

| Nhóm | Nội dung |
| --- | --- |
| Giao diện Hợp nhất (Unified UI) | `Reference`, `Market`, `Fundamental`, `Retail`, `Broker` |
| Lớp API adapter | `Quote`, `Listing`, `Company`, `Finance`, `Trading`, `Fund` |
| Nguồn dữ liệu | VCI, KBS, MSN, FMarket, cùng nguồn giá vàng và tỷ giá |
| Connector | DNSE (giao dịch), FMP (chứng khoán quốc tế) |
| Tiện ích lõi | chuẩn hoá trường dữ liệu, retry với exponential backoff, phát hiện CDN/WAF block, circuit breaker theo host |

## Cài đặt

```bash
pip install vietstock
```

Cài từ mã nguồn:

```bash
git clone <repo-url> && cd vietstock
pip install -e .
```

Yêu cầu **Python >= 3.10**.

## Biểu đồ (tuỳ chọn)

`vietstock` không kèm thư viện vẽ biểu đồ. Cài thêm một backend rồi thư viện tự phát
hiện khi bạn dùng `Chart`:

- `vnstock_ezchart` — backend cơ bản.
- `vnstock_chart` — backend đầy đủ hơn.

Lưu ý: `vnstock_ezchart` khai báo phụ thuộc vào package `vnstock`, mà package đó
không có trên PyPI, nên cần cài từ nguồn phân phối riêng của nó. Nếu không cài
backend nào, mọi chức năng truy xuất dữ liệu vẫn hoạt động bình thường.

## Bắt đầu nhanh

```python
from vietstock import Market, Reference, Fundamental

market = Market()
ref = Reference()
fa = Fundamental()

# Giá lịch sử (OHLCV)
df_history = market.equity().ohlcv(symbol="VNM", start="2024-01-01", end="2024-05-01")

# Hồ sơ doanh nghiệp
df_profile = ref.company(symbol="FPT").info()

# Báo cáo tài chính
df_balance = fa.equity(symbol="TCB").balance_sheet(period="year")
```

Mỗi nhóm dữ liệu là một đối tượng gọi được, nhận `symbol` rồi trả về các phương thức
con. Ví dụ `market.equity()` cho `ohlcv`, `quote`, `trades`; `fa.equity("TCB")` cho
`balance_sheet`, `income_statement`, `cash_flow`, `ratio`.

## Các nhóm dữ liệu

Thư viện trích xuất dữ liệu từ các nguồn công bố bên thứ ba theo 6 nhóm chức năng.
Phạm vi dữ liệu phụ thuộc vào từng nguồn và có thể thay đổi.

1. **Cổ phiếu (Equity):** giá trong phiên, lịch sử giá, báo cáo tài chính, hồ sơ doanh nghiệp.
2. **Chỉ số thị trường (Index):** biến động lịch sử VNINDEX, HNX, UPCOM và các chỉ số ngành.
3. **Chứng quyền (Warrant):** thông tin chứng quyền, thị giá, ngày đáo hạn.
4. **Phái sinh (Futures):** hợp đồng tương lai chỉ số VN30 và các kỳ hạn tương ứng.
5. **Quỹ đầu tư (Fund & ETF):** danh mục, hiệu suất quỹ mở và quỹ hoán đổi danh mục.
6. **Vĩ mô & Hàng hoá (Macro & Commodities):** tỷ giá ngoại tệ, giá vàng, tiền mã hoá.

## Cấu trúc API

Gọi `show_api()` để in toàn bộ cây API:

```python
from vietstock import show_api

show_api()
```

```text

API STRUCTURE TREE - VIETSTOCK (Unified UI)
vietstock
├── Reference
│   ├── company # Access company-specific reference data.
│   │   ├── info() [KBS] -> DataFrame # Get company overview.
│   │   ├── shareholders() [KBS] -> DataFrame # List major shareholders.
│   │   ├── officers() [KBS] -> DataFrame # List company leadership.
│   │   ├── subsidiaries() [KBS] -> DataFrame # List subsidiaries.
│   │   ├── ownership() [KBS] -> DataFrame # Company ownership structure.
│   │   ├── insider_trading() [KBS] -> DataFrame # Insider trading history.
│   │   ├── capital_history() [KBS] -> DataFrame # Capital change history.
│   │   ├── news() [KBS] -> DataFrame # Company related news.
│   │   └── events() [KBS] -> DataFrame # Upcoming corporate events.
│   ├── equity # Equity symbols and grouping reference.
│   │   ├── list() [KBS] -> DataFrame # List all equity symbols.
│   │   ├── list_by_group() [KBS] -> Series # List equities by group.
│   │   ├── list_by_industry() [VCI] -> DataFrame # List equities by industry.
│   │   └── list_by_exchange() [KBS] -> DataFrame # List symbols by exchange/board.
│   ├── index # Market index reference data.
│   │   ├── list() [KBS] -> DataFrame # List all market indices.
│   │   ├── members() [KBS] -> Series # List constituents of an index.
│   │   └── groups() [KBS] -> DataFrame # List supported index groups.
│   ├── etf # ETF reference data.
│   │   └── list() [KBS] -> Series # List all trackers/ETFs.
│   ├── futures # Access index futures reference data.
│   │   └── list() [KBS] -> Series # List all futures instruments.
│   ├── warrant # Access covered warrant reference data.
│   │   └── list() [KBS] -> Series # List all covered warrants.
│   ├── bond # Bond/Debt reference data.
│   │   └── list() [Unified] -> DataFrame # List all debt/bonds.
│   ├── fund # Mutual fund reference data.
│   │   ├── list() [FMarket] -> DataFrame # List all mutual funds.
│   │   ├── top_holding() [FMarket] -> DataFrame # Fund top holdings.
│   │   ├── industry_holding() [FMarket] -> DataFrame # Fund industry allocation.
│   │   ├── nav_report() [FMarket] -> DataFrame # Fund NAV performance.
│   │   └── asset_holding() [FMarket] -> DataFrame # Fund asset allocation.
│   ├── industry # Industry classification reference.
│   │   ├── list() [VCI] -> DataFrame # ICB industry classification.
│   │   └── sectors() [KBS] -> DataFrame # List symbols grouped by industry.
│   ├── market # Market status and metadata.
│   │   └── status() [VCI] -> DataFrame # Get live market status.
│   └── search # Search functionality.
│       ├── symbol() [MSN] -> DataFrame # Search for symbols globally.
│       └── info() [MSN] -> DataFrame # Search for detailed asset information.
├── Market
│   ├── quote() [KBS] -> DataFrame # Global in-session quote (source-delayed).
│   ├── equity # Access equity market data.
│   │   ├── ohlcv() [KBS] -> DataFrame # Historical OHLCV bars.
│   │   ├── quote() [KBS] -> DataFrame # In-session pricing board data (source-delayed).
│   │   └── trades() [KBS] -> DataFrame # Tick-by-tick trade tape.
│   ├── index # Access index market data.
│   │   └── ohlcv() [KBS] -> DataFrame # Historical OHLCV bars for indices.
│   ├── etf # Access ETF market data.
│   │   ├── ohlcv() [KBS] -> DataFrame # Historical OHLCV bars for ETFs.
│   │   ├── quote() [KBS] -> DataFrame # In-session pricing for ETFs (source-delayed).
│   │   └── trades() [KBS] -> DataFrame # Tick-by-tick trades for ETFs.
│   ├── futures # Access futures market data.
│   │   ├── ohlcv() [KBS] -> DataFrame # Historical OHLCV bars for Futures.
│   │   ├── quote() [KBS] -> DataFrame # In-session pricing for Futures (source-delayed).
│   │   └── trades() [KBS] -> DataFrame # Tick-by-tick trades for Futures.
│   ├── warrant # Access warrant market data.
│   │   ├── ohlcv() [KBS] -> DataFrame # Historical OHLCV bars for Warrants.
│   │   ├── quote() [KBS] -> DataFrame # In-session pricing for Warrants (source-delayed).
│   │   └── trades() [KBS] -> DataFrame # Tick-by-tick trades for Warrants.
│   ├── forex # Access forex market data.
│   │   └── ohlcv() [MSN] -> DataFrame # Historical OHLCV bars for forex.
│   ├── fund # Access Mutual Fund market data.
│   │   ├── history() [FMarket] -> DataFrame # Fund NAV history.
│   │   ├── nav() [FMarket] -> DataFrame # Fund NAV history.
│   │   ├── top_holding() [FMarket] -> DataFrame # Top holdings of the fund.
│   │   ├── industry_holding() [FMarket] -> DataFrame # Industry allocation of the fund.
│   │   └── asset_holding() [FMarket] -> DataFrame # Asset class allocation of the fund.
│   ├── commodity # Access commodity market data.
│   │   └── ohlcv() [MSN] -> DataFrame # Historical OHLCV for commodities.
│   └── crypto # Access crypto market data.
│       └── ohlcv() [MSN] -> DataFrame # Historical OHLCV for crypto.
├── Fundamental
│   └── equity # Access equity fundamental data.
│       ├── balance_sheet() [KBS] -> DataFrame # Get balance sheet.
│       ├── cash_flow() [KBS] -> DataFrame # Get cash flow.
│       ├── income_statement() [KBS] -> DataFrame # Get income statement.
│       └── ratio() [KBS] -> DataFrame # Financial ratios.
├── Retail
│   ├── gold() [SJC/BTMC] -> DataFrame # Unified gold price (use source='sjc' or 'btmc').
│   └── exchange_rate() [VCB] -> DataFrame # Get exchange rate from Vietcombank.
└── Broker
    └── dnse # DNSE Brokerage integration.
        ├── login() [DNSE] -> str # Login to account.
        ├── account() [DNSE] -> DataFrame # Generic account info.
        ├── sub_accounts() [DNSE] -> DataFrame # List sub-accounts.
        ├── account_balance() [DNSE] -> DataFrame # Sub-account balance.
        ├── order_list() [DNSE] -> DataFrame # Order history.
        ├── order_detail() [DNSE] -> DataFrame # Order details.
        ├── place_order() [DNSE] -> DataFrame # Place new order.
        ├── cancel_order() [DNSE] -> DataFrame # Cancel order.
        ├── trade_capacities() [DNSE] -> DataFrame # Buying power.
        ├── deals_list() [DNSE] -> DataFrame # Open deals.
        ├── loan_packages() [DNSE] -> DataFrame # Loan packages.
        ├── email_otp() [DNSE] -> None # Request OTP.
        └── get_trading_token() [DNSE] -> str # Trading token.
```

## Nguồn dữ liệu

| Nguồn | Dùng cho |
| --- | --- |
| VCI | Lịch sử giá, khớp lệnh, báo cáo tài chính, hồ sơ doanh nghiệp |
| KBS | Danh sách mã, chỉ số, hồ sơ doanh nghiệp, báo cáo tài chính |
| MSN | Giá và danh sách mã theo `SecId` |
| FMarket | Danh mục và hiệu suất quỹ mở |
| SJC / tỷ giá | Giá vàng và tỷ giá ngoại tệ |

Một số nguồn có thể chặn địa chỉ IP từ hạ tầng cloud. Khi gặp lỗi kết nối, thử đổi
`source=` sang nguồn khác.

## Phát triển

```bash
pip install -e ".[dev]"
ruff check .
pytest tests/
```

## Giấy phép

Chưa công bố.
