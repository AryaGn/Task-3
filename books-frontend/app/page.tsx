'use client';

import { useEffect, useState } from 'react';

export default function Home() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    fetch('/api/books')
      .then(res => res.json())
      .then(data => setBooks(data));
  }, []);

  return (
    <main style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>📚 Books to Scrape</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '20px' }}>
        {books.map((book: any, index) => (
          <div
            key={index}
            style={{
              border: '1px solid #ddd',
              padding: '10px',
              borderRadius: '6px',
              background: '#fff'
            }}
          >
            <img
              src={book.image_url}
              alt={book.title}
              style={{ width: '100%', height: '250px', objectFit: 'cover' }}
            />
            <h3 style={{ fontSize: '16px' }}>{book.title}</h3>
            <p>Category: {book.category}</p>
            <p>Price: £{book.price}</p>
            <p>Rating: ⭐ {book.rating}</p>
            <p>{book.availability}</p>
          </div>
        ))}
      </div>
    </main>
  );
}

