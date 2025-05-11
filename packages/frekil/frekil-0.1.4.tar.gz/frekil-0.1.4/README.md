# Frekil SDK

The official Python SDK for the Frekil API.

## Installation

```bash
pip install frekil
```

## Usage

### Authentication

To use the SDK, you'll need an API key from your Frekil account:

```python
from frekil import FrekilClient

# Initialize the client with your API key
client = FrekilClient(api_key="your-api-key")
```

### Working with Projects

#### List Projects

```python
# Get all projects the authenticated user has access to
projects = client.projects.list()
print(projects)
```

#### Get Project Membership

```python
# Get membership details for a specific project
project_id = "project-uuid"
memberships = client.projects.get_membership(project_id)
print(memberships)
```

#### Bulk Allocate Images

```python
# Allocate images to specific annotators and reviewers
project_id = "project-uuid"
allocations = [
    {
        "image_key": "image1.jpg",
        "annotators": ["annotator1@example.com", "annotator2@example.com"],
        "reviewers": ["reviewer1@example.com", "reviewer2@example.com"]
    },
    {
        "image_key": "image2.jpg",
        "annotators": ["annotator1@example.com"],
        "reviewers": ["reviewer1@example.com"]
    }
]

result = client.projects.bulk_allocate_images(
    project_id=project_id,
    allocations=allocations,
    override_existing_work=False  # Set to True to override existing work
)
print(result)
```

## Error Handling

The SDK uses custom exception classes to handle API errors:

```python
from frekil.exceptions import FrekilAPIError, FrekilClientError

try:
    projects = client.projects.list()
except FrekilClientError as e:
    # Handle client errors (e.g., authentication issues, invalid parameters)
    print(f"Client error: {e} (Status: {e.status_code})")
    print(f"Error details: {e.error_details}")
except FrekilAPIError as e:
    # Handle API errors (e.g., server issues)
    print(f"API error: {e} (Status: {e.status_code})")
    print(f"Error details: {e.error_details}")
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/notatehq/frekil-python-sdk.git
cd frekil-python-sdk

# Install dependencies
pip install -e ".[dev]"
```

### Testing

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.