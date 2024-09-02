import uvicorn
from fastapi import FastAPI
from backend.routes import routes
from starlette.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


# Set the service name
resource = Resource(attributes={
    "service.name": "Fastapi_try"
})

# Initialize TracerProvider with the resource
trace.set_tracer_provider(TracerProvider(resource=resource))

# Create a Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name='localhost',
    agent_port=6831,
)

# Add the exporter to the tracer provider
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)


# Main app
app = FastAPI(debug=True, title="Basic E-Commerce API", version="1.0.0",
              summary="A basic E-Commerce API with applied security for "
                      "managing products and learning how to make "
                      "REST APIs."
              )

# Instrument the FastAPI app
FastAPIInstrumentor.instrument_app(app)

# Set up the tracer
tracer = trace.get_tracer(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Includes router of every sub-app
app.include_router(routes.router)


# Demo/Home endpoint
@app.get("/")
async def home():
    with trace.get_tracer(__name__).start_as_current_span("demo-span"):
        return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000,
                log_level="info",
                reload=True)

# uvicorn main:app --host 0.0.0.0 --port 8000
