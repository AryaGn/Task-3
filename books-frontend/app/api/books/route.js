import pool from "@/lib/db";

export async function GET() {
  console.log("DATABASE_URL =", process.env.DATABASE_URL);

  try {
    const result = await pool.query(
      "SELECT id, title FROM books ORDER BY id DESC"
    );
    return Response.json({ data: result.rows });
  } catch (error) {
    console.error("DB ERROR:", error.message);
    return Response.json(
      { data: [], error: error.message },
      { status: 500 }
    );
  }
}

