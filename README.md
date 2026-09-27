# CentroidApp
#### Video Demo: https://youtu.be/UNTwx1DWM5o
#### Description:

*CentroidApp* is a full-stack web application developed to execute, visualize, and store clustering analyses using the K-Means Machine Learning algorithm. The project stands out for its "Zero-Disk Write" architecture, where all data processing, chart generation, and file compression happen entirely in the server's RAM.

## The Project Idea
The main goal is to provide an interactive interface where users can select data scenarios, define the number of clusters (k) and the iteration limit, and instantly receive the visual and analytical results of the clustering process. In addition to asynchronously displaying the data on the screen, the system packages the reports and charts into a `.zip` file and archives them in a sql database for future reference (user execution history).

---

## Main Features

* *Asynchronous Processing:* Form submission via Fetch API, allowing the display of results and loaders (spinners) without reloading the page.
* *Visualization Generation:* Generates four distinct charts per execution:
  1. *Original Graph* (Initial data distribution).
  2. *Clusters Graph* (Final grouping and centroids).
  3. *Metrics Graph* (Performance evaluation, like Intra-cluster Variance).
  4. *Movement Graph* (Centroids movement values throughout the iterations).
* *Packaging:* In-memory generation of a `.zip` file (using `zipfile.ZIP_DEFLATED`) containing the 4 pure PNG images and a `.txt` log file.
* *Direct Download:* Delivery of the compressed ZIP package to the user via Base64 Data URIs, eliminating the need for temporary download links on the server.
* *View old executions :* Saves the `.zip` package in raw binary format (BLOB) directly into the database's `executions` table, linked to the logged-in user's ID.
* *Validation & Security:* Back-end methods against malicious data injection, ensuring parameters like k and iterations are numeric and within safe limits, returning http erros in case of violations.

---

## Technologies Used

*Back-end & Infrastructure:*
* *Python 3:* Main language for the server and algorithm.
* *Flask:* Web micro-framework for routing and HTTP request management.
* *SQLite3:* DBMS.

*Front-end:*
* *HTML5 & CSS3:* Semantic page structure.
* *Bootstrap 5:* Grid system, typography styling, UI components and responsive layout.
* *Vanilla JavaScript:* DOM manipulation and asynchronous communication .

*Data Science & Algorithm:*
* *Matplotlib:* Chart generation.
* *From zero K-Means:* Implementation of the clustering algorithm.

---

## Folder Structure

The repository structure was designed to clearly separate mathematical responsibilities, routing logic, and visual elements:

```text
centroidapp-webapp/
├── algorithm/                  # Algorithm core & Data Science Logic
│   ├── graphs_helper.py        # Matplotlib chart generation
│   ├── kmeans.py               # K-Means clustering implementation
│   └── scenarios.py            # Dataset scenario definitions and loading
├── db/                         # Database Layer
│   └── schema.sql              # Database schema initialization script
├── static/                     # Static assets served to the client
│   ├── js/
│   │   └── request_kmeans.js   # Client-side async logic
│   ├── scenarios/              # Image previews for dataset scenarios
│   │   ├── scenario1.png
│   │   ├── scenario2.png
│   │   ├── scenario3.png
│   │   ├── scenario4.png
│   │   └── scenario5.png
│   ├── favicon.ico             # Website favicon
│   └── styles.css              # Custom styling
├── templates/                  # HTML Templates
│   ├── account.html            # User account management page
│   ├── errorpage.html          # Custom error page
│   ├── executions.html         # Execution history & ZIP downloads
│   ├── index.html              # Execution interface
│   ├── layout.html             # Base layout template
│   ├── login.html              # User login interface
│   └── register.html           # User registration interface
├── .gitignore                  
├── app.py                      # Main Flask application
├── helpers.py                  # Helper functions (authentication decorators, etc.)
├── README.md                   # This document
└── requirements.txt            # Python dependencies