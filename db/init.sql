CREATE TABLE IF NOT EXISTS greetings (
    id BIGSERIAL PRIMARY KEY,
    message TEXT NOT NULL CHECK (length(message) > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO greetings (message)
SELECT 'Hello, world!'
WHERE NOT EXISTS (SELECT 1 FROM greetings);

