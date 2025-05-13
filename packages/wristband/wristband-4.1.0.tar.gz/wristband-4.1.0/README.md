# fastapi-auth
SDK for integrating your Python FastAPI application with Wristband. Handles user authentication and token management.


1. Build package
```bash
# manual
poetry build

# Bump patch version (4.0.1 → 4.0.2)
poetry version patch

# Bump minor version (4.0.1 → 4.1.0)
poetry version minor

# Bump major version (4.0.1 → 5.0.0)
poetry version major
```
2. Set token 
```bash
poetry config pypi-token.pypi <your-token>
```