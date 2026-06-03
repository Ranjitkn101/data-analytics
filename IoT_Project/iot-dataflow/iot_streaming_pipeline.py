import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam import window, trigger
from apache_beam.io import fileio
import json
from datetime import datetime
import uuid
import os

PROJECT_ID = os.environ.get("PROJECT_ID", "iot-device-project")
BUCKET = os.environ.get("BUCKET", "gs://landing-iot-device-bkt-east1")
TOPIC = f"projects/{PROJECT_ID}/topics/iot-events-us-east1"


class ParseAndEnrich(beam.DoFn):
    """
    This DoFn:
    - Parses raw Pub/Sub JSON
    - Builds Bronze (always)
    - Builds Silver (only if valid)
    - Builds Meta (always)
    - Applies filtering rules for Silver
    """

    def process(self, element, processing_ts=beam.DoFn.TimestampParam):
        raw = element.decode("utf-8")
        ingest_time = datetime.utcfromtimestamp(float(processing_ts))
        event_id = str(uuid.uuid4())

        try:
            # -----------------------------
            # PARSE JSON
            # -----------------------------
            data = json.loads(raw)

            # Required fields
            required = ["deviceId", "ts", "temp", "humidity"]
            if any(f not in data for f in required):
                raise ValueError("Missing required fields")

            # Parse timestamp
            ts = datetime.fromisoformat(data["ts"].replace("Z", "+00:00"))
            event_date = ts.date().isoformat()

            # Convert numeric fields
            temp = float(data["temp"])
            humidity = float(data["humidity"])

            # -----------------------------
            # BRONZE RECORD (always emitted)
            # -----------------------------
            bronze = {
                "deviceId": data["deviceId"],
                "ts": ts.isoformat(),
                "temp": temp,
                "humidity": humidity,
                "site": data.get("site", None),
                "event_date": event_date,
            }

            # -----------------------------
            # FILTERING RULES FOR SILVER
            # -----------------------------
            # Temperature realistic range
            if not (-40 <= temp <= 85):
                raise ValueError("Temperature out of range")

            # Humidity realistic range
            if not (0 <= humidity <= 100):
                raise ValueError("Humidity out of range")

            # -----------------------------
            # SILVER RECORD (only if valid)
            # -----------------------------
            silver = {
                "deviceId": data["deviceId"],
                "ts": ts.isoformat(),
                "temp_celsius": temp,
                "humidity": humidity,
                "site": data.get("site", None),
                "event_date": event_date,
                "source": "iot-events-us-east1",
                "pipeline_version": "v1",
            }

            # -----------------------------
            # META SUCCESS
            # -----------------------------
            meta = {
                "event_id": event_id,
                "device_id": data["deviceId"],
                "raw_ts": ts.isoformat(),
                "ingest_ts": ingest_time.isoformat(),
                "event_date": event_date,
                "pipeline_name": "iot_streaming_pipeline",
                "status": "SUCCESS",
                "error_message": None,
            }

        except Exception as e:
            # -----------------------------
            # META ERROR
            # -----------------------------
            meta = {
                "event_id": event_id,
                "device_id": None,
                "raw_ts": None,
                "ingest_ts": ingest_time.isoformat(),
                "event_date": ingest_time.date().isoformat(),
                "pipeline_name": "iot_streaming_pipeline",
                "status": "ERROR",
                "error_message": str(e),
            }
            bronze = None
            silver = None

        # Emit Bronze (if parsed)
        if bronze:
            yield beam.pvalue.TaggedOutput("bronze", bronze)

        # Emit Silver (only if valid)
        if silver:
            yield beam.pvalue.TaggedOutput("silver", silver)

        # Emit Meta (always)
        yield beam.pvalue.TaggedOutput("meta", meta)


def to_jsonl(rec):
    return json.dumps(rec)


def run(argv=None):
    options = PipelineOptions(save_main_session=True)
    standard_options = options.view_as(StandardOptions)
    standard_options.streaming = True

    with beam.Pipeline(options=options) as p:
        parsed = (
            p
            | "ReadPubSub" >> beam.io.ReadFromPubSub(topic=TOPIC)
            | "ParseEnrich" >> beam.ParDo(ParseAndEnrich()).with_outputs("bronze", "silver", "meta")
        )

        bronze = parsed.bronze
        silver = parsed.silver
        meta = parsed.meta

        # Windowing + Trigger
        windowing = window.FixedWindows(10)
        trig = trigger.Repeatedly(trigger.AfterProcessingTime(5))

        # -----------------------------
        # BRONZE → GCS
        # -----------------------------
        (
            bronze
            | "BronzeToJsonl" >> beam.Map(to_jsonl)
            | "WindowBronze" >> beam.WindowInto(
                windowing,
                trigger=trig,
                accumulation_mode=trigger.AccumulationMode.DISCARDING,
            )
            | "WriteBronze" >> fileio.WriteToFiles(
                path=f"{BUCKET}/bronze/",
                destination=lambda x: "bronze",
                file_naming=fileio.destination_prefix_naming(suffix=".jsonl"),
                shards=1,
            )
        )

        # -----------------------------
        # SILVER → GCS
        # -----------------------------
        (
            silver
            | "SilverToJsonl" >> beam.Map(to_jsonl)
            | "WindowSilver" >> beam.WindowInto(
                windowing,
                trigger=trig,
                accumulation_mode=trigger.AccumulationMode.DISCARDING,
            )
            | "WriteSilver" >> fileio.WriteToFiles(
                path=f"{BUCKET}/silver/",
                destination=lambda x: "silver",
                file_naming=fileio.destination_prefix_naming(suffix=".jsonl"),
                shards=1,
            )
        )

        # -----------------------------
        # META → GCS
        # -----------------------------
        (
            meta
            | "MetaToJsonl" >> beam.Map(to_jsonl)
            | "WindowMeta" >> beam.WindowInto(
                windowing,
                trigger=trig,
                accumulation_mode=trigger.AccumulationMode.DISCARDING,
            )
            | "WriteMeta" >> fileio.WriteToFiles(
                path=f"{BUCKET}/metadata/",
                destination=lambda x: "meta",
                file_naming=fileio.destination_prefix_naming(suffix=".jsonl"),
                shards=1,
            )
        )


if __name__ == "__main__":
    run()
