# Python/Flask Backend

This directory contains the Python/Flask application for processing IoT data and exposing endpoints for the heat map
analytics.

---

## Table of Contents

- [Conda Environment](#conda-environment)
    - [Creating or Updating the Conda Environment](#creating-or-updating-the-conda-environment)
    - [Configuring MongoDB Variables](#configuring-mongodb-variables)
- [Running the Application](#running-the-application)
- [Verifying the Installation](#verifying-the-installation)
- [Additional Tips](#additional-tips)

---

## Conda Environment

### Creating or Updating the Conda Environment

A file named `environment.yml` is provided in this directory:

- **Create** the environment if you have not already:

  ```bash
  cd .\web\
  ```

  ```bash
  conda env create -f environment.yml
  ```

- **Update** the environment if it exists:

  ```bash
  conda env update -f environment.yml --prune
  ```

> The default environment name is **heatmap-web** (which you can change inside `environment.yml`).

### Configuring MongoDB Variables

Set your MongoDB credentials after creating/updating the environment:

```bash
conda env config vars set MONGO_USERNAME="your_username"
conda env config vars set MONGO_PASSWORD="your_password"
conda env config vars set MONGO_URL="your_url"
```

Deactivate and then reactivate the environment so these variables take effect:

```bash
conda deactivate
conda activate heatmap-web
```

---

## Running the Application

1. Run the Flask application:

   ```bash
   python main.py
   ```
2. If the server starts successfully, you will see console output indicating which port the application is listening on.

---

## Verifying the Installation

You can check package versions (e.g., Flask or PyMongo) to confirm dependencies are correctly installed:

```bash
python -c "import flask; print(flask.__version__)"
python -c "import pymongo; print(pymongo.__version__)"
```

To see a list of all installed packages and their versions:

```bash
pip list
```

---

## Additional Tips

- **IDE Usage**: Ensure your IDE is configured to use the `heatmap-web` environment.
- **Logging**: Logs can be inspected in the console or the location you configure in `main.py`.
- **Common Errors**:
    - Missing environment variables can lead to “Invalid URI host” exceptions if your MongoDB URI is incomplete.
    - If you cannot connect to MongoDB, confirm that the database accepts connections from your machine/IP.