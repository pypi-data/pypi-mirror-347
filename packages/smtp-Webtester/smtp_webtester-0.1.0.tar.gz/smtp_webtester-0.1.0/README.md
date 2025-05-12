# SMTP Tester

![PyPI](https://img.shields.io/pypi/v/smtp-tester?color=blue)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Mrv3n0m666/Smtp-Webtester/publish.yml?branch=main)
![License](https://img.shields.io/github/license/Mrv3n0m666/Smtp-Webtester)

A Flask-based web application to test SMTP server connections and send test emails. This tool is designed to help developers and system administrators verify SMTP server configurations with a user-friendly interface and AI-powered chat support.

## Overview

SMTP Tester provides:
- Testing of SMTP server connectivity with security options (None, SSL, TLS, Auto).
- Sending test emails to verify sender and recipient addresses.
- Real-time chat assistance powered by OpenAI.
- Email address validation before sending.
- Secure form submissions with CSRF protection.
- Configuration of sensitive settings via `.env` file.

This project is open-source under the MIT License and welcomes contributions from the community.

## Demo
SMTP Tester features a sleek, dark-themed interface with a form to input SMTP details and a live chat for troubleshooting. Run it locally to see it in action, or check the [Issues](https://github.com/Mrv3n0m666/Smtp-Webtester/issues) page for planned UI enhancements!

## Installation and Usage

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Mrv3n0m666/Smtp-Webtester.git
   cd Smtp-Webtester
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your OpenAI API key:
   ```text
   OPENAI_API_KEY=sk-proj-your-api-key
   ```
4. Run the application:
   ```bash
   python smtpWEBtester.py
   ```

### Usage
1. Open your browser and navigate to `http://localhost:5000`.
2. Fill in the SMTP server details:
   - **SMTP Host**: e.g., `smtp.example.com`
   - **Port**: Common ports are `465` (SSL) or `587` (TLS)
   - **Security**: Choose `None`, `SSL`, `TLS`, or `Auto`
   - **Username**: Your SMTP username (e.g., `your@email.com`)
   - **Password**: Your SMTP password or API key
   - **Mail From**: Sender email address
   - **Mail To**: Recipient email address
3. Click **Test SMTP** to send a test email.
4. Check the result message for success or error details.
5. Use the chat feature on the right to ask for assistance or troubleshooting tips.

### Notes
- Ensure your SMTP server supports the selected security protocol.
- Email addresses are validated to prevent errors.
- The form is protected against CSRF attacks.
- For production, configure a secure environment and disable debug mode (`debug=True`).

## Roadmap
We aim to make SMTP Tester more robust and feature-rich. Planned features include:
- Support for multiple recipients in a single test.
- Test history stored in a local database.
- Integration with alternative AI chat providers (e.g., xAI Grok).
- Automated tests with pytest.
- Deployment guides for platforms like Heroku or Docker.

Have an idea? Open an issue to discuss!

## Contributing
We love contributions! Whether you're fixing bugs, adding features, or improving docs, your help is welcome. See our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on how to get started. Check the [Issues](https://github.com/Mrv3n0m666/Smtp-Webtester/issues) page for tasks labeled `good first issue` or `help wanted`.

## License
MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements
- Thanks to the Flask and OpenAI communities for their amazing tools.
- Shoutout to future contributors for helping improve SMTP Tester!

## Contact
For questions, suggestions, or bug reports, please [open an issue](https://github.com/Mrv3n0m666/Smtp-Webtester/issues) or contact [Mrv3n0m666](mailto:mrv3n0m666@example.com).