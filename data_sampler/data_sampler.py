from google.cloud import bigquery as bq
import json


class VoyagerDataCollector:
    def __init__(self, sample_size):
        self.sample_size = sample_size
        pass

    @classmethod
    def build_data_controller(cls, data_collector_config):
        source_format = data_collector_config["source_format"]
        if source_format == "BigQuery":
            bq_client = bq.Client()
            return VoyagerBQDataCollector(bq_client=bq_client,
                                          sample_size=data_collector_config["sample_size"])
        elif source_format == "GCS":
            # TODO
            pass
        elif source_format == "Bigtable":
            # TODO
            pass
        else:
            raise NotImplementedError("Unrecognized source data format!")

    def export_to_file(self, data, path='./', filename='voyager_data'):
        target_file = f'{path}/{filename}.json'
        with open(target_file, "w") as f:
            json.dump(data, f)


class VoyagerBQDataCollector(VoyagerDataCollector):
    def __init__(self, bq_client, sample_size):
        super().__init__(sample_size)
        self.client = bq_client

    def collect_data(self, target_table):
        # TODO:
        # - Hardcode with timestamp WHERE condition because many partitioned tables
        #   can't be queried without it.
        # - Didn't find a proper way to directly sample N rows,
        #   so hardcode with TABLESAMPLE with 1 percent row & limit N.
        query = f"""
            SELECT * FROM `{target_table}` TABLESAMPLE SYSTEM (1 PERCENT)
            WHERE TIMESTAMP_TRUNC(timestamp, DAY) = TIMESTAMP(CURRENT_DATE())
            LIMIT {self.sample_size}
        """
        query_result = self.client.query(query).to_dataframe()
        schema = list(query_result.T.index)
        content = query_result.T.to_json()
        result_json = json.dumps({
            "source_format": "BQ",
            "schema": schema,
            "content": content
        })
        return result_json


# demo
target_tables = ["moloco-rmp-infra-prod.balaan_platform_us.event_user_event"]
bq_client = bq.Client()
myDataCollector = VoyagerBQDataCollector(bq_client, sample_size=10)
datas = []
for target_table in target_tables:
    data = myDataCollector.collect_data(target_table)
    datas.append(data)
myDataCollector.export_to_file(datas)
