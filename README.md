# activistChatbot

activistChatbot is an AI-powered chatbot designed to support activists by providing information, resources, and conversation around social justice, policy advocacy, and community organizing. The project leverages modern natural language processing techniques to facilitate insightful and supportive dialogue for those engaged in activism.

## Features

- **Automatic Event Scraping:** Scrapes a typo3 website for events
- **Regular reminder on future events:** Get regular reminders on events.

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- **Python:** Version 3.13 or later.
- **uv:** A Python package manager: [docs.astral.sh/uv](https://docs.astral.sh/uv/)
- **signal-rest-api:** A running and configured instance of [bbernhard/signal-rest-api](https://github.com/bbernhard/signal-cli-rest-api/)

### Installation

Create and activate a virtual environment and install dependencies:

```bash
uv sync
source .venv/bin/activate
```

To install dev dependencies, run:

```bash
uv sync --dev
```

## Configuration

The application reads the configuration from environment variables or a `.env` file.
To get started copy the `example.env` into `.env` and update the settings according to your needs.

## Usage

To start the chatbot locally, run:

```bash
activistChatbot
```

It will automatically listen to message from either allowed groups or contacts. These can be configured with the env variables `ACTIVIST_BOT_ALLOWED_GROUPS` and `ACTIVIST_BOT_ALLOWED_CONTACTS` both are lists of strings.

### Commands

Commands in this chatbot are generally prefixed with a . (dot). This makes it convenient for users, as it avoids the need to switch to special characters on mobile keyboards.

The help command gives an overview of all available commands.

Example usage:

```text
.help
.abo
.event
```

## Deployment

### Build the container image

From the repository root, run the following command to build the Docker image:

```bash
podman build -t activist-chatbot .
```

### Running the container

After building the image, run the container with the following command:

```bash
podman run -d --env-file .env activist-chatbot
```

## Contributing

Contributions are welcome! If you have ideas for improvements or additional features, your PR is highly welcome!

- Please configure your editor to use respect the `.editorconfig`.
- Please use `pre-commit`, this will automatically lint and format all files. See [pre-commit](https://pre-commit.com/)

For major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the GPL-3.0 license. See the [LICENSE file](LICENSE) for details.
