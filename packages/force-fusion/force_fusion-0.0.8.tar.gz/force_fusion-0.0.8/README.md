<div align="center">
   <a href="https://github.com/Sang-Buster/Force-Fusion">
      <img src="https://raw.githubusercontent.com/Sang-Buster/Force-Fusion/refs/heads/main/src/force_fusion/resources/favicon.png" width=40% alt="logo">
   </a>
   <h1>Force Fusion</h1>
   <a href="https://deepwiki.com/Sang-Buster/Force-Fusion"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>
   <a href="https://pypi.org/project/force-fusion/"><img src="https://img.shields.io/pypi/v/force-fusion" alt="PyPI"></a>
   <a href="https://github.com/Sang-Buster/Force-Fusion/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Sang-Buster/Force-Fusion" alt="License"></a>
   <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/badge/package%20manager-uv-000000.svg" alt="uv"></a>
   <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/code%20style-ruff-000000.svg" alt="Ruff"></a>
   <a href="https://pepy.tech/project/force-fusion"><img src="https://img.shields.io/pypi/dm/force-fusion" alt="Downloads"></a>
   <a href="https://github.com/Sang-Buster/Force-Fusion/commits/main"><img src="https://img.shields.io/github/last-commit/Sang-Buster/Force-Fusion" alt="Last Commit"></a>
   <h6><small>A real-time PyQt dashboard visualizing vehicle dynamics and normal-force distribution.</small></h6>
   <p><b>#Vehicle Dynamics &emsp; #Normal-force Estimation &emsp; #PyQt &emsp; #3D Visualization</b></p>
</div>

---

[▶️ Watch Demo Video](https://github.com/user-attachments/assets/6da15919-4409-4f2f-801d-bb6dbe1a3da1)

<div align="center">
  <h2>🚀 Getting Started</h2>
</div>

It is recommended to use [uv](https://docs.astral.sh/uv/getting-started/installation/) to create a virtual environment and pip install the following package.

```bash
pip install force-fusion
```

To run the application, simply type:

```bash
force-fusion
# or
force-fusion --help
```

---

<div align="center">
  <h2>👨‍💻 Development Setup</h2>
</div>

1. **Clone the repository and navigate to project folder:**
   ```bash
   git clone https://github.com/Sang-Buster/Force-Fusion
   cd Force-Fusion
   ```

2. **Install uv first:**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   ```powershell
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Create a virtual environment at `Force-Fusion/.venv/`:**
   ```bash
   uv venv --python 3.10
   ```

4. **Activate the virtual environment:**
   ```bash
   # macOS/Linux
   source .venv/bin/activate
   ```

   ```powershell
   # Windows
   .venv\Scripts\activate
   ```

5. **Install the required packages:**
   ```bash
   uv pip install -e .
   ```

6. **Set up environment variables:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   ```
   - You can get a `MAPBOX_TOKEN` by signing up at https://www.mapbox.com/
   - Update the `CSV_PATH` if you want to use a custom database file
   - Update the `WS_HOST` if you want to use a custom websocket host
   - Update the `WS_PORT` if you want to use a custom websocket port
   - Update the `WS_RECONNECT_INTERVAL` if you want to use a custom websocket reconnect interval
   - Modify more variables in `.env` as needed

7. **Install ruff and pre-commit:**
   ```bash
   uv pip install ruff pre-commit
   ```
   - `ruff` is a super fast Python linter and formatter.
   - `pre-commit` helps maintain code quality by running automated checks before commits are made.

8. **Install git hooks:**
   ```bash
   pre-commit install --hook-type commit-msg --hook-type pre-commit --hook-type pre-push
   ```

   These hooks perform different checks at various stages:
   - `commit-msg`: Ensures commit messages follow the conventional format
   - `pre-commit`: Runs Ruff linting and formatting checks before each commit
   - `pre-push`: Performs final validation before pushing to remote
  
9. **Code Linting:**
   ```bash
   ruff check
   ruff check --fix
   ruff check --select I
   ruff check --select I --fix
   ruff format
   ```

10. **Run the application:**
   ```bash
   uv run src/force_fusion/app.py
   ```

---

<div align="center">
  <h2>📝 File Structure</h2>
</div>

```text
📂Force-Fusion
 ┣ 📂src                         // Source Code
 ┃ ┗ 📦force_fusion                  // Python package
 ┃ ┃ ┣ 📂cli                             // Command Line Interface Directory
 ┃ ┃ ┃ ┣ 📄cli.py
 ┃ ┃ ┃ ┣ 📄env.py
 ┃ ┃ ┃ ┣ 📄test.py
 ┃ ┃ ┣ 📂resources                       // Static Resources Directory
 ┃ ┃ ┃ ┣ 📄car_back.svg
 ┃ ┃ ┃ ┣ 📄car_side.svg
 ┃ ┃ ┃ ┣ 📄demo.mp4
 ┃ ┃ ┃ ┣ 📄favicon.png
 ┃ ┃ ┃ ┗ 📄styles.qss
 ┃ ┃ ┣ 📂utils                           // Utility Directory
 ┃ ┃ ┃ ┣ 📄env_utils.py
 ┃ ┃ ┃ ┣ 📄geo_utils.py
 ┃ ┃ ┃ ┣ 📄test_utils.py
 ┃ ┃ ┃ ┣ 📄websocket_client_test.py
 ┃ ┃ ┃ ┗ 📄websocket_server.py
 ┃ ┃ ┣ 📂widgets                         // Widgets Directory  
 ┃ ┃ ┃ ┣ 📄attitude.py
 ┃ ┃ ┃ ┣ 📄gg_diagram.py
 ┃ ┃ ┃ ┣ 📄heading.py
 ┃ ┃ ┃ ┣ 📄mapbox_view.py
 ┃ ┃ ┃ ┣ 📄minimap.py
 ┃ ┃ ┃ ┣ 📄speedometer.py
 ┃ ┃ ┃ ┗ 📄tire_force.py
 ┃ ┃ ┣ 📄app.py
 ┃ ┃ ┣ 📄config.py
 ┃ ┃ ┣ 📄controller.py
 ┃ ┃ ┣ 📄sensors.py
 ┃ ┃ ┗ 📄ui_main_window.py
 ┣ 📄.env.example                // Template for environment variables
 ┣ 📄.gitignore                  // Git ignore patterns (env, cache, database)
 ┣ 📄.pre-commit-config.yaml     // Pre-commit hooks (ruff, commit message)
 ┣ 📄.pre-commit_msg_template.py // Commit message format validator
 ┣ 📄.python-version             // Python version
 ┣ 📄LICENSE                     // MIT License
 ┣ 📄README.md                   // Project documentation
 ┣ 📄pyproject.toml              // Project configuration
 ┗ 📄uv.lock                     // Lock file
 ```