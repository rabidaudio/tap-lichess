# tap-lichess

`tap-lichess` is a Singer tap for [Lichess](https://lichess.org).

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

Currently supported:

- Users
- Games

There are plenty more interesting data sources available from [the API](https://lichess.org/api). PRs accepted if this tap doesn't include what you need.

Install from GitHub:

```bash
pipx install git+https://github.com/ORG_NAME/tap-lichess.git@main
```

## Configuration

### Accepted Config Options

```js
{
  "usernames": ["VincentKeymer2004"], // A list of player's games to download
  "auth_token": "<personal access token>", // optional
}
```

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-lichess --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

You can generate a personal access token from your [account settings](https://lichess.org/account/oauth/token). Authentication is not required, but authenticating will increase rate limits. `preference:read` is the only required permission.

## Usage

You can easily run `tap-lichess` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-lichess --version
tap-lichess --help
tap-lichess --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_lichess/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-lichess` CLI interface directly using `poetry run`:

```bash
poetry run tap-lichess --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-lichess
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-lichess --version
# OR run a test `elt` pipeline:
meltano elt tap-lichess target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
