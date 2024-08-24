# FASTAPIFORGPT
PDF-QA FastAPI Application
Overview
This FastAPI application enables users to upload PDF files and ask questions about their content. The application uses a Retrieval-Augmented Generation (RAG) system built with LangChain to process the PDFs and generate accurate answers based on the provided content. The system leverages the Ollama model for language understanding and FAISS for efficient vector-based retrieval.

Features
Dynamic PDF Processing: Upload PDF files and retrieve answers to questions based on the document's content.
LLM Integration: Uses the Ollama language model for generating human-like responses.
Efficient Search: Implements FAISS vector stores for fast and accurate document retrieval.
Cross-Origin Resource Sharing (CORS): Enabled for broader API accessibility.
Installation
Prerequisites
Ensure you have Python 3.8+ installed on your machine. You will also need pip for managing Python packages.

Step 1: Clone the Repository
bash
Copy code
git clone https://github.com/your-username/pdf-qa-fastapi.git
cd pdf-qa-fastapi
Step 2: Install Required Packages
bash
Copy code
pip install -r requirements.txt
Alternatively, manually install the dependencies:

bash
Copy code
pip install fastapi uvicorn langchain langchain-community pypdf pydantic sentence-transformers
Step 3: Run the Application
Start the FastAPI application using Uvicorn:

bash
Copy code
uvicorn api_gateway:app --reload
The API will be available at http://127.0.0.1:8000.

API Endpoints
1. POST /ask
Upload a PDF and ask a question.

Request:

Question (str): The question you want to ask.
PDF (file): The PDF file containing the content to be queried.
Response:

Question (str): The question submitted.
Answer (str): The generated answer based on the PDF content.
Example request using curl:

bash
Copy code
curl -X POST "http://127.0.0.1:8000/ask" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "question=What is the main topic of this document?" \
-F "pdf=@path/to/your/document.pdf"
2. GET /health
Check the health status of the API.

Response:
status (str): Returns "API is running successfully."
Deployment on AWS
Step 1: Create an AWS Account and Set Up CLI
Sign up for an AWS account.

Install and configure the AWS CLI:

bash
Copy code
pip install awscli
aws configure
Enter your AWS Access Key, Secret Key, region, and output format when prompted.

Step 2: Set Up an EC2 Instance
Launch an EC2 instance:

Choose Amazon Linux 2 AMI as your instance.
Select an instance type (e.g., t2.micro for free tier).
Configure instance details, add storage, and configure security groups (allow HTTP, HTTPS, and SSH).
Review and launch the instance.
Connect to your EC2 instance using SSH:

bash
Copy code
ssh -i "your-key.pem" ec2-user@your-ec2-public-ip
Step 3: Install Dependencies on EC2
Update the package index and install Python 3:

bash
Copy code
sudo yum update -y
sudo yum install python3 -y
Install Git and clone your repository:

bash
Copy code
sudo yum install git -y
git clone https://github.com/your-username/pdf-qa-fastapi.git
cd pdf-qa-fastapi
Install the Python packages:

bash
Copy code
pip3 install -r requirements.txt
Step 4: Run the Application on EC2
Start the FastAPI server using Uvicorn:

bash
Copy code
uvicorn api_gateway:app --host 0.0.0.0 --port 80
Your API will be accessible at http://your-ec2-public-ip/.

Step 5: Set Up a Reverse Proxy (Optional)
To improve security and scalability, you can set up a reverse proxy using NGINX:

Install NGINX:

bash
Copy code
sudo amazon-linux-extras install nginx1.12
Configure NGINX to forward requests to Uvicorn:

Edit the /etc/nginx/nginx.conf file:

bash
Copy code
sudo nano /etc/nginx/nginx.conf
Add the following server block:

nginx
Copy code
server {
    listen 80;
    server_name your-ec2-public-ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
Restart NGINX:

bash
Copy code
sudo systemctl restart nginx
Step 6: Test Your Deployment
You should now be able to access your FastAPI application via the public IP of your EC2 instance.

Contributing
Feel free to submit pull requests or open issues to improve this project. Contributions are always welcome!

License
This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to customize the instructions and replace placeholders like your-username, your-key.pem, and your-ec2-public-ip with your actual details.
