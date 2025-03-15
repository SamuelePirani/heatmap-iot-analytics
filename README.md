# Heat-map Analytics

This project creates an analytics pipeline to generate geolocated heat maps based on time-series IoT data.  
By integrating temporal data (IoT events) with corresponding geolocation data, the pipeline aggregates information over
selected time windows and visualizes it on a geo-heat map.

![Heat-map Visualization](docs/images/Figure1.png)

---

## Table of Contents

- [Prerequisites](#prerequisites)
    - [JDK 17 Installation](#jdk-17-installation)
    - [Conda Installation](#conda-installation)
- [Repository Structure](#repository-structure)
- [Environment Setup](#environment-setup)
    - [Creating or Updating the Conda Environment](#creating-or-updating-the-conda-environment)
    - [Configuring MongoDB Connection Variables](#configuring-mongodb-connection-variables)
- [Running the Backend Application](#running-the-backend-application)
- [Running the Angular Client](#running-the-angular-client)
- [Additional Notes](#additional-notes)

---

## Prerequisites

### JDK 17 Installation

The project includes Java-based components. To install JDK 17 or a compatible version:

1. Download a JDK (e.g., [Oracle JDK 17](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)).
2. Run the installer.
3. Verify your setup:
   ```bash
   java --version
   ```
4. Ensure the `JAVA_HOME` environment variable points to the JDK installation path.

### Conda Installation

If you do not have Conda installed:

1. Download and install [Anaconda](https://www.anaconda.com/download).
2. Confirm Conda is accessible via your system’s PATH.

---

## Repository Structure

A brief overview of key folders:

- **src/api/**  
  Contains the Python/Flask application and environment files.
- **client/**  
  Contains the Angular application for UI and data visualization.
- **web/**
  Contains the service Web API that starts the frontend.
- **heatmap-iot-analytics/**  
  Documentation and images (including heat map examples).

---

## Environment Setup

### Creating or Updating the Conda Environment

In the root folder (`heatmap-iot-analytics/`), an `environment.yml` file is provided to manage Python
dependencies:

- **Cloning the Project**

  ```bash
  git clone https://github.com/SamuelePirani/heatmap-iot-analytics.git
  ```

  ```bash
  cd heatmap-iot-analytics
  ```

- **Creating the environment**:

  ```bash
  conda env create -f environment.yml
  ```

- **Updating an existing environment**:

  ```bash
  conda env update -f environment.yml --prune
  ```

> By default, this environment is named **heatmap-iot-analytics**. If you wish to use a different name, edit
`environment.yml`
> accordingly.

### Configuring MongoDB Connection Variables

After creating or updating the Conda environment, configure your MongoDB credentials:

```bash
conda env config vars set MONGO_USERNAME="your_username"
conda env config vars set MONGO_PASSWORD="your_password"
conda env config vars set MONGO_URL="your_url"
```

Deactivate and reactivate the environment for changes to take effect:

```bash
conda deactivate
conda activate heatmap-web
```

---

## Running the Backend Application

1. In the root directory, run the Spark application:

   ```bash
   python main.py
   ```

2. Check for any console output or logs to ensure the server has started successfully.

---

## Running the Angular Client

The Angular client resides in the **client/** directory. Steps to build and serve the client
at [Client Readme](client/README.md)

---

## Additional Notes

- **IDE Configuration**: If you use an IDE (such as PyCharm or VSCode), make sure it points to the correct Conda
  environment for the Python backend.
- **Troubleshooting**:
    - If you see MongoDB connection errors, verify your `MONGO_*` environment variables.
- **Further Documentation**:
    - Check the **web/README.md** for more backend-api-specific details.
    - Check the **client/README.md** for more client-specific details.