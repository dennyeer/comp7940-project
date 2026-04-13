CREATE TABLE IF NOT EXISTS message_logs (
    id SERIAL PRIMARY KEY,
    telegram_user_id BIGINT NOT NULL,
    username VARCHAR(255),
    user_message TEXT NOT NULL,
    bot_reply TEXT,
    response_time_ms INTEGER,
    estimated_cost NUMERIC(10, 6),
    status VARCHAR(50) DEFAULT 'success',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);