# 🇮🇳 Advanced Indian Price Intelligence Suite

An end-to-end data engineering pipeline and machine learning predictive system designed to scrape, persist, analyze, and forecast real-time consumer electronics market prices localized in Indian Rupees (₹). 

---

## 🚀 Key Architectural Strengths

* **Hybrid Polyglot Persistence Architecture:** Combines relational and document-based data models. Uses **MySQL** to serve highly optimized transactional states for real-time dashboard rendering and a **MongoDB** cluster to store infinite unstructured time-series price streams chronologically.
* **Quantified Machine Learning Analytics:** Ingests the 30-day historical time-series out of MongoDB into a **Scikit-Learn Linear Regression model** to predict forthcoming market trends while continually computing **Mean Absolute Error (MAE)** to display statistical model stability natively on the UI.
* **High-Performance Server-Side Visualization:** Renders automated trend analysis on the dashboard using a non-interactive **Matplotlib back-end engine (`Agg`)**, streaming the graph plot matrices cleanly as memory buffers via **Base64 binary encodings** directly into standard HTML `<img>` elements.
* **Immediate Deployment Seeding:** Includes a programmatic data initialization engine that dynamically manufactures a realistic, 30-day simulated historical volatility dataset on the very first server boot, eliminating external data configuration dependencies.

---

## 📁 System Core Modules

```text
AI-Price-Tracker-Web/
├── src/
│   ├── scraper.py         # Ingestion Engine: Standardizes cross-platform marketplace pricing data arrays
│   ├── database.py        # Storage Router: Manages parallel MySQL/MongoDB pipelines & 30-day data seeding
│   └── forecaster.py      # Analytics Core: Fits regression paths & evaluates real-time forecasting metrics
├── templates/
│   └── index.html         # User Interface: Dark-mode dashboard built for immediate visual scannability
└── app.py                 # Core Controller: Main Flask application orchestrator handling runtime server threads
