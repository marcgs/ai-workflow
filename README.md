# AI Workflow

This small sample exemplifies how a workflow can be orchestrated with an LLM.

Two main inputs are provided to the LLM to enable intelligent navigation through the workflow:

* Workflow Definition (see [release workflow](workflows/release-workflow.txt))
* Function Definitions (see [functionDefinitions.py](./functionDefinitions.py))

I this sample, calls to external systems performed by functions are mocked in [functionDefinitions.py](./functionDefinitions.py).

## Initial Setup

To run this sample you need to have an instance of Azure AI Foundry with an OpenAI chat model deployed (4o preferrably) - see [documentation](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource?pivots=web-portal).

Once your model is ready, create an `.env` file by copying `.env.template` and replacing values with your configuration.

## Running the sample

Install Python dependencies if not previously done:

```bash
poetry install
```

Run the sample by running

```bash
poetry run python orchestrator.py
```
