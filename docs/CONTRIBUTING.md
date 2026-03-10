# Contributing to Rack‑Planner

Thank you for your interest in contributing!  Rack‑Planner relies on the community to add new devices, fix bugs and build the software that will make this mini‑rack planner a reality.  Whether you are a developer, designer, documentation writer or homelab enthusiast, your help is welcome.

## How to contribute

### 1 Get the code

Fork the repository on GitHub and clone your fork locally:

```sh
git clone https://github.com/<your‑username>/rack‑planner.git
cd rack‑planner
```

### 2 Create a branch

Name your branch descriptively.  For example, if you are adding a new device definition:

```sh
git checkout -b add‑device‑edge‑router
```

### 3 Make changes

* **For code changes**, follow the existing architecture described in [`docs/architecture.md`](docs/architecture.md).  Use Python ≥ 3.10 for backend development and adhere to [PEP 8](https://peps.python.org/pep-0008/) coding style.  Use [Black](https://black.readthedocs.io) and [isort](https://pycqa.github.io/isort/) to format code.
* **For frontend changes**, use [React](https://react.dev/) with hooks and functional components.  Use [TypeScript](https://www.typescriptlang.org/) for type safety.  Ensure components are accessible and responsive.
* **For device definitions**, add new JSON objects to `data/devices/`.  Follow the schema documented in [`docs/architecture.md`](docs/architecture.md#31-data-model).  Use SI units (millimetres, kilograms, watts) and provide as much detail as possible.
* **For documentation**, edit the Markdown files.  Keep sentences short and use clear headings and lists.  Include citations using the notation `【source†Lstart-Lend】` when referencing external sources.

### 4 Run tests and linting

Before committing, run the test suite and linters:

```sh
pip install -r requirements-dev.txt
pytest
black --check .
isort --check .
```

### 5 Commit and push

Use informative commit messages.  Follow the conventional commit style (`feat:`, `fix:`, `docs:`, `chore:`, etc.).

```sh
git add .
git commit -m "feat: add 24‑port PoE switch device definition"
git push origin add‑device‑edge‑router
```

### 6 Open a pull request

Go to your fork on GitHub and open a pull request (PR) against the `main` branch of the `xnobE0311/rack-planner` repository.  Describe what your change does and why.  Link to any relevant issues.

### 7 Code review and discussion

Project maintainers will review your PR and may request changes.  Be responsive to feedback and feel free to ask questions.  Larger contributions may require design discussions in the issue tracker before coding begins.

## Reporting issues

If you find a bug or have an idea for a new feature, please open an issue on GitHub.  Provide as much information as possible: steps to reproduce, expected vs. actual behaviour, screenshots or logs, and environment details.  For feature requests, explain the use case and any relevant constraints.

## Code of conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) to ensure a welcoming and inclusive environment.  By participating in this project you agree to uphold these standards.  Instances of abusive or harassing behaviour may be reported by opening a confidentiality‑marked issue.

## Licensing and copyright

All contributions are accepted under the terms of the MIT Licence (see [`LICENSE`](LICENSE)).  By submitting a pull request, you agree that your work may be distributed under that licence.

## A note on sustainability

Please consider the environmental impact of your contributions.  Reuse existing models and libraries where possible instead of duplicating functionality.  Design printable parts to minimise material usage.  When documenting hardware devices, include details about energy consumption so that users can make informed decisions.

We look forward to your contributions – together we can build a comprehensive and sustainable 10‑inch rack planner!