./run_backend.sh
if [ $? -ne 0 ]; then
    echo "Failed to run backend"
    exit 1
fi

echo "Backend is running, starting frontend"

cd client && npm run dev
