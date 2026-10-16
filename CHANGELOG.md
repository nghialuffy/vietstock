# Changelog

All notable changes to the `vietstock` project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Explorer TCBS: `Listing(source="tcbs").research_reports()` lấy báo cáo phân tích
  (ngày công bố, loại báo cáo, mã, hashtag, link PDF), hỗ trợ phân trang, lấy toàn bộ
  và lọc theo tiêu chí của trang.
- Giao diện Hợp nhất: `Reference().reports.list()`.
- Tiện ích lõi: `send_request_text()` cho endpoint trả về HTML thay vì JSON.
- Bổ sung `DataSource.TCBS`, khôi phục khả năng import của `vietstock.core.constants`.

### Changed

- Tiện ích lõi: HTTP client chuyển sang `curl_cffi` với fingerprint Chrome
  (`impersonate="chrome"`) thay cho `requests`, để vượt qua chặn Cloudflare theo
  TLS/HTTP2 fingerprint. Thêm dependency `curl-cffi`.
- Explorer VCI: handshake priceboard của `Finance` dùng chung session đó thay vì
  `requests.Session()` riêng.

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
