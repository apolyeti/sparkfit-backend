# Sparkfit - Backend

Backend of Sparkfit, run using Flask.

https://github.com/user-attachments/assets/4684b00a-f9d5-4059-b163-9dbef57832cb

## Tech Stack
<img height="50" src="https://user-images.githubusercontent.com/25181517/183890598-19a0ac2d-e88a-4005-a8df-1ee36782fde1.png"> <img height="50" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png"> 
<img height="50" src=https://github.com/marwin1991/profile-technology-icons/assets/136815194/5f8c622c-c217-4649-b0a9-7e0ee24bd704>
<img height="50" src="https://user-images.githubusercontent.com/25181517/183423775-2276e25d-d43d-4e58-890b-edbc88e915f7.png">
<img height="50" src="https://user-images.githubusercontent.com/25181517/183568594-85e280a7-0d7e-4d1a-9028-c8c2209e073c.png">
<img height="50" src="https://user-images.githubusercontent.com/25181517/223639822-2a01e63a-a7f9-4a39-8930-61431541bc06.png">
<img height="50" src="https://user-images.githubusercontent.com/25181517/183896132-54262f2e-6d98-41e3-8888-e40ab5a17326.png">
<img height="50" src="https://user-images.githubusercontent.com/25181517/202896760-337261ed-ee92-4979-84c4-d4b829c7355d.png"> 
<img src="https://skillicons.dev/icons?i=dynamodb" height="50">
<img src="https://seeklogo.com/images/A/aws-cloudfront-logo-D475098A98-seeklogo.com.png" height="50">
<img src="https://authjs.dev/img/etc/logo-sm.webp" height="50"/>
<img src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.png" height="50">
<img src="https://avatars.githubusercontent.com/u/132372032?s=200&v=4" height="50"/>
<img height="50" src="https://user-images.githubusercontent.com/25181517/117207330-263ba280-adf4-11eb-9b97-0ac5b40bc3be.png">


## 🚧 Not deployed yet

There will be an `instance/` directory in the root of the project. This directory will contain any sensitive configuration files that should not be committed into the remote repository.

Unfortunately, the ML models are stored in a private S3 bucket, so you will not be able to access them. If you would like to test the backend locally, please reach out to me and I can provide you with the necessary files.

You will also need to configure your own AWS credentials (for DynamoDB and S3) in order to run the backend locally. You can do this by following this [guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Many libraries used in this project do not fully support Apple Silicon, if at all. Both AI libraries, PyTorch and Tensorflow, run into large troubles with M1, M2, etc.. chips, so running this project on a machine with x86 architecture is advised.

Additionally, you will not be able to use certain libraries without an Nvidia GPU, with its CUDA toolkit. The highest version of CUDA that PyTorch supports as of July 27th, 2024, is v12.4. Refer to the [PyTorch docs](https://pytorch.org/get-started/locally/) for more information and/or updates.

The Sparkfit LLM is stored on the HuggingFace repository, so you will need to configure your credentials for it as well. To access the Sparkfit LLM, you will need to request access, and you will need to use your HuggingFace token when loading the model using the Transformers library.

Note: To use this LLM, your machine must have a NVIDIA GPU with CUDA <=v12.4 support for quantization. This essentially maps high precision values to lower precision values (ex: high precision datatypes to say 8bit ints) in order to mitigate memory and computation costs of such a large and costly model.

You may read more about quantization [here](https://huggingface.co/docs/transformers/en/main_classes/quantization)

If you do not have accees to a CUDA GPU, you may have to use a cloud service such as AWS Sagemaker and use their GPUs.

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
