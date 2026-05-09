-- SmartFarm initial schema
CREATE TABLE IF NOT EXISTS livestock (
  id SERIAL PRIMARY KEY,
  animal_id TEXT,
  species TEXT,
  health_status TEXT,
  temperature NUMERIC,
  recorded_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS crops (
  id SERIAL PRIMARY KEY,
  plot_id TEXT,
  crop_type TEXT,
  health_status TEXT,
  moisture_level NUMERIC,
  recorded_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS irrigation (
  id SERIAL PRIMARY KEY,
  schedule_id TEXT,
  plot_id TEXT,
  start_time TIMESTAMP,
  duration_minutes INT,
  status TEXT,
  recorded_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS worker_tasks (
  id SERIAL PRIMARY KEY,
  worker_id TEXT,
  task TEXT,
  assigned_at TIMESTAMP,
  completed_at TIMESTAMP,
  status TEXT,
  recorded_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS alerts (
  id SERIAL PRIMARY KEY,
  domain TEXT,
  reference_id TEXT,
  alert_type TEXT,
  message TEXT,
  severity TEXT,
  raised_at TIMESTAMP DEFAULT now()
);
