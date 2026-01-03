# Data Model: JWT Verification Dependency

## JWT Token Entity
- **Fields**:
  - token: str (JWT token string from Authorization header)
  - payload: dict (decoded JWT payload containing user information)
  - user_id: str (UUID string extracted from payload)
  - expiration: datetime (token expiration time from payload)
  - issuer: str (token issuer from payload)
- **Validation**:
  - Token must be valid JWT format
  - Token must be signed with the shared BETTER_AUTH_SECRET
  - Token must not be expired
  - Payload must contain valid user ID in expected location
- **Relationships**: Maps to User identity for authentication purposes
- **State Transitions**: N/A (JWT tokens are stateless)

## User Identity Entity (Conceptual)
- **Fields**:
  - id: str (UUID string from JWT payload)
  - email: str (from JWT payload, if available)
  - permissions: list (from JWT payload, if available)
- **Validation**:
  - ID must be valid UUID format
  - Email, if present, must be valid email format
- **Relationships**: Used by all protected endpoints to enforce access control

## Authorization Header Entity (Conceptual)
- **Fields**:
  - header_value: str (full Authorization header value)
  - scheme: str (expected to be "Bearer")
  - token: str (extracted JWT token)
- **Validation**:
  - Header must start with "Bearer "
  - Token must be present after the scheme
- **Relationships**: Contains JWT Token for verification