# tool-interface

Main Python package to access the 3DTrees backend from tool containers. This package provides a unified interface for interacting with various backend services (Supabase, S3) used in the 3DTrees project.

## Installation

Using `uv`:
```bash
uv pip install git+https://github.com/3dtrees-earth/tool-interface.git
```

Using `pip`:
```bash
pip install git+https://github.com/3dtrees-earth/tool-interface.git
```

## Configuration

The package uses environment variables for configuration. All variables should be prefixed with `THREEDTREES_`. You can also use a `.env` file.

Required environment variables:
```bash
# Supabase
THREEDTREES_SUPABASE_URL=your_supabase_url
THREEDTREES_SUPABASE_KEY=your_supabase_key

# Storage (S3 compatible)
THREEDTREES_STORAGE_ACCESS_KEY=your_access_key
THREEDTREES_STORAGE_SECRET_KEY=your_secret_key
THREEDTREES_STORAGE_BUCKET_NAME=your_bucket_name

# Optional
THREEDTREES_STORAGE_ENDPOINT_URL=custom_s3_endpoint  # For non-AWS S3
THREEDTREES_STORAGE_REGION=eu-central-1  # Default: eu-central-1
THREEDTREES_PROCESSING_TEMP_DIR=/tmp/3dtrees  # Default: /tmp/3dtrees
```

## Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```
3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## License

See [LICENSE](LICENSE) file.
