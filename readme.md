# project setup 

1. create a venv in the root of the project 
   ```
   python -m venv venv
   ```
2. install the package (all the package and their version are mentioned)
   ```
   pip install -r truereadapi\lamdareq.txt
   ```
3. to run the project go inside the project 
   ```
   cd .\truereadapi\
   ```
4. run the project
   ```
   python manage.py runserver
   ```

# This project is hosted in lambda through aws sam.
The image will be built locally and pushed to ecr . to build the image you need to have to docker open in background

1. to build sam in local
   ```
   sam build
   ```
2. test the image locally 
   ```
   sam local start-api   # to run on the local systen 
   sam local start-api --host 0.0.0.0 --port 8000  # to run over network
   ```
3. push to lambda(this command will pushh the image to ECR). This uses api creditails in the local system . so make sure to change samconfig.toml  with profile variable to system profile that has permission to push the image to ECR.
   ```
   sam deploy
   ```

## 🚀 Prerequisites for ECR Push

Before pushing your Docker image to Amazon ECR, ensure your local environment is correctly configured.

### 1. AWS IAM User Configuration
You must have an AWS IAM user configured on your system with a valid profile and credentials. This user must have the necessary permissions (e.g., `AmazonEC2ContainerRegistryPowerUser`) to push images to the ECR repository.

To check the existing profiles on your system via Command Prompt (CMD) or Terminal, run:
```bash
aws configure list-profiles
```

## 🚀 Steps for final deployment

📦 Step 1: Update the Lambda Function Image
Navigate to the AWS Lambda Console and select your specific function.

   1. Go to the Image tab (or the "Code" tab).
   2. Click Deploy new image.
   3. Click Browse images and select the ECR repository.
   4. Select the latest image from the list and click Save.

🧪 Step 2: Validation
   1. Wait for the function update to complete (status will change to "Successful").
   2. Test the changes using the Function URL.
   Note: At this stage, the prod alias is still pointing to the previous version, so your production environment remains safe while you test.

🔢 Step 3: Versioning
   1. To use aliases, you must publish a specific immutable version of your code.
   2. Go to the Versions tab.
   3. Click Publish new version.
   Description: Enter a name or number (e.g., v1.0.5 or Refactored DB queries).
   Click Publish.

🏁 Step 4: Promote to Production (Alias Swap)
   1. This is the final step to point your production traffic to the new code.
   2. Go to the Aliases tab.
   3. Select the prod alias and click Edit.
   4. In the Version dropdown, select the version number you just published in Step 3.
   5. Weighted Alias: Ensure this is set to None (unless you are performing a canary deployment).
   6. Click Save.

Success: Your new image is now live in production!