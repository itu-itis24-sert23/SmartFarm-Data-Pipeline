# SmartFarm: End-to-End IoT Data Pipeline

This repository provides a comprehensive infrastructure for a Smart Agriculture data pipeline. It integrates **Docker Compose**, **Apache Airflow**, **Apache NiFi**, **PostgreSQL**, and the **ELK Stack** (Elasticsearch & Kibana) to simulate, ingest, and visualize synthetic farm data.

## 🚀 Quick Start

Build and launch all services in detached mode:

```bash
docker compose up --build -d

```

## 📂 Project Structure

* `docker-compose.yml`: Container orchestration for all 7 services.
* `db/init.sql`: PostgreSQL schema defining `livestock`, `crops`, `irrigation`, `worker_tasks`, and `alerts`.
* `scripts/generate_data.py`: Synthetic data generator (12k+ records) using the Faker library.
* `airflow/dags/smartfarm_dag.py`: Orchestration DAG to trigger data generation.
* `nifi/Nifi_Flow.json`: Pre-configured NiFi ingestion and routing flow.

---

## ⚙️ Configuration & Setup

### 1. Airflow Access

Retrieve the auto-generated admin password:

```bash
docker exec -it airflow-standalone cat /opt/airflow/standalone_admin_password.txt

```
* **URL:** `http://localhost:8082`
* **Username:** `admin`
* **Password:** (from above command)
or

```bash
docker exec airflow-standalone airflow users delete --username admin
docker exec airflow-standalone airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.org --password admin
```
* **URL:** `http://localhost:8082`
* **Username:** `admin`
* **Password:** `admin`


**Permissions Fix:** If you encounter a `Permission Denied` error during DAG execution, run:

```bash
docker exec -u root airflow-standalone chmod -R 777 /data/input

```

### 2. Apache NiFi Setup

**JDBC Driver Installation:**
Copy the PostgreSQL driver to the NiFi container:

```bash
docker cp ./nifi/postgresql-42.7.3.jar nifi:/opt/nifi/nifi-current/lib/

```

**Workflow Activation:**

1. Access NiFi: `https://localhost:8443/nifi`
* **User:** `nifi` | **Password:** `NifiNifi_12345!`


2. Import `Nifi_Flow.json` as a Process Group.
3. Configure `DBCPConnectionPool`:
* Set password to: `smartfarm`
* Set Driver Location: `/opt/nifi/nifi-current/lib/postgresql-42.7.3.jar`


4. Right-click on the Controller Services to **Enable** them, then **Start** the flow.

### 3. Database Management (pgAdmin)

* **URL:** `http://localhost:5050`
* **Login:** `admin@smartfarm.com` | `admin`
* **Server Connection:**
* **Host:** `postgres-db`
* **Maintenance DB:** `smartfarm`
* **Username/Password:** `smartfarm` / `smartfarm`



---

## 🛠️ Data Pipeline Workflow

1. **Generation:** Airflow triggers `generate_data.py`, creating `generator_output.jsonl` in the shared volume.
2. **Ingestion:** NiFi `GetFile` monitors the directory and consumes the JSONL records.
3. **Routing:** NiFi parses the `domain` attribute (livestock, crop, etc.) and routes anomalies (e.g., high temperature) to the `alerts` table and normal data to respective tables.
4. **Storage:** PostgreSQL stores structured data for long-term persistence.
5. **Visualization:** Kibana connects to Elasticsearch to visualize alerts and farm metrics (Manual dashboard setup required).

---

## 📈 Next Steps

* **Kibana Dashboards:** Once data flows into Elasticsearch, create a Data View for `alerts*` to build real-time monitoring graphs.
* **Jupyter Analysis:** Use the included Jupyter container (`localhost:8888`) to perform advanced data science on the stored Postgres data.

---