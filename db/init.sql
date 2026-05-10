CREATE TABLE IF NOT EXISTS alerts (
  id SERIAL PRIMARY KEY,
  domain TEXT,
  animal_id TEXT,
  temperature NUMERIC,
  health_status TEXT,
  moisture_level NUMERIC,
  status TEXT,
  plot_id TEXT,
  worker_id TEXT,
  task TEXT,
  recorded_at TIMESTAMP,
  detected_at TIMESTAMP DEFAULT NOW()
);
