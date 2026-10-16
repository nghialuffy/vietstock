# Changelog

All notable changes to the `vietstock` project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]

Bản phát hành đầu tiên.

### Added

- Giao diện Hợp nhất (Unified UI): `Reference`, `Market`, `Fundamental`, `Retail`,
  `Broker`.
- Lớp API adapter: `Quote`, `Listing`, `Company`, `Finance`, `Trading`, `Fund`.
- Explorer cho các nguồn dữ liệu VCI, KBS, MSN, FMarket, cùng nguồn giá vàng và
  tỷ giá.
- Connector DNSE (giao dịch) và FMP (chứng khoán quốc tế).
- Tiện ích lõi: chuẩn hoá trường dữ liệu, chính sách retry với exponential backoff,
  phát hiện CDN/WAF block và circuit breaker theo host.
