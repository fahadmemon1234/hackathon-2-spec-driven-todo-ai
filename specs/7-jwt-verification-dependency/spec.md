# Feature Specification: JWT Verification Dependency

**Feature Branch**: `7-jwt-verification-dependency`
**Created**: 2025-01-07
**Status**: Draft
**Input**: User description: "# Task 3: JWT Verification Dependency Specification + Implementation # Phase II Backend – Secure Authentication using Better Auth JWT # Current Status: Task 1 & Task 2 complete (DB connected, Task model ready) You are an expert FastAPI security engineer. Goal for Task 3: Implement a robust JWT verification dependency that: - Extracts JWT from Authorization: Bearer <token> header sent by frontend - Verifies and decodes it using the same BETTER_AUTH_SECRET (HS256 algorithm) - Extracts the authenticated user's ID (string UUID) - Returns the user_id for use in all task routes - Rejects invalid, missing, or expired tokens with proper 401 response Key Details from Better Auth (v1.4+, December 31, 2025): - Frontend sends stateless JWT in Bearer header (configured via JWT strategy or plugin) - JWT is signed with BETTER_AUTH_SECRET using HS256 - Payload structure typically contains: { \"user\": { \"id\": \"uuid-string\", \"email\": \"...\", ... }, ... other claims } or sometimes directly \"id\": \"uuid-string\" - We must handle both possibilities safely Requirements: 1. Install Required Package - pyjwt with cryptography: pip install pyjwt[cryptography] 2. Implement in dependencies.py Create or update dependencies.py with exactly this function: from fastapi import Header, HTTPException, Depends from jose import JWTError, jwt import os from dotenv import load_dotenv load_dotenv() def get_current_user_id( Authorization: str = Header(...) ) -> str: \"\"\" Dependency to extract and verify JWT from Bearer header Returns authenticated user_id (str UUID) \"\"\" if not Authorization.startswith(\"Bearer \"): raise HTTPException( status_code=401, detail=\"Invalid authorization header. Expected: Bearer <token>\" ) token = Authorization.split(\" \")[1] secret = os.getenv(\"BETTER_AUTH_SECRET\") if not secret: raise RuntimeError(\"BETTER_AUTH_SECRET not set in .env\") try: payload = jwt.decode( token, secret, algorithms=[\"HS256\"] ) # Extract user_id safely from common Better Auth payload structures user_id: str | None = None if \"user\" in payload and isinstance(payload[\"user\"], dict): user_id = payload[\"user\"].get(\"id\") elif \"id\" in payload: user_id = payload.get(\"id\") if not user_id or not isinstance(user_id, str): raise HTTPException(status_code=401, detail=\"Invalid token: missing user ID\") return user_id except JWTError as e: raise HTTPException(status_code=401, detail=\"Invalid or expired token\") 3. Expected Behavior - Valid token → returns user_id (str) - No token / wrong format → 401 - Invalid signature / expired → 401 - Missing user ID in payload → 401 - BETTER_AUTH_SECRET missing → server error (for dev catch) 4. Usage in Future Routes This dependency will be used as: user_id: str = Depends(get_current_user_id) Refer to: @specs/features/authentication.md @backend/CLAUDE.md Now implement Task 3 exactly as specified. Create/update dependencies.py with the secure get_current_user_id function. Ensure proper imports, error handling, and comments. After this task, backend will be able to identify authenticated users from frontend JWTs."
**Constitution Compliance**: All features must adhere to project constitution principles

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure API Access (Priority: P1)

An authenticated user wants to access protected API endpoints by sending a JWT token in the Authorization header. The system must verify the token and allow access to the user's own resources while rejecting invalid or expired tokens.

**Why this priority**: This is the fundamental security mechanism that protects all user data and ensures only authenticated users can access the API.

**Independent Test**: Can be fully tested by sending requests with valid and invalid JWT tokens and verifying that only valid tokens grant access to protected resources, delivering the core value of secure API access.

**Acceptance Scenarios**:

1. **Given** a user has a valid JWT token from Better Auth, **When** they send a request with Authorization: Bearer <token>, **Then** the request is processed with the user's identity verified
2. **Given** a user has an invalid JWT token, **When** they send a request with Authorization: Bearer <invalid_token>, **Then** a 401 Unauthorized response is returned
3. **Given** a user has an expired JWT token, **When** they send a request with Authorization: Bearer <expired_token>, **Then** a 401 Unauthorized response is returned
4. **Given** a user sends a request without an Authorization header, **When** the system checks authentication, **Then** a 401 Unauthorized response is returned

---

### User Story 2 - User Identity Extraction (Priority: P1)

