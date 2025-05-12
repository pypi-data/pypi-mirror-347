# Newberry Metrics

A Python package for tracking and analyzing AWS Bedrock API usage metrics, including costs, latency, and token usage, with an automatically launched dashboard for live visualization.

## Latest Version: 0.1.8

## Features

- Track API call costs, latency, and token usage (input/output).
- Automatic Streamlit dashboard for live visualization, launched as a background process.
- Dashboard displays KPIs (total/average cost & latency), hourly/daily charts, and detailed call logs.
- Maintain session-based metrics in a local JSON file, uniquely identified by AWS credentials.
- Support for multiple Bedrock models.
- Automatic AWS credential handling.
- Console alerts for configurable cost and latency thresholds.
- Method to manually stop the background dashboard process.

## Installation

```bash
pip install newberry_metrics
```

Ensure you also have Streamlit installed if it's not included as a direct dependency:
```bash
pip install streamlit pandas plotly
```

## AWS Credential Setup

The package uses the AWS credential chain to authenticate with AWS services. You can set up credentials in one of the following ways:

### 1. Using IAM Role (Recommended for EC2)
- Attach an IAM role to your EC2 instance with Bedrock permissions.
- No additional configuration needed.

### 2. Using AWS CLI
```bash
aws configure
```
This will create a credentials file at `~/.aws/credentials`.

### 3. Using Environment Variables
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region
```

## Usage Examples

### 1. Initialize TokenEstimator & Launch Dashboard

When you initialize `TokenEstimator`, it will automatically attempt to launch the Newberry Metrics dashboard as a **background process** if it's not already running. The dashboard URL (typically `http://localhost:8501`) and its Process ID (PID) will be printed to your console.

```python
from newberry_metrics import TokenEstimator
import json # For printing examples

# Initialize with your model ID and AWS region
model_id = "anthropic.claude-3-haiku-20240307-v1:0"
region = "us-east-1" # Specify your AWS region

# Optional: Define alert thresholds
cost_alert_threshold = 0.05  # Alert if total session cost exceeds $0.05
latency_alert_threshold_ms = 2000 # Alert if any single call takes > 2000ms

estimator = TokenEstimator(
    model_id=model_id,
    region=region,
    cost_threshold=cost_alert_threshold,      # Optional
    latency_threshold_ms=latency_alert_threshold_ms # Optional
)

# The dashboard should now be running in the background.
# Check your console for the URL and PID.
# Open the URL in your browser to see live metrics as you make calls.
# The dashboard will continue running even if this script finishes.
```

### 2. Get Model Pricing

Retrieve the cost per million tokens for the initialized model.

```python
costs = estimator.get_model_cost_per_million()
print(f"Input cost per million tokens: ${costs['input']}")
print(f"Output cost per million tokens: ${costs['output']}")
```

### 3. Making API Calls & Tracking Metrics

Use the `get_response` method to make calls to the Bedrock model. This method automatically tracks metrics (cost, latency, token counts), updates the session JSON file, and checks for alerts. The dashboard will reflect these updates upon refresh.

```python
prompt = "Explain the concept of Large Language Models in simple terms."
max_tokens_to_generate = 150

response_data = estimator.get_response(prompt=prompt, max_tokens=max_tokens_to_generate)

# The response_data contains details about the current call and the updated session totals.
print("\n--- API Call Response & Metrics ---")
print(f"Model's Answer (truncated): {response_data.get('answer', 'N/A')[:100]}...")

current_call = response_data.get('current_call_metrics', {})
print(f"\nMetrics for this Call:")
print(f"  Cost: ${current_call.get('cost', 0):.6f}")
print(f"  Latency: {current_call.get('latency', 0):.3f}s")
print(f"  Input Tokens: {current_call.get('input_tokens', 0)}")
print(f"  Output Tokens: {current_call.get('output_tokens', 0)}")

print(f"\nUpdated Session Totals:")
print(f"  Total Session Cost: ${response_data.get('total_cost_session', 0):.6f}")
print(f"  Average Session Cost: ${response_data.get('average_cost_session', 0):.6f}")
print(f"  Total Calls in Session: {response_data.get('total_calls_session', 0)}")

# Make another call
prompt_2 = "What are some key applications of LLMs?"
response_data_2 = estimator.get_response(prompt=prompt_2, max_tokens=200)
# ... inspect response_data_2 ...
# Refresh your dashboard in the browser to see the new data.
```

### 4. Using the Dashboard

- **Automatic Launch**: The dashboard starts as a background process when `TokenEstimator` is initialized (if not already running on port 8501). The URL (default: `http://localhost:8501`) and its PID are printed to the console.
- **Persistent Process**: The dashboard runs independently and will continue to run even after the Python script that launched it has exited.
- **Live Data**: The dashboard reads data from the `session_metrics_<CREDENTIAL_HASH>.json` file.
- **Refresh**: Use the refresh button (🔄) on the dashboard to load the latest data from the JSON file after new API calls are made.
- **Features**:
    - Key Performance Indicators (KPIs): Average/Total Cost, Average/Total Latency.
    - Charts: Hourly or Daily views for Cost, Latency, and Input/Output Token Distribution.
    - Detailed Table: A paginated table showing metrics for each individual API call in the session.
