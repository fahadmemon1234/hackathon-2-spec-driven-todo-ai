# Research Findings: JWT Verification Dependency

## Decision: Testing Approach
**Rationale**: For a FastAPI authentication dependency, pytest with FastAPI TestClient is the standard approach. This provides excellent integration with FastAPI's dependency injection system and async features.
**Alternatives considered**:
- unittest (more verbose for async testing)
- pytest with requests library (doesn't leverage FastAPI's test client benefits)
- Manual testing only (insufficient for reliable development)

## Decision: JWT Library Selection
**Rationale**: python-jose is specifically recommended for FastAPI applications and provides robust JWT handling with support for various cryptographic algorithms. It's actively maintained and well-documented.
**Alternatives considered**:
- PyJWT (also good, but python-jose has better integration with FastAPI)
- authlib (more comprehensive but potentially overkill for this use case)
- Custom implementation (not recommended due to security considerations)

## Decision: Environment Variable Loading
**Rationale**: Using python-dotenv for loading environment variables is the standard practice. This ensures sensitive information like BETTER_AUTH_SECRET is not hardcoded in the source code.
**Alternatives considered**:
- Hardcoding the secret in source (major security vulnerability)
- Storing in a local file (still insecure and not flexible for deployments)

## Decision: Error Handling Strategy
**Rationale**: FastAPI provides built-in HTTPException for returning appropriate status codes. Using custom exception handlers will provide consistent error responses across the API.
**Alternatives considered**:
- Generic try/catch blocks (less elegant and inconsistent)
- Returning error responses manually in each endpoint (repetitive and error-prone)

## Decision: Dependency Injection Pattern
**Rationale**: FastAPI's dependency injection system is ideal for handling authentication. Creating a dependency for JWT verification will ensure all protected endpoints have consistent authentication logic.
**Alternatives considered**:
- Manual token verification in each endpoint (repetitive and error-prone)
- Decorator-based authentication (less integrated with FastAPI's native patterns)

## Decision: Token Structure Handling
**Rationale**: Better Auth may place user ID in different locations in the JWT payload. Safely checking for both common structures ("user.id" and "id") ensures compatibility with different configurations.
**Alternatives considered**:
- Assuming a single payload structure (would not work with all Better Auth configurations)
- Using a configuration option (adds unnecessary complexity for this specific use case)