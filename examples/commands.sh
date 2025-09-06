bash
# Flask (hello world)
python -m autodeploy.cli "Deploy Flask on AWS" \
  --repo https://github.com/Arvo-AI/hello_world \
  --region us-west-2

# Node app from ZIP
python -m autodeploy.cli "Node on AWS" --zip_path ./myapp.zip --region us-west-2

# Run API server
uvicorn autodeploy.api:app --port 8080
