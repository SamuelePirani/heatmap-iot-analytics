### Creating/Updating the Conda Environment

Use the provided `environment.yml` file to create (or update) the Conda environment with all necessary dependencies:

- **Creating the environment:**

  ```bash
  conda env create -f environment.yml
  ```

- **Updating an existing environment:**

  ```bash
  conda env update -f environment.yml --prune
  ```

### Configuring MongoDB Connection Variables

The project uses environment variables to configure the MongoDB connection. After creating or updating your Conda
environment, set the appropriate variables using the following commands:

```bash
conda env config vars set MONGO_PASSWORD="your_password"
conda env config vars set MONGO_USERNAME="your_username"
conda env config vars set MONGO_URL="your_url"
```

### Running the Flask Application

After setting up the environment and configuring MongoDB, activate the Conda environment and run the Flask application:

```bash
conda activate heatmap-web
```

```bash
python main.py
```


### Verifying the Installation

To verify that Flask and PyMongo are installed correctly, you can check their versions:

```bash
python -c "import flask; print(flask.__version__)"
python -c "import pymongo; print(pymongo.__version__)"
```

If you encounter any issues, ensure that all dependencies are correctly installed using:

```bash
pip list | grep -E 'Flask|pymongo'
```

