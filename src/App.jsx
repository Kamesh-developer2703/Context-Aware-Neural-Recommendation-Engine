import React, { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

const DEFAULT_CUSTOMER =
  "00000dbacae5abe5e23885899a1fa44253a17956c6d1c3d25f88aa139fdfc657";

const DEFAULT_ARTICLE = 108775051;

function App() {
  const [customerId, setCustomerId] = useState(DEFAULT_CUSTOMER);
  const [searchCustomerId, setSearchCustomerId] =
    useState(DEFAULT_CUSTOMER);

  const [articleId, setArticleId] =
    useState(DEFAULT_ARTICLE);

  const [recommendations, setRecommendations] = useState([]);
  const [trending, setTrending] = useState([]);
  const [similar, setSimilar] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [recent, setRecent] = useState([]);
  const [feedback, setFeedback] = useState([]);

  const [health, setHealth] = useState(null);

  const [loadingRecommendations, setLoadingRecommendations] =
    useState(false);

  const [loadingSimilar, setLoadingSimilar] =
    useState(false);

  const [loadingTrending, setLoadingTrending] =
    useState(false);

  const [message, setMessage] = useState("");

  const [error, setError] = useState("");

  // =========================================================
  // Generic API helper
  // =========================================================

  const apiRequest = async (url, options = {}) => {
    const response = await fetch(`${API_BASE}${url}`, options);

    if (!response.ok) {
      throw new Error(
        `API request failed: ${response.status}`
      );
    }

    return response.json();
  };

  // =========================================================
  // Health
  // =========================================================

  const checkHealth = async () => {
    try {
      const data = await apiRequest("/health");
      setHealth(data);
    } catch (err) {
      setHealth(null);
    }
  };

  // =========================================================
  // Personalized Recommendations
  // =========================================================

  const loadRecommendations = async (
    id = customerId
  ) => {
    if (!id.trim()) {
      setError("Please enter a customer ID.");
      return;
    }

    setLoadingRecommendations(true);
    setError("");

    try {
      const data = await apiRequest(
        `/personalized/${encodeURIComponent(id)}?limit=10`
      );

      if (data.status === "success") {
        setRecommendations(data.recommendations || []);
        setCustomerId(id);
        setMessage("Personalized recommendations loaded.");
      } else {
        setRecommendations([]);
        setError(
          data.message ||
            "No personalized recommendations found."
        );
      }
    } catch (err) {
      console.error(err);
      setRecommendations([]);
      setError(
        "Unable to connect to the recommendation API."
      );
    } finally {
      setLoadingRecommendations(false);
    }
  };

  // =========================================================
  // Trending
  // =========================================================

  const loadTrending = async () => {
    setLoadingTrending(true);

    try {
      const data = await apiRequest(
        "/trending?limit=10"
      );

      if (data.status === "success") {
        setTrending(data.trending || []);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingTrending(false);
    }
  };

  // =========================================================
  // Similar Articles
  // =========================================================

  const loadSimilar = async (
    id = articleId
  ) => {
    if (!id) {
      setError("Please enter an article ID.");
      return;
    }

    setLoadingSimilar(true);
    setError("");

    try {
      const data = await apiRequest(
        `/similar/${id}?limit=10`
      );

      if (data.status === "success") {
        setSimilar(data.similar || []);
        setMessage(
          `Similar articles loaded for ${id}.`
        );
      } else {
        setSimilar([]);
        setError(
          data.message || "Article not found."
        );
      }
    } catch (err) {
      console.error(err);
      setSimilar([]);
      setError(
        "Unable to load similar articles."
      );
    } finally {
      setLoadingSimilar(false);
    }
  };

  // =========================================================
  // Favorites
  // =========================================================

  const loadFavorites = async (
    id = customerId
  ) => {
    try {
      const data = await apiRequest(
        `/favorites/${encodeURIComponent(id)}`
      );

      setFavorites(data.favorites || []);
    } catch (err) {
      console.error(err);
    }
  };

  // =========================================================
  // Recently Viewed
  // =========================================================

  const loadRecent = async (
    id = customerId
  ) => {
    try {
      const data = await apiRequest(
        `/recent/${encodeURIComponent(id)}?limit=10`
      );

      setRecent(data.recent || []);
    } catch (err) {
      console.error(err);
    }
  };

  // =========================================================
  // Feedback
  // =========================================================

  const loadFeedback = async (
    id = customerId
  ) => {
    try {
      const data = await apiRequest(
        `/feedback/${encodeURIComponent(id)}`
      );

      setFeedback(data.feedback || []);
    } catch (err) {
      console.error(err);
    }
  };

  // =========================================================
  // Add Favorite
  // =========================================================

  const addFavorite = async (id) => {
    try {
      const data = await apiRequest(
        `/favorites/${encodeURIComponent(
          customerId
        )}/${id}`,
        {
          method: "POST"
        }
      );

      setMessage(
        data.message || "Article added to favorites."
      );

      await loadFavorites();
    } catch (err) {
      console.error(err);
      setError("Unable to add favorite.");
    }
  };

  // =========================================================
  // Remove Favorite
  // =========================================================

  const removeFavorite = async (id) => {
    try {
      const data = await apiRequest(
        `/favorites/${encodeURIComponent(
          customerId
        )}/${id}`,
        {
          method: "DELETE"
        }
      );

      setMessage(
        data.message || "Article removed from favorites."
      );

      await loadFavorites();
    } catch (err) {
      console.error(err);
      setError("Unable to remove favorite.");
    }
  };

  // =========================================================
  // Add Recently Viewed
  // =========================================================

  const addRecentlyViewed = async (id) => {
    try {
      const data = await apiRequest(
        `/recent/${encodeURIComponent(
          customerId
        )}/${id}`,
        {
          method: "POST"
        }
      );

      setMessage(
        data.message ||
          "Article added to recently viewed."
      );

      await loadRecent();
    } catch (err) {
      console.error(err);
      setError(
        "Unable to update recently viewed."
      );
    }
  };

  // =========================================================
  // Feedback
  // =========================================================

  const sendFeedback = async (
    id,
    type
  ) => {
    try {
      const data = await apiRequest(
        `/feedback/${encodeURIComponent(
          customerId
        )}/${id}?feedback=${type}`,
        {
          method: "POST"
        }
      );

      setMessage(
        data.message ||
          `Feedback "${type}" submitted.`
      );

      await loadFeedback();
    } catch (err) {
      console.error(err);
      setError("Unable to submit feedback.");
    }
  };

  // =========================================================
  // Initial Load
  // =========================================================

  useEffect(() => {
    checkHealth();
    loadRecommendations(DEFAULT_CUSTOMER);
    loadTrending();
    loadSimilar(DEFAULT_ARTICLE);
    loadFavorites(DEFAULT_CUSTOMER);
    loadRecent(DEFAULT_CUSTOMER);
    loadFeedback(DEFAULT_CUSTOMER);
  }, []);

  // =========================================================
  // Styles
  // =========================================================

  const styles = {
    app: {
      minHeight: "100vh",
      background:
        "linear-gradient(135deg, #070b14 0%, #0c1220 50%, #080b12 100%)",
      color: "#ffffff",
      fontFamily:
        "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
      paddingBottom: "60px"
    },

    header: {
      position: "sticky",
      top: 0,
      zIndex: 100,
      backdropFilter: "blur(18px)",
      background: "rgba(7, 11, 20, 0.82)",
      borderBottom:
        "1px solid rgba(255,255,255,0.08)",
      padding: "18px 40px"
    },

    headerInner: {
      maxWidth: "1400px",
      margin: "auto",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: "20px"
    },

    brand: {
      display: "flex",
      alignItems: "center",
      gap: "14px"
    },

    logo: {
      width: "46px",
      height: "46px",
      borderRadius: "14px",
      background:
        "linear-gradient(135deg, #7c3aed, #2563eb)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: "23px",
      boxShadow:
        "0 8px 30px rgba(99,102,241,0.35)"
    },

    brandTitle: {
      fontSize: "18px",
      fontWeight: "800",
      margin: 0
    },

    brandSubtitle: {
      fontSize: "12px",
      color: "#8b95a7",
      marginTop: "3px"
    },

    health: {
      display: "flex",
      alignItems: "center",
      gap: "8px",
      padding: "8px 14px",
      borderRadius: "999px",
      background:
        "rgba(34,197,94,0.10)",
      border:
        "1px solid rgba(34,197,94,0.25)",
      color: "#86efac",
      fontSize: "13px",
      fontWeight: "700"
    },

    container: {
      maxWidth: "1400px",
      margin: "auto",
      padding: "35px 40px"
    },

    hero: {
      padding: "45px 0 30px"
    },

    heroTitle: {
      fontSize: "clamp(34px, 5vw, 62px)",
      lineHeight: "1.02",
      margin: 0,
      fontWeight: "900",
      letterSpacing: "-2px",
      maxWidth: "850px"
    },

    gradientText: {
      background:
        "linear-gradient(90deg, #a78bfa, #60a5fa, #22d3ee)",
      WebkitBackgroundClip: "text",
      WebkitTextFillColor: "transparent"
    },

    heroText: {
      maxWidth: "720px",
      color: "#9ca8ba",
      fontSize: "17px",
      lineHeight: "1.7",
      marginTop: "20px"
    },

    controlPanel: {
      marginTop: "28px",
      display: "flex",
      flexWrap: "wrap",
      gap: "12px",
      padding: "18px",
      background:
        "rgba(255,255,255,0.035)",
      border:
        "1px solid rgba(255,255,255,0.08)",
      borderRadius: "18px"
    },

    input: {
      flex: "1 1 420px",
      minWidth: "250px",
      background: "#0d1422",
      border:
        "1px solid rgba(255,255,255,0.1)",
      color: "#fff",
      padding: "13px 15px",
      borderRadius: "11px",
      outline: "none",
      fontSize: "14px"
    },

    button: {
      border: "none",
      borderRadius: "11px",
      padding: "13px 18px",
      cursor: "pointer",
      color: "#fff",
      fontWeight: "750",
      fontSize: "14px",
      background:
        "linear-gradient(135deg, #7c3aed, #2563eb)"
    },

    secondaryButton: {
      border:
        "1px solid rgba(255,255,255,0.1)",
      borderRadius: "10px",
      padding: "9px 12px",
      cursor: "pointer",
      color: "#dbe4f0",
      fontWeight: "650",
      fontSize: "12px",
      background:
        "rgba(255,255,255,0.05)"
    },

    message: {
      marginTop: "14px",
      color: "#86efac",
      fontSize: "13px"
    },

    error: {
      marginTop: "14px",
      color: "#fca5a5",
      fontSize: "13px"
    },

    section: {
      marginTop: "45px"
    },

    sectionHeader: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: "15px",
      marginBottom: "18px"
    },

    sectionTitle: {
      fontSize: "24px",
      fontWeight: "850",
      margin: 0
    },

    sectionDescription: {
      color: "#778398",
      fontSize: "13px",
      marginTop: "5px"
    },

    grid: {
      display: "grid",
      gridTemplateColumns:
        "repeat(auto-fill, minmax(220px, 1fr))",
      gap: "16px"
    },

    card: {
      background:
        "linear-gradient(145deg, rgba(255,255,255,0.065), rgba(255,255,255,0.025))",
      border:
        "1px solid rgba(255,255,255,0.09)",
      borderRadius: "18px",
      padding: "18px",
      transition:
        "transform 0.2s ease, border-color 0.2s ease",
      minHeight: "170px"
    },

    cardTop: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    },

    articleIcon: {
      width: "44px",
      height: "44px",
      borderRadius: "12px",
      background:
        "linear-gradient(135deg, rgba(124,58,237,.25), rgba(37,99,235,.25))",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: "20px"
    },

    rank: {
      color: "#8792a6",
      fontSize: "12px",
      fontWeight: "700"
    },

    articleId: {
      marginTop: "18px",
      fontSize: "17px",
      fontWeight: "800"
    },

    score: {
      marginTop: "7px",
      color: "#8ea2bd",
      fontSize: "13px"
    },

    actions: {
      display: "flex",
      flexWrap: "wrap",
      gap: "7px",
      marginTop: "16px"
    },

    statGrid: {
      display: "grid",
      gridTemplateColumns:
        "repeat(auto-fit, minmax(180px, 1fr))",
      gap: "14px",
      marginTop: "25px"
    },

    stat: {
      padding: "18px",
      borderRadius: "16px",
      background:
        "rgba(255,255,255,0.035)",
      border:
        "1px solid rgba(255,255,255,0.08)"
    },

    statValue: {
      fontSize: "28px",
      fontWeight: "900"
    },

    statLabel: {
      marginTop: "5px",
      color: "#7e899b",
      fontSize: "12px"
    },

    empty: {
      padding: "30px",
      borderRadius: "16px",
      border:
        "1px dashed rgba(255,255,255,0.12)",
      color: "#748096",
      textAlign: "center"
    },

    footer: {
      marginTop: "70px",
      paddingTop: "25px",
      borderTop:
        "1px solid rgba(255,255,255,0.07)",
      color: "#647086",
      textAlign: "center",
      fontSize: "12px"
    }
  };

  // =========================================================
  // Recommendation Card
  // =========================================================

  const RecommendationCard = ({
    item,
    index
  }) => {
    const isFavorite = favorites.some(
      (fav) =>
        Number(fav.article_id) ===
        Number(item.article_id)
    );

    return (
      <div style={styles.card}>
        <div style={styles.cardTop}>
          <div style={styles.articleIcon}>
            👕
          </div>

          <div style={styles.rank}>
            #{index + 1}
          </div>
        </div>

        <div style={styles.articleId}>
          Article #{item.article_id}
        </div>

        <div style={styles.score}>
          Similarity Score:{" "}
          <strong>
            {Number(item.score).toFixed(4)}
          </strong>
        </div>

        <div style={styles.actions}>
          <button
            style={styles.secondaryButton}
            onClick={() =>
              addRecentlyViewed(item.article_id)
            }
          >
            👁 View
          </button>

          <button
            style={styles.secondaryButton}
            onClick={() =>
              sendFeedback(
                item.article_id,
                "like"
              )
            }
          >
            👍
          </button>

          <button
            style={styles.secondaryButton}
            onClick={() =>
              sendFeedback(
                item.article_id,
                "dislike"
              )
            }
          >
            👎
          </button>

          <button
            style={styles.secondaryButton}
            onClick={() =>
              isFavorite
                ? removeFavorite(
                    item.article_id
                  )
                : addFavorite(
                    item.article_id
                  )
            }
          >
            {isFavorite ? "❤️" : "♡"}
          </button>
        </div>
      </div>
    );
  };

  // =========================================================
  // Simple Article Card
  // =========================================================

  const SimpleArticleCard = ({
    item,
    index,
    icon = "👕"
  }) => {
    const id =
      item.article_id ?? item.id;

    const score =
      item.score !== undefined
        ? Number(item.score)
        : null;

    return (
      <div style={styles.card}>
        <div style={styles.cardTop}>
          <div style={styles.articleIcon}>
            {icon}
          </div>

          <div style={styles.rank}>
            #{index + 1}
          </div>
        </div>

        <div style={styles.articleId}>
          Article #{id}
        </div>

        {score !== null && (
          <div style={styles.score}>
            Score:{" "}
            <strong>
              {score.toFixed(4)}
            </strong>
          </div>
        )}

        <div style={styles.actions}>
          <button
            style={styles.secondaryButton}
            onClick={() => {
              setArticleId(id);
              loadSimilar(id);
            }}
          >
            ✨ Similar
          </button>

          <button
            style={styles.secondaryButton}
            onClick={() =>
              addRecentlyViewed(id)
            }
          >
            👁 View
          </button>
        </div>
      </div>
    );
  };

  return (
    <div style={styles.app}>
      {/* =====================================================
          HEADER
      ===================================================== */}

      <header style={styles.header}>
        <div style={styles.headerInner}>
          <div style={styles.brand}>
            <div style={styles.logo}>
              🧠
            </div>

            <div>
              <h1 style={styles.brandTitle}>
                Context-Aware Neural
              </h1>

              <div style={styles.brandSubtitle}>
                Recommendation Engine
              </div>
            </div>
          </div>

          <div style={styles.health}>
            <span>
              {health ? "●" : "○"}
            </span>

            {health
              ? "API Connected"
              : "API Offline"}
          </div>
        </div>
      </header>

      {/* =====================================================
          MAIN
      ===================================================== */}

      <main style={styles.container}>
        {/* HERO */}

        <section style={styles.hero}>
          <div
            style={{
              color: "#8b95a7",
              fontSize: "13px",
              fontWeight: "700",
              marginBottom: "14px"
            }}
          >
            TWO-TOWER ANN • PERSONALIZED AI
          </div>

          <h2 style={styles.heroTitle}>
            Intelligent recommendations,
            <br />

            <span style={styles.gradientText}>
              built for every customer.
            </span>
          </h2>

          <p style={styles.heroText}>
            A context-aware recommendation system
            powered by a Two-Tower Neural Network.
            Customer and article features are converted
            into embeddings and ranked using cosine
            similarity.
          </p>

          {/* CUSTOMER CONTROL */}

          <div style={styles.controlPanel}>
            <input
              style={styles.input}
              value={searchCustomerId}
              onChange={(e) =>
                setSearchCustomerId(
                  e.target.value
                )
              }
              placeholder="Enter Customer ID"
            />

            <button
              style={styles.button}
              onClick={() =>
                loadRecommendations(
                  searchCustomerId
                )
              }
            >
              🎯 Get Recommendations
            </button>

            <button
              style={styles.secondaryButton}
              onClick={() => {
                loadFavorites(
                  searchCustomerId
                );
                loadRecent(
                  searchCustomerId
                );
                loadFeedback(
                  searchCustomerId
                );
              }}
            >
              Refresh User Data
            </button>
          </div>

          {message && (
            <div style={styles.message}>
              ✓ {message}
            </div>
          )}

          {error && (
            <div style={styles.error}>
              ⚠ {error}
            </div>
          )}

          {/* STATS */}

          <div style={styles.statGrid}>
            <div style={styles.stat}>
              <div style={styles.statValue}>
                {recommendations.length}
              </div>

              <div style={styles.statLabel}>
                Personalized Results
              </div>
            </div>

            <div style={styles.stat}>
              <div style={styles.statValue}>
                {favorites.length}
              </div>

              <div style={styles.statLabel}>
                Favorite Articles
              </div>
            </div>

            <div style={styles.stat}>
              <div style={styles.statValue}>
                {recent.length}
              </div>

              <div style={styles.statLabel}>
                Recently Viewed
              </div>
            </div>

            <div style={styles.stat}>
              <div style={styles.statValue}>
                {feedback.length}
              </div>

              <div style={styles.statLabel}>
                User Feedback
              </div>
            </div>
          </div>
        </section>

        {/* =================================================
            PERSONALIZED
        ================================================= */}

        <section style={styles.section}>
          <div style={styles.sectionHeader}>
            <div>
              <h3 style={styles.sectionTitle}>
                🎯 Personalized For You
              </h3>

              <div style={styles.sectionDescription}>
                Recommendations generated by the
                Two-Tower ANN model
              </div>
            </div>

            <button
              style={styles.secondaryButton}
              onClick={() =>
                loadRecommendations()
              }
            >
              ↻ Refresh
            </button>
          </div>

          {loadingRecommendations ? (
            <div style={styles.empty}>
              Generating recommendations...
            </div>
          ) : recommendations.length === 0 ? (
            <div style={styles.empty}>
              No recommendations available.
            </div>
          ) : (
            <div style={styles.grid}>
              {recommendations.map(
                (item, index) => (
                  <RecommendationCard
                    key={item.article_id}
                    item={item}
                    index={index}
                  />
                )
              )}
            </div>
          )}
        </section>

        {/* =================================================
            TRENDING
        ================================================= */}

        <section style={styles.section}>
          <div style={styles.sectionHeader}>
            <div>
              <h3 style={styles.sectionTitle}>
                🔥 Trending Articles
              </h3>

              <div style={styles.sectionDescription}>
                Articles currently receiving the
                strongest interaction signals
              </div>
            </div>

            <button
              style={styles.secondaryButton}
              onClick={loadTrending}
            >
              ↻ Refresh
            </button>
          </div>

          {loadingTrending ? (
            <div style={styles.empty}>
              Loading trending articles...
            </div>
          ) : trending.length === 0 ? (
            <div style={styles.empty}>
              No trending data available.
            </div>
          ) : (
            <div style={styles.grid}>
              {trending.map(
                (item, index) => (
                  <SimpleArticleCard
                    key={item.article_id}
                    item={item}
                    index={index}
                    icon="🔥"
                  />
                )
              )}
            </div>
          )}
        </section>

        {/* =================================================
            SIMILAR ARTICLES
        ================================================= */}

        <section style={styles.section}>
          <div style={styles.sectionHeader}>
            <div>
              <h3 style={styles.sectionTitle}>
                ✨ Similar Articles
              </h3>

              <div style={styles.sectionDescription}>
                Find articles with similar learned
                embeddings
              </div>
            </div>
          </div>

          <div style={styles.controlPanel}>
            <input
              style={styles.input}
              type="number"
              value={articleId}
              onChange={(e) =>
                setArticleId(e.target.value)
              }
              placeholder="Enter Article ID"
            />

            <button
              style={styles.button}
              onClick={() =>
                loadSimilar(articleId)
              }
            >
              ✨ Find Similar
            </button>
          </div>

          {loadingSimilar ? (
            <div style={styles.empty}>
              Calculating similar articles...
            </div>
          ) : similar.length === 0 ? (
            <div style={styles.empty}>
              No similar articles available.
            </div>
          ) : (
            <div
              style={{
                ...styles.grid,
                marginTop: "18px"
              }}
            >
              {similar.map(
                (item, index) => (
                  <SimpleArticleCard
                    key={item.article_id}
                    item={item}
                    index={index}
                    icon="✨"
                  />
                )
              )}
            </div>
          )}
        </section>

        {/* =================================================
            FAVORITES
        ================================================= */}

        <section style={styles.section}>
          <div style={styles.sectionHeader}>
            <div>
              <h3 style={styles.sectionTitle}>
                ❤️ Favorites
              </h3>

              <div style={styles.sectionDescription}>
                Articles saved by the current customer
              </div>
            </div>
          </div>

          {favorites.length === 0 ? (
            <div style={styles.empty}>
              No favorite articles yet.
            </div>
          ) : (
            <div style={styles.grid}>
              {favorites.map(
                (item, index) => (
                  <SimpleArticleCard
                    key={item.article_id}
                    item={item}
                    index={index}
                    icon="❤️"
                  />
                )
              )}
            </div>
          )}
        </section>

        {/* =================================================
            RECENT
        ================================================= */}

        <section style={styles.section}>
          <div style={styles.sectionHeader}>
            <div>
              <h3 style={styles.sectionTitle}>
                🕘 Recently Viewed
              </h3>

              <div style={styles.sectionDescription}>
                Latest articles interacted with by the
                customer
              </div>
            </div>
          </div>

          {recent.length === 0 ? (
            <div style={styles.empty}>
              No recently viewed articles.
            </div>
          ) : (
            <div style={styles.grid}>
              {recent.map(
                (item, index) => (
                  <div
                    key={`${item.article_id}-${index}`}
                    style={styles.card}
                  >
                    <div style={styles.articleIcon}>
                      🕘
                    </div>

                    <div style={styles.articleId}>
                      Article #{item.article_id}
                    </div>

                    <div style={styles.score}>
                      {item.timestamp}
                    </div>

                    <div style={styles.actions}>
                      <button
                        style={styles.secondaryButton}
                        onClick={() => {
                          setArticleId(
                            item.article_id
                          );

                          loadSimilar(
                            item.article_id
                          );
                        }}
                      >
                        ✨ Similar
                      </button>
                    </div>
                  </div>
                )
              )}
            </div>
          )}
        </section>

        {/* =================================================
            FEEDBACK
        ================================================= */}

        <section style={styles.section}>
          <div style={styles.sectionHeader}>
            <div>
              <h3 style={styles.sectionTitle}>
                👍 User Feedback
              </h3>

              <div style={styles.sectionDescription}>
                Feedback signals used by the
                personalization layer
              </div>
            </div>
          </div>

          {feedback.length === 0 ? (
            <div style={styles.empty}>
              No feedback submitted yet.
            </div>
          ) : (
            <div style={styles.grid}>
              {feedback.map(
                (item, index) => (
                  <div
                    key={`${item.article_id}-${index}`}
                    style={styles.card}
                  >
                    <div style={styles.articleIcon}>
                      {item.feedback ===
                      "like"
                        ? "👍"
                        : "👎"}
                    </div>

                    <div style={styles.articleId}>
                      Article #{item.article_id}
                    </div>

                    <div style={styles.score}>
                      Feedback:{" "}
                      <strong>
                        {item.feedback}
                      </strong>
                    </div>

                    <div style={styles.score}>
                      {item.timestamp}
                    </div>
                  </div>
                )
              )}
            </div>
          )}
        </section>

        {/* =================================================
            FOOTER
        ================================================= */}

        <footer style={styles.footer}>
          <div>
            Context-Aware Neural Recommendation Engine
          </div>

          <div style={{ marginTop: "7px" }}>
            Two-Tower ANN • FastAPI • PyTorch • React
          </div>

          <div style={{ marginTop: "7px" }}>
            API: {API_BASE}
          </div>
        </footer>
      </main>
    </div>
  );
}

export default App;