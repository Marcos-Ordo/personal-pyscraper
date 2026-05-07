import { useState, useCallback } from "react";
import SearchPanel from "./components/SearchPanel";
import ResultsTable from "./components/ResultsTable";
import "./App.css";

export default function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = useCallback(async (params) => {
    setLoading(true);
    setError(null);
    setHasSearched(true);

    const { websites, category, flags, query, minPrice, maxPrice } = params;

    const searchParams = new URLSearchParams();
    websites.forEach((w) => searchParams.append("websites", w));
    flags.forEach((f) => searchParams.append("flags", f));
    if (query) searchParams.set("query", query);
    if (flags.includes("mp") && minPrice !== "") searchParams.set("mp", minPrice);
    if (flags.includes("Mp") && maxPrice !== "") searchParams.set("Mp", maxPrice);

    const endpoint = category
      ? `http://localhost:5000/products/${category}`
      : `http://localhost:5000/products`;

    try {
      const res = await fetch(`${endpoint}?${searchParams.toString()}`);
      if (!res.ok) throw new Error(`Server responded with ${res.status}`);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-inner">
          <span className="header-logo">⬡</span>
          <h1 className="header-title">pyscraper</h1>
          <span className="header-sub">hardware price tracker</span>
        </div>
      </header>

      <main className="app-main">
        <SearchPanel onSearch={handleSearch} loading={loading} />
        <ResultsTable
          results={results}
          loading={loading}
          error={error}
          hasSearched={hasSearched}
        />
      </main>
    </div>
  );
}
