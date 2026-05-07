import { useState } from "react";

const WEBSITES = ["compragamer", "maximus"];
const CATEGORIES = [
  { id: "cpu", label: "CPU" },
  { id: "gpu", label: "GPU" },
  { id: null, label: "General" },
];

export default function SearchPanel({ onSearch, loading }) {
  const [selectedWebsites, setSelectedWebsites] = useState(["compragamer"]);
  const [category, setCategory] = useState("cpu");
  const [query, setQuery] = useState("");
  const [useNameFilter, setUseNameFilter] = useState(false);
  const [useMinPrice, setUseMinPrice] = useState(false);
  const [useMaxPrice, setUseMaxPrice] = useState(false);
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");

  const toggleWebsite = (site) => {
    setSelectedWebsites((prev) =>
      prev.includes(site)
        ? prev.length === 1 ? prev : prev.filter((s) => s !== site)
        : [...prev, site]
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedWebsites.length === 0) return;

    const flags = [];
    const isGeneral = category === null;

    if (isGeneral) {
      flags.push("msg");
    } else {
      if (useNameFilter && query) flags.push("name");
      if (useMinPrice && minPrice !== "") flags.push("mp");
      if (useMaxPrice && maxPrice !== "") flags.push("Mp");
    }

    onSearch({
      websites: selectedWebsites,
      category: isGeneral ? null : category,
      flags,
      query,
      minPrice,
      maxPrice,
    });
  };

  const isGeneral = category === null;

  return (
    <form className="search-panel" onSubmit={handleSubmit}>

      <div className="panel-section">
        <p className="section-label">Websites</p>
        <div className="toggle-group">
          {WEBSITES.map((site) => (
            <button
              key={site}
              type="button"
              className={`toggle-btn ${selectedWebsites.includes(site) ? "active" : ""}`}
              onClick={() => toggleWebsite(site)}
            >
              {site}
            </button>
          ))}
        </div>
      </div>

      <div className="panel-section">
        <p className="section-label">Category</p>
        <div className="toggle-group">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id ?? "general"}
              type="button"
              className={`toggle-btn ${category === cat.id ? "active" : ""}`}
              onClick={() => setCategory(cat.id)}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      <div className="panel-section">
        <p className="section-label">Search query</p>
        <input
          className="text-input"
          type="text"
          placeholder={isGeneral ? "Search anything…" : "e.g. Ryzen 5 5600"}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {!isGeneral && (
        <div className="panel-section">
          <p className="section-label">Filters</p>
          <div className="filters-grid">

            <label className="filter-row">
              <input
                type="checkbox"
                checked={useNameFilter}
                onChange={(e) => setUseNameFilter(e.target.checked)}
              />
              <span>Filter by name</span>
            </label>

            <label className="filter-row">
              <input
                type="checkbox"
                checked={useMinPrice}
                onChange={(e) => setUseMinPrice(e.target.checked)}
              />
              <span>Min price</span>
              {useMinPrice && (
                <input
                  className="price-input"
                  type="number"
                  min="0"
                  step="0.01"
                  placeholder="0.00"
                  value={minPrice}
                  onChange={(e) => setMinPrice(e.target.value)}
                />
              )}
            </label>

            <label className="filter-row">
              <input
                type="checkbox"
                checked={useMaxPrice}
                onChange={(e) => setUseMaxPrice(e.target.checked)}
              />
              <span>Max price</span>
              {useMaxPrice && (
                <input
                  className="price-input"
                  type="number"
                  min="0"
                  step="0.01"
                  placeholder="0.00"
                  value={maxPrice}
                  onChange={(e) => setMaxPrice(e.target.value)}
                />
              )}
            </label>

          </div>
        </div>
      )}

      <button
        className="search-btn"
        type="submit"
        disabled={loading || selectedWebsites.length === 0}
      >
        {loading ? (
          <span className="spinner" aria-label="Searching…" />
        ) : (
          "Search"
        )}
      </button>

    </form>
  );
}
