# Examples

Examples of how to use Patronus and what it can do.

## Usage

These examples demonstrate common use cases and integration patterns for Patronus.

### Installing required dependencies

Each example requires specific dependencies to run. The dependencies are defined in the `patronus-examples` package. You can install these dependencies in a few ways:

#### Manual installation

You can install the dependencies manually as shown in each example's documentation. For example:

```bash
pip install patronus
pip install smolagents[litellm]
pip install openinference-instrumentation-smolagents
pip install opentelemetry-instrumentation-threading
```

#### Using uv with the examples package

The easiest way to run examples is with `uv`, which can automatically install the required dependencies:

```bash
# For smolagents examples
uv run --with "patronus-examples[smolagents]" \
  -m patronus-examples.tracking.smolagents-weather
```

This installs the `patronus-examples` package with the `smolagents` optional dependencies.

### Setting required environment variables

Most examples require you to set up authentication with Patronus and other services. In most cases, you'll need to set the following environment variables:

```bash
export PATRONUS_API_KEY=your-api-key
export OPENAI_API_KEY=your-api-key
```

### Running Examples

To run the examples after installing dependencies:

```bash
python -m patronus-examples.<example_module_name>
```

For example, to run the `smolagents-weather` example:

```bash
python -m patronus-examples.tracking.smolagents-weather
```

If you're using `uv` and prefer one-liners, you can run an example with minimal setup:

```bash
# Remember to export environment variables before running the example.
uv run --with "patronus-examples[smolagents]" \
  -m patronus-examples.tracking.smolagents-weather
```
