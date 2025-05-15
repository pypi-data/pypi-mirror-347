# Authentication

The FluidGrids CLI requires authentication to interact with the FluidGrids Workflow Engine. This guide explains the available authentication methods and how to set them up.

## Authentication Methods

The FluidGrids CLI supports three authentication methods:

1. **Username and Password**: Log in with your FluidGrids account credentials
2. **API Key**: Use an API key for automated or programmatic access
3. **Token**: Use a JWT token obtained from another source

## Setting Up Authentication

### Username and Password

This is the most common authentication method for interactive use:

```bash
fluidgrids auth login --url https://api.fluidgrids.ai
```

You will be prompted to enter your username and password. These credentials will be securely stored for future use.

If you want to provide username and password directly (not recommended for security reasons):

```bash
fluidgrids auth login --url https://api.fluidgrids.ai --username your_username --password your_password
```

### API Key

For automation and CI/CD pipelines, using an API key is recommended:

```bash
fluidgrids auth set-key --api-key YOUR_API_KEY --url https://api.fluidgrids.ai
```

The API key will be securely stored for future use.

### Token

If you have a JWT token obtained from another source:

```bash
fluidgrids auth set-token --token YOUR_JWT_TOKEN --url https://api.fluidgrids.ai
```

## Checking Authentication Status

To check your current authentication status:

```bash
fluidgrids auth status
```

This will show:
- The API URL you're configured to use
- The authentication method in use
- Masked credentials for security

## Logging Out

To clear stored credentials and log out:

```bash
fluidgrids auth logout
```

## Configuration File

The FluidGrids CLI stores configuration in `~/.fluidgrids/config.yaml`. This file contains:

- The API URL
- Authentication preferences
- Other configuration options

Sensitive information like passwords and API keys are not stored in this file directly. Instead, they are stored securely using your system's keyring service.

## Environment Variables

You can also use environment variables for authentication:

```bash
# For API key authentication
export FLUIDGRIDS_API_KEY=your_api_key
export FLUIDGRIDS_API_URL=https://api.fluidgrids.ai

# For username/password authentication
export FLUIDGRIDS_USERNAME=your_username
export FLUIDGRIDS_PASSWORD=your_password
export FLUIDGRIDS_API_URL=https://api.fluidgrids.ai

# For token authentication
export FLUIDGRIDS_TOKEN=your_jwt_token
export FLUIDGRIDS_API_URL=https://api.fluidgrids.ai
```

Environment variables take precedence over stored credentials.

## Security Considerations

- Never share your FluidGrids credentials or API keys
- Use API keys with appropriate permissions for the task at hand
- Rotate API keys periodically, especially for production systems
- Avoid including credentials in scripts or version control
- For CI/CD systems, use secret management features to store credentials

## Troubleshooting

### Authentication Errors

If you're getting authentication errors, try the following:

1. Verify that you're using the correct API URL with `fluidgrids auth status`
2. Check that your credentials are correct by logging in again
3. If using an API key, verify that it's active and has the necessary permissions
4. If using a token, check that it hasn't expired

### Connection Issues

If you can't connect to the API:

1. Verify your internet connection
2. Check if the API URL is correct
3. Ensure there are no firewalls or network policies blocking the connection 