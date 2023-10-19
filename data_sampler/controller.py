from google.cloud import bigquery as bq
from data_collector import VoyagerDataCollector

# Not ready yet
# from scanner import VoyagerScanner
# from reporter import VoyagerReporter


class VoyagerController:
    def __init__(self, data_source_config, data_collector_config, scanner_config, reporter_config):
        self.source_format = data_source_config["source_format"]
        self.data_source_config = data_source_config
        self.data_collector = VoyagerDataCollector.build_data_controller(data_collector_config)
        # self.scanner = VoyagerScanner.build_scanner(scanner_config)
        # self.reporter = VoyagerReporter.build_reporter(reporter_config)

    @classmethod
    def build_controller(cls, data_source_config, data_collector_config, scanner_config, reporter_config):
        source_format = data_collector_config["source_format"]
        if source_format == "BigQuery":
            bq_client = bq.Client()
            return VoyagerBQController(data_source_config, data_collector_config, scanner_config, reporter_config)
        elif source_format == "GCS":
            # TODO
            pass
        elif source_format == "Bigtable":
            # TODO
            pass
        else:
            raise NotImplementedError("Unrecognized source data format!")

    def collect_data(self):
        data_paths = self.get_data_paths()
        datas = {}
        for data_path in data_paths:
            data = self.data_collector.collect_data(data_path)
            datas[data_path] = data
        return datas

    def scan_data(self, datas):
        scan_results = {}
        for uri, data in datas:
            scan_result = self.scanner.scan_data(data)
            scan_results[uri] = scan_result
        return scan_results

    def generate_report(self, scan_results):
        reports = {}
        for uri, scan_result in scan_results:
            report = self.reporter.generate_report(scan_result)
            reports[uri] = report
        return reports

    def work(self):
        datas = self.collect_data()
        scan_results = self.scan_data(datas)
        reports = self.generate_report(scan_results)
        # May need to change this, based on api of reporter
        return reports


class VoyagerBQController(VoyagerController):
    def __init__(self, data_source_config, data_collector_config, scanner_config, reporter_config):
        super().__init__(data_source_config, data_collector_config, scanner_config, reporter_config)

    def walk(self, config):
        project_id = config["project"]
        dataset_id = config["dataset"]

        table_path_prefix = f"{project_id}.{dataset_id}"

        # client = bq.Client()
        # tables = client.list_table(table_path_prefix)

        # Hardcoding here, because there is limitation in data collector that prevents
        # it from using the same query on every table.
        tables = ["event_user_event", "event_user_signal"]

        table_full_paths = []
        for table in tables:
            table_full_paths.append(f"{table_path_prefix}.{table}")
        return table_full_paths

    def get_data_paths(self):
        data_paths = []
        for config in self.data_source_config["targets"]:
            data_paths.extend(self.walk(config))
        return data_paths


my_data_source_config = {
    "source_format": "BigQuery",
    "targets": [
        {
            "project": "moloco-rmp-infra-prod",
            "dataset": "balaan_platform_us"
        },
        {
            "project": "moloco-rmp-infra-prod",
            "dataset": "bucketplace_platform_us"
        }
    ]
}

my_data_collector_config = {
    "source_format": "BigQuery",
    "sample_size": 10
}

my_controller = VoyagerBQController(my_data_source_config, my_data_collector_config, {}, {})
print(my_controller.collect_data())
