"use client";

import { useEffect, useState } from "react";

export default function Page() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    fetch("/api/books")
      .then(res => res.json())
      .then(data => {
        setBooks(Array.isArray(data.data) ? data.data : []);
      })
      .catch(() => setBooks([]));
  }, []);

  return (
    <div>
      <h1>Books</h1>

      {books.length === 0 && <p>No books found</p>}

      {books.map((book: any) => (
        <div key={book.id}>
          <strong>{book.title}</strong>
        </div>
      ))}
    </div>
  );
}

