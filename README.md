# Sparkfit - Backend

Backend of Sparkfit, run using Flask.

## 🚧 Still in Development

There will be an `instance/` directory in the root of the project. This directory will contain any sensitive configuration files that should not be committed into the remote repository.

You will also need to configure your own AWS credentials (for DynamoDB and S3) in order to run the backend locally. You can do this by following this [guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Unfortunately, the ML models are stored in a private S3 bucket, so you will not be able to access them. If you would like to test the backend locally, please reach out to me and I can provide you with the necessary files.

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- AWS CLI configured with your credentials

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/sparkfit-backend.git
   cd sparkfit-backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:

   ```bash
   flask --app flaskr run --debug
   ```

5. The server will be running at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Frontend

Here is the [frontend](https://github.com/apolyeti/sparkfit).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
