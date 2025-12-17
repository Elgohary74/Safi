# Safi
**Safi** is a web-based utility designed to simplify and automate shared expense calculations for small groups.

The application is built to eliminate the confusion and manual effort involved when groups of people (like roommates, friends, or coworkers) share costs. Users log expenses they have paid for the group, and the application calculates the most efficient way to settle all debts so that each member has contributed their equal share.

The primary goal is to provide a clear, accurate, and simple solution that prevents financial disagreements and makes living or working together easier. The key benefit is transforming a complex calculation mess into a simple clear set of who-pays-whom instructions.


## Prerequisites

Before you start, ensure you have the following installed:

- **WSL** (for windows)
- **Docker**
- **MiniConda**
- **Python 3.13+**
- **black formatter**
- **flake8**
- **isort**

## Quick Start (Onboarding)

Follow these steps to get the app running on your local machine

### 1. Clone the Repository

```bash
$ git clone https://github.com/OsamaAshraf01/Safi.git
$ cd Safi
```

### 2. Configure Environment

**Create your Secret `.env` file:**

```bash
$ cp .env.example .env
```

_Action:_ Open `.env` and fill in any missing secrets (ask the Team Lead for keys).

### 3. Setup the environment
Download and install MiniConda from [here](https://www.anaconda.com/docs/main)

Create a new environment using the following command:

```bash
$ conda create -n safi python=3.13
```

Activate the environment:

```bash
$ conda activate safi
```

Install the requirements:

```bash
$ pip install -r requirements.txt
```
### 4. Install Pre-Commit Hooks

Install hooks

```bash
$ pre-commit install
```

_Now, Git will automatically fix your formatting when you commit code._

### 5. Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```

- Update `.env` with your credentials.

```bash
$ cd docker
$ sudo docker compose up -d
```

- **Backend:** <http://localhost:5000>

## Development Workflow

### Checking Logs
Check your terminal for Flask logs when running the container.
<br>Or access through the terminal
```bash
$ docker logs safi_dev
```
### Running Tests

We run tests **inside** the Docker container to match the environment using the following commands:

- Run all tests
```bash
$ docker-compose -f docker/docker-compose.yml run --rm test_runner
```

- Run only unit tests
```bash
$ docker-compose -f docker/docker-compose.yml run --rm test_runner pytest tests/unit
```

### Installing New Dependencies

If `requirements.txt` gets updated you need to Rebuild the container as follows:
```bash
$ docker-compose up -d --build
```
## Extensions for VSCode users
if you use vscode for development, you may need to download the following extensions:
- **GitHub Actions**
- **black formatter**
- **flake8**
- **isort**
