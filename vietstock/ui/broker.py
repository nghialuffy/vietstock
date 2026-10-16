from __future__ import annotations


class Broker:
    """
    Brokerage Connectors.
    """

    @property
    def dnse(self):
        from vietstock.ui.domains.broker.dnse import DNSEBroker

        return DNSEBroker()
