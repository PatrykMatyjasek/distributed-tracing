from sys import argv

from requests import get

from opentelemetry import trace
from opentelemetry.propagate import inject
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

trace.set_tracer_provider(
TracerProvider(
        resource=Resource.create({SERVICE_NAME: "DistributedTracingPythonExample"})
    )
)
tracer = trace.get_tracer_provider().get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    # configure agent
    agent_host_name='localhost',
    agent_port=6831,
)
# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(jaeger_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)

with tracer.start_as_current_span("python-client"):

    with tracer.start_as_current_span("client-server"):
        headers = {}
        inject(headers)
        requested = get(
            "http://localhost:7777/hello",
            params={"param": "foo"},
            headers=headers,
        )

        assert requested.status_code == 200
