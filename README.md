# Sparkfit Backend

Backend of Sparkfit, ran using Flask.

## Local Development

There will be an `instance/` directory in the root of the project. This directory will contain any sensitive configuration files that should not be commited into the remote repository.

You will also need to configure your own AWS credentials (for Dynamo and S3) in order to run the backend locally. You can do this by following this [guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Unfortunately, the ML models are stored in a private S3 bucket, so you will not be able to access them. If you would like to test the backend locally, please reach out to me and I can provide you with the necessary files.

### Frontend

Here is the [frontend](https://github.com/apolyeti/sparkfit)
