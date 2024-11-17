Here’s a clear and professional `README.md` for your project:

---

# Full-Stack Application

This project is a full-stack application consisting of a **FastAPI backend** and a **Next.js frontend**.

## Features

- **Backend**: Built with FastAPI and SQLAlchemy for handling authentication and data.
- **Frontend**: Built with Next.js (TypeScript) for an interactive and responsive user interface.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python** (version 3.9 or higher)
- **PostgreSQL** (for the database)
- **Node.js** (version 18 or higher) and `pnpm`
- **pip** (Python package manager)

---

## Setup Instructions

### 1. Configure Environment Variables

#### Backend

Set up the following environment variables in `/backend/.env`:

```env
SQLALCHEMY_DATABASE_URL=your_postgres_connection_url
ALLOW_ORIGINS=your_frontend_url
```

#### Frontend

If your frontend URL needs to be dynamic, you can configure it using `.env.local` in `/frontend`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

### 2. Run the Backend

1. Navigate to the backend folder:

   ```bash
   cd backend
   ```

2. Install required Python packages:

   ```bash
   pip install fastapi sqlalchemy psycopg2-binary uvicorn
   ```

3. Seed the database:

   ```bash
   python seeder.py
   ```

4. Start the backend server:
   ```bash
   uvicorn auth:app --reload
   ```

By default, the backend will run at `http://localhost:8000`.

---

### 3. Run the Frontend

1. Navigate to the frontend folder:

   ```bash
   cd frontend
   ```

2. Install frontend dependencies:

   ```bash
   pnpm install
   ```

3. Start the development server:
   ```bash
   pnpm dev
   ```

By default, the frontend will run at `http://localhost:3000`.

---

## Directory Structure

```
├── backend/
│   ├── database/          # Contains database models and setup
│   ├── seeder.py          # Seeds the database with initial data
│   ├── auth.py            # Backend entry point for FastAPI
│   └── .env               # Backend environment variables
├── frontend/
│   ├── public/            # Static files
│   ├── pages/             # Next.js routes
│   ├── components/        # Reusable UI components
│   └── .env.local         # Frontend environment variables
└── README.md              # Project documentation
```

---

## Development Tips

- Ensure the backend and frontend URLs are correctly set in their respective `.env` files.
- If you encounter CORS errors, verify the `ALLOW_ORIGINS` setting in `backend/.env`.

---

## License

This project is licensed under the MIT License.

---