- **Shutdown**: To stop the dashboard, you can:
    - Call `TokenEstimator.stop_dashboard()` from any Python script where `TokenEstimator` is accessible.
    - Manually kill the process using the PID provided when the dashboard was launched. A `.newberry_dashboard.pid` file is also created in the package directory containing the PID.

```python
# Example of stopping the dashboard
# from newberry_metrics import TokenEstimator # If in a new script/session

# TokenEstimator.stop_dashboard()
# print("Attempted to stop the Newberry Metrics dashboard.")
```

### 5. Retrieve Current Session Metrics Programmatically

You can get the complete metrics object for the current session at any time.

```python
# from dataclasses import asdict # For printing example

current_session_object = estimator.get_session_metrics()
print(f"\n--- Full Session Metrics Object ---")
print(f"Total calls so far: {current_session_object.total_calls}")
print(f"Total session cost: ${current_session_object.total_cost:.6f}")
print(f"Average session latency: {current_session_object.average_latency:.3f}s")
# print(json.dumps(asdict(current_session_object), indent=2)) # For full details
```

### 6. Reset Session Metrics

Reset the tracked metrics for the current session (identified by AWS credentials) back to zero in the `session_metrics_*.json` file.

```python
estimator.reset_session_metrics()
print("Session metrics have been reset. Refresh the dashboard to see the changes.")
```

### 7. Stopping the Dashboard Manually

If you need to stop the dashboard process, you can use the static method `TokenEstimator.stop_dashboard()`. This method will attempt to find the dashboard's PID from a `.newberry_dashboard.pid` file (created when the dashboard starts) and terminate the process.

```python
from newberry_metrics import TokenEstimator

# Call this from any Python environment where TokenEstimator is available
TokenEstimator.stop_dashboard()
```
If `stop_dashboard()` is unable to terminate the process, or if the PID file is missing/corrupt, you may need to manually kill the process using its PID (which was printed to the console when the dashboard started).

## Supported Models

The package includes pricing information for the following Bedrock models (primarily in `us-east-1`). Ensure the model ID you use matches one of these or that its pricing and payload/response parsing logic is available in `bedrock_models.py`.

- amazon.nova-pro-v1:0
- amazon.nova-micro-v1:0
- anthropic.claude-3-sonnet-20240229-v1:0
- anthropic.claude-3-haiku-20240307-v1:0
- anthropic.claude-3-opus-20240229-v1:0
- meta.llama2-13b-chat-v1
- meta.llama2-70b-chat-v1
- ai21.jamba-1-5-large-v1:0
- cohere.command-r-v1:0
- cohere.command-r-plus-v1:0
- mistral.mistral-7b-instruct-v0:2
- mistral.mixtral-8x7b-instruct-v0:1
*(Pricing based on us-east-1, may vary in other regions. Token counting and payload structure depend on `bedrock_models.py`.)*

## Session Metrics & Alerting

The package automatically tracks and persists session metrics.
- **Session File**: A unique JSON file named `session_metrics_<CREDENTIAL_HASH>.json` is created in the directory where the script is run (or where `TokenEstimator` is initialized). The `<CREDENTIAL_HASH>` is derived from the AWS credentials and region.
- **Dashboard Source**: The Streamlit dashboard (`app.py`) reads data directly from this JSON file.

Metrics stored in the JSON and displayed on the dashboard include:
- `total_cost`, `average_cost`
- `total_latency`, `average_latency`
- `total_calls`
- `api_calls`: A detailed list (`List[APICallMetrics]`) for each call, including its timestamp, cost, latency, input/output tokens, and call counter.

**Alerting:**
If `cost_threshold` (e.g., `0.10` for $0.10) or `latency_threshold_ms` (e.g., `1500.0` for 1500ms) are provided during `TokenEstimator` initialization, warnings are printed to the console if:
- The **total cost** for the current session exceeds `cost_threshold`.
- The **latency** of an individual API call exceeds `latency_threshold_ms`.

## Requirements
- Python >= 3.10
- `boto3` for AWS Bedrock integration
- `streamlit` for the dashboard
- `pandas` for data manipulation in the dashboard
- `plotly` for charts in the dashboard

## Contact & Support
- **Developer**: Satya-Holbox, Harshika-Holbox
- **Email**: satyanarayan@holbox.ai
- **GitHub**: [SatyaTheG](https://github.com/SatyaTheG)

## License
This project is licensed under the MIT License.

---

**Note**: This package is actively maintained. Please ensure you are using the latest version for new features and model support.
