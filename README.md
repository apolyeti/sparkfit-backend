# Sparkfit - Backend

Backend of Sparkfit, run using Flask.

## 🚧 Still in Development

There will be an `instance/` directory in the root of the project. This directory will contain any sensitive configuration files that should not be committed into the remote repository.

You will also need to configure your own AWS credentials (for DynamoDB and S3) in order to run the backend locally. You can do this by following this [guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Unfortunately, the ML models are stored in a private S3 bucket, so you will not be able to access them. If you would like to test the backend locally, please reach out to me and I can provide you with the necessary files.

Many libraries used in this project do not fully support Apple Silicon, if at all. Both AI libraries, PyTorch and Tensorflow, run into large troubles with M1, M2, etc.. chips, so running this project on a machine with x86 architecture is advised.

Additionally, you wil not be able to use certain libraries without an Nvidia GPU, with its CUDA toolkit. The highest version of CUDA that PyTorch supports as of July 27th, 2024, is v12.4. Refer to the [PyTorch docs](https://pytorch.org/get-started/locally/) for more information and/or updates.

## Getting Started

### Prerequisites

- Python 3.8+
- conda
- pip (some libraries can only be downloaded by pip)
- AWS CLI configured with your credentials
- x86 machine with an Nvidia CUDA GPU (Libraries such as PyTorch, Transformers, and BitsAndBytes will not work without CUDA <=v12.4 support)

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
   conda env create -f environment.yml
   conda activate myenv
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
