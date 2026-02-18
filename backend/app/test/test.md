I need you to create Python test fixtures using `factory.alchemy.SQLAlchemyModelFactory` from the `factory_boy` library for testing API endpoints in my backend application. The fixtures should generate mock data for realistic test scenarios while ensuring database isolation. Here are the requirements:

1. **Context**:
   - The database is PostgreSQL, running in an isolated Docker Compose environment for tests.
   - Tests are written using Pytest, and I use a test client (e.g., `TestClient` from FastAPI) to make HTTP requests.

2. **Model Structure**:
   - `User`: Has `id` (primary key, integer), `username` (unique string), `password` (string), `session_token` (unique string for authentication).
   - `Device`: Has `id` (primary key, integer), `user_id` (foreign key to `User.id`), `name` (string), and a relationship to `User`.

3. **Fixture Requirements**:
   - Create a `db_session` fixture to manage the SQLAlchemy session, ensuring it is properly closed after tests.
   - Create factory classes using `SQLAlchemyModelFactory`:
     - `UserFactory`: Generates unique `username` (e.g., `testuser1`) and `session_token` (e.g., `token1`).
     - `DeviceFactory`: Links to a `User` via `SubFactory` and generates unique `name` (e.g., `device1`).
   - Create a `mock_devices` fixture:
     - Takes a parameter `device_count` (default: 1) to create a specified number of devices for a user.
     - Returns a tuple of the created `User` object and a list of `Device` objects.
     - Commits the data to the database and relies on `clean_database` for cleanup.


4. **Additional Requirements**:
   - Use `factory_boy`'s `Sequence` for unique values and `SubFactory` for relationships.
   - Ensure fixtures work with a SQLAlchemy session and commit data correctly.
   - Include example tests for:
     - A `GET /devices` endpoint that lists all devices for a user, verifying the correct number of devices is returned.
   - Tests should use a `client` fixture (e.g., `TestClient` from FastAPI) for HTTP requests.
   - Do not include explicit teardown code for deleting objects, as `clean_database` handles cleanup.
   - Wrap the code in an `<xaiArtifact>` tag with a unique `artifact_id` (generate a new UUID), `title="test_fixtures.py"`, and `contentType="text/python"`.

5. **Output Format**:
   - Provide only the Python code wrapped in the `<xaiArtifact>` tag.
   - Do not include explanations or comments outside the `<xaiArtifact>` tag.
   - Ensure the code is complete, syntactically correct, and ready to use with Pytest, SQLAlchemy, and `factory_boy`.

Please generate the code based on these requirements.