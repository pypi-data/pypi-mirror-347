import requests

from argparse import Namespace
from datetime import datetime, timedelta
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
from prometheus_client.registry import Collector

from technitium_exporter.lookups import RECORD_TYPES, COMMON_RECORD_TYPES, PROTOCOL_TYPES, HELP_FOR_STATS
from technitium_exporter.constants import CAMEL_CASE


class TechnitiumCollector(Collector):
    def __init__(self, args: Namespace):
        self._args = args
        super().__init__()

    def collect_top_clients(self, stats: dict):
        fam = GaugeMetricFamily("technitium_top_clients", "Top 10 clients by number of requests",
                                labels=["rank", "name", "domain", "rateLimited"])
        for rank, top in enumerate(stats["topClients"], start=1):
            fam.add_metric([str(rank), top["name"], top.get("domain", "None"), str(top["rateLimited"])], top["hits"])
        yield fam

    def collect_top_domains(self, stats: dict):
        fam = GaugeMetricFamily("technitium_top_domains", "Top 10 domains requested for lookup",
                                labels=["rank", "name"])
        for rank, top in enumerate(stats["topDomains"], start=1):
            fam.add_metric([str(rank), top["name"]], top["hits"])
        yield fam

    def collect_top_blocked(self, stats: dict):
        fam = GaugeMetricFamily("technitium_top_blocked", "Top 10 blocked domains",
                                labels=["rank", "name"])
        for rank, top in enumerate(stats["topBlockedDomains"], start=1):
            fam.add_metric([str(rank), top["name"]], top["hits"])
        yield fam

    def collect_update_check(self):
        response = requests.get(f"{self._args.url}/api/user/checkForUpdate", params={"token": self._args.token})
        response.raise_for_status()
        json = response.json()
        assert json["status"] == "ok", "Server returned invalid status for update check"
        yield GaugeMetricFamily("technitium_update_available", "Returns 1 if there is a newer version of Technitium",
                                1 if json["response"]["updateAvailable"] else 0)

    def get_stats(self):
        now = datetime.now().isoformat()
        then = (datetime.now() - timedelta(minutes=1)).isoformat()
        response = requests.get(f"{self._args.url}/api/dashboard/stats/get",
                                params={"token": self._args.token, "type": "custom", "start": then, "end": now})
        response.raise_for_status()
        json = response.json()
        assert json["status"] == "ok", "Server returned invalid status for stats request"
        return json["response"]

    def collect_general_stats(self, stats: dict):
        for key, val in stats["stats"].items():
            name = "technitium_stats_" + CAMEL_CASE.sub("_", key).lower()
            desc = HELP_FOR_STATS[name]
            if key.startswith("total"):
                name = name.replace("_total", "")
                yield CounterMetricFamily(name, desc, val)
            else:
                yield GaugeMetricFamily(name, desc, val)

    def collect_stats_by_record_type(self, stats: dict):
        data = stats["queryTypeChartData"]
        fam = GaugeMetricFamily("technitium_record_type_count",
                                "Number of responses by record type", labels=["record_type", "desc"])
        by_type = dict()
        for record_type, count in zip(data["labels"], data["datasets"][0]["data"]):
            by_type[record_type] = count
        for record_type, help in RECORD_TYPES.items():
            if self._args.all_record_types or record_type in COMMON_RECORD_TYPES:
                fam.add_metric([record_type, help], by_type.get(record_type, 0))
        yield fam

    def collect_stats_by_protocol_type(self, stats: dict):
        data = stats["protocolTypeChartData"]
        fam = GaugeMetricFamily("technitium_protocol_type_count", "Number of requests by protocol", labels=["protocol"])
        by_proto = dict()
        for proto, count in zip(data["labels"], data["datasets"][0]["data"]):
            by_proto[proto.lower()] = count
        for proto in PROTOCOL_TYPES:
            fam.add_metric([proto], by_proto.get(proto, 0))
        yield fam

    def collect_request_stats(self, stats: dict):
        fam1 = GaugeMetricFamily("technitium_dns_request_result_count",
                                 "Number of requests with the given result", labels=["result"])
        fam2 = GaugeMetricFamily("technitium_dns_resolve_mode_count",
                                 "Number of requests resolved in a given mode", labels=["result"])
        fam3 = GaugeMetricFamily("technitium_dns_clients_connected", "Number of clients sending requests")
        for dataset in stats["mainChartData"]["datasets"]:
            name = dataset["label"].lower().replace(" ", "_")
            if name in ("total", "no_error", "server_failure", "nx_domain", "refused"):
                fam1.add_metric([name], dataset["data"][-1])
            elif name == "clients":
                fam3.add_metric([], dataset["data"][-1])
            else:
                fam2.add_metric([name], dataset["data"][-1])
        yield fam1
        yield fam2

    def collect(self):
        stats = self.get_stats()

        yield from self.collect_update_check()
        yield from self.collect_general_stats(stats)
        yield from self.collect_top_clients(stats)
        yield from self.collect_top_domains(stats)
        yield from self.collect_top_blocked(stats)
        yield from self.collect_request_stats(stats)
        yield from self.collect_stats_by_record_type(stats)
        yield from self.collect_stats_by_protocol_type(stats)
