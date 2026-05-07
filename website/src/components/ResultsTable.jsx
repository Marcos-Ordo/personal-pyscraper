import { useState, useMemo, useEffect } from "react";

const SORT_KEYS = ["name", "price", "origin", "type"];

const formatPrice = (price) => {
  const num = typeof price === "number" ? price : parseFloat(price);
  return "$" + num.toLocaleString("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
};

function ProductModal({ item, onClose }) {
  useEffect(() => {
    const handler = (e) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose} aria-label="Close">✕</button>
        <span className={`type-badge type-${item.type?.toLowerCase()}`} style={{ marginBottom: "1rem", display: "inline-block" }}>
          {item.type}
        </span>
        <h2 className="modal-name">{item.name}</h2>
        <div className="modal-price">{formatPrice(item.price)}</div>
        <div className="modal-meta">
          <span className="modal-meta-label">Source</span>
          <span className="origin-badge">{item.origin}</span>
        </div>
      </div>
    </div>
  );
}

export default function ResultsTable({ results, loading, error, hasSearched }) {
  const [sortKey, setSortKey] = useState("price");
  const [sortAsc, setSortAsc] = useState(true);
  const [selected, setSelected] = useState(null);

  const frozen = useMemo(() => Object.freeze([...results]), [results]);

  const sorted = useMemo(() => {
    return [...frozen].sort((a, b) => {
      const av = a[sortKey];
      const bv = b[sortKey];
      if (typeof av === "number") return sortAsc ? av - bv : bv - av;
      return sortAsc
        ? String(av).localeCompare(String(bv))
        : String(bv).localeCompare(String(av));
    });
  }, [frozen, sortKey, sortAsc]);

  const handleSort = (key) => {
    if (key === sortKey) {
      setSortAsc((prev) => !prev);
    } else {
      setSortKey(key);
      setSortAsc(true);
    }
  };

  const arrow = (key) => {
    if (key !== sortKey) return <span className="sort-arrow muted">↕</span>;
    return <span className="sort-arrow">{sortAsc ? "↑" : "↓"}</span>;
  };

  if (loading) {
    return (
      <div className="results-state">
        <div className="big-spinner" aria-label="Loading results" />
        <p>Scraping… this may take a moment</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="results-state error">
        <span className="state-icon">✕</span>
        <p>Could not reach the server: {error}</p>
        <p className="hint">Make sure Flask is running on port 5000.</p>
      </div>
    );
  }

  if (!hasSearched) {
    return (
      <div className="results-state empty">
        <span className="state-icon dim">⬡</span>
        <p>Configure your search above and hit Search.</p>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="results-state empty">
        <span className="state-icon dim">∅</span>
        <p>No results found.</p>
      </div>
    );
  }

  return (
    <>
      {selected && <ProductModal item={selected} onClose={() => setSelected(null)} />}
      <div className="results-wrap">
        <p className="results-count">
          {results.length} result{results.length !== 1 ? "s" : ""}
          <span className="results-hint"> — click a row to expand</span>
        </p>
        <div className="table-scroll table-scroll-fixed">
          <table className="results-table">
            <thead>
              <tr>
                {SORT_KEYS.map((key) => (
                  <th key={key} onClick={() => handleSort(key)} className="sortable">
                    {key} {arrow(key)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sorted.map((item, i) => (
                <tr
                  key={item.id ?? i}
                  className="row-clickable"
                  onClick={() => setSelected(item)}
                >
                  <td className="cell-name">{item.name}</td>
                  <td className="cell-price">{formatPrice(item.price)}</td>
                  <td>
                    <span className="origin-badge">{item.origin}</span>
                  </td>
                  <td>
                    <span className={`type-badge type-${item.type?.toLowerCase()}`}>
                      {item.type}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
