import { NextResponse } from "next/server";
import pool from "../../../lib/db.js";


export async function GET() {
  try {
    const result = await pool.query(
      "SELECT title, category, price, availability, rating, image_url FROM books LIMIT 50"
    );
    return NextResponse.json(result.rows);
  } catch (err) {
    return NextResponse.json(
      { error: err.message },
      { status: 500 }
    );
  }
}

