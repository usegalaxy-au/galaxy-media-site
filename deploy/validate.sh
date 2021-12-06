# Validate that build context is sufficient before running build

if [ ! -f .env ]; then
  echo "Please set environment variables in a .env file."
  echo "See .env.sample for required variables."
  exit 1
fi