An API endpoint needs to identify which user is making the request to enforce proper data isolation. The system must extract the user's unique identifier from the JWT payload to associate actions with the correct user account.

**Why this priority**: Without proper user identification, the system cannot enforce data isolation, which would allow users to access each other's resources.

**Independent Test**: Can be fully tested by sending requests with valid JWT tokens and verifying that the correct user ID is extracted from the token payload, delivering the core value of user-specific data access.

**Acceptance Scenarios**:

1. **Given** a valid JWT with user ID in the "user.id" field, **When** the system processes the token, **Then** the correct user ID is extracted and returned
2. **Given** a valid JWT with user ID in the "id" field, **When** the system processes the token, **Then** the correct user ID is extracted and returned
3. **Given** a JWT without a valid user ID field, **When** the system processes the token, **Then** a 401 Unauthorized response is returned
4. **Given** a malformed JWT, **When** the system attempts to decode it, **Then** a 401 Unauthorized response is returned

---

### User Story 3 - Token Validation Robustness (Priority: P2)

The system needs to handle various token validation scenarios gracefully to maintain security and provide appropriate feedback. The system must reject improperly formatted tokens while maintaining secure error handling.

**Why this priority**: Robust token validation prevents security vulnerabilities and ensures the API behaves predictably under various conditions.

**Independent Test**: Can be fully tested by sending various types of invalid tokens and verifying appropriate rejection with secure error messages, delivering the value of resilient authentication.

**Acceptance Scenarios**:

1. **Given** a token with incorrect format (not Bearer <token>), **When** the system validates it, **Then** a 401 Unauthorized response is returned with appropriate message
2. **Given** a token with wrong signature, **When** the system verifies it, **Then** a 401 Unauthorized response is returned
3. **Given** a token with unsupported algorithm, **When** the system processes it, **Then** a 401 Unauthorized response is returned
4. **Given** a token with missing secret configuration, **When** the system attempts verification, **Then** a server error occurs during development

---

### Edge Cases

- What happens when the BETTER_AUTH_SECRET environment variable is not set?
- How does the system handle JWT payloads with unexpected structures?
- What occurs when the token contains non-string user IDs?
- How does the system handle extremely long token strings?
- What happens when the authorization header contains unexpected characters?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST extract JWT tokens from Authorization: Bearer <token> header
- **FR-002**: System MUST verify JWT tokens using the BETTER_AUTH_SECRET with HS256 algorithm
- **FR-003**: System MUST extract user ID from JWT payload (supporting both "user.id" and "id" structures)
- **FR-004**: System MUST return the authenticated user ID as a string for use in route dependencies
- **FR-005**: System MUST reject invalid, expired, or missing tokens with HTTP 401 status
- **FR-006**: System MUST handle both payload structures: {"user": {"id": "uuid"}} and {"id": "uuid"}
- **FR-007**: System MUST validate that extracted user ID is a valid string UUID format
- **FR-008**: System MUST provide clear error messages for different failure scenarios
- **FR-009**: System MUST load BETTER_AUTH_SECRET from environment variables
- **FR-010**: System MUST raise appropriate exceptions when BETTER_AUTH_SECRET is not configured
- **FR-011**: System MUST be usable as a FastAPI dependency with Depends(get_current_user_id)
- **FR-012**: System MUST be thread-safe for concurrent API requests
- **FR-013**: System MUST not expose sensitive information in error responses
- **FR-014**: System MUST validate token format before attempting to decode
- **FR-015**: System MUST handle JWT decoding errors gracefully

### Key Entities

- **JWT Token**: Represents an authentication token containing user identity information, signed with BETTER_AUTH_SECRET using HS256 algorithm
- **User Identity**: Represents the authenticated user's unique identifier (UUID string) extracted from the JWT payload
- **Authorization Header**: Represents the HTTP header containing the Bearer token for authentication

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Valid JWT tokens are accepted and user IDs extracted with 99.9% success rate
- **SC-002**: Invalid or expired JWT tokens are rejected with appropriate 401 responses 100% of the time
- **SC-003**: User ID extraction from JWT payloads completes in under 50ms for 95% of requests
- **SC-004**: System handles 1000 concurrent authentication requests without degradation
- **SC-005**: All supported JWT payload structures are handled correctly (both "user.id" and "id" formats)
- **SC-006**: Error responses provide sufficient information for clients without exposing security details
- **SC-007**: The authentication dependency integrates seamlessly with FastAPI route dependencies
- **SC-008**: Memory usage remains stable during sustained authentication operations
- **SC-009**: Token validation prevents unauthorized access to protected resources with 100% effectiveness
- **SC-010**: The system properly handles misconfigured environment variables during startup