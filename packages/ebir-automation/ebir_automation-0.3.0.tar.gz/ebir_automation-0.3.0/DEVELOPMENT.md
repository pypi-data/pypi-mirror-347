# ebir-automation Development

This document is for contributors and maintainers of the ebir-automation project.

## 1. Environment Setup

1. Install [uv](https://github.com/astral-sh/uv):
   ```sh
   pip install uv
   ```
2. Install all project dependencies (from `pyproject.toml`):
   ```sh
   uv install
   ```
   > Note: All dependencies are managed in `pyproject.toml`. There is no `requirements.txt`.
3. (Optional) Activate your virtual environment if not already active.
4. Ensure you have Rust 2021 or newer (Rust 2024 recommended):
   ```sh
   rustup update stable
   rustup default stable
   ```

## 2. Development Workflow

- To run Rust tests (with output):

  ```sh
  cargo test test_open_application -- --nocapture
  ```

  Or run all Rust tests:

  ```sh
  cargo test -- --nocapture
  ```

- To run Python tests (while in the uv environment):

  ```sh
  pytest
  ```

- To check Rust code for errors and warnings:

  ```sh
  cargo clippy -- -D warnings
  ```

- To use the Python extension in your environment (for import and testing):

  ```sh
  maturin develop
  ```

- To build a wheel file for distribution or installation on another system:
  ```sh
  maturin build
  # or for a release build:
  maturin build --release
  ```
  The wheel will be in the `target/wheels/` or `wheels/` directory.

## 3. Building and Publishing with uv

- To build the project (including the wheel):
  ```sh
  uv build
  ```
- To publish to PyPI:
  ```sh
  uv publish
  ```
  > **Note:** Before publishing, update the version in `pyproject.toml` and `Cargo.toml`.

## 4. Project Structure

- Rust code: `src/`
- Python stub/interface: `ebir_automation/`
- Tests: `tests/`

## License

MIT
