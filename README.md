## Run Backend

Setup database first on /backend/database
SQLALCHEMY_DATABASE_URL={ur url postgres}
make sure ur url frontend is appropriate on main.py
allow_origins={ur url frontend}

cd /backend
pip install fastapi sqlalchemy psycopg2-binary uvicorn
python seeder.py
uvicorn auth:app --reload

## Run Frontend

cd ..
cd /frontend
pnpm install
pnpm dev
