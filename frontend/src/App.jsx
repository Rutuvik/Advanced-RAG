import { useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askQuestion = async () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to process the question."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the RAG backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askQuestion();
    }
  };

  const formatTime = (value) => {
    if (typeof value !== "number") return "—";

    return `${value.toFixed(2)}s`;
  };

  const formatScore = (value) => {
    if (typeof value !== "number") return "—";

    return value.toFixed(4);
  };

  const confidenceLevel =
    result?.confidence?.level?.toLowerCase() || "default";

  const retrieval = result?.retrieval || {};

  const metrics =
    result?.metrics ||
    result?.metrices ||
    {};

  return (
    <div className="app">

      {/* ================= HEADER ================= */}

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            ◈
          </div>

          <div>
            <h1>Advanced RAG</h1>

            <p>
              Retrieval Intelligence Platform
            </p>
          </div>

        </div>

        <div className="status">
          <span className="status-dot"></span>
          Local API
        </div>

      </header>


      {/* ================= MAIN ================= */}

      <main className="main">

        {/* HERO */}

        <section className="hero">

          <div className="hero-badge">
            ADVANCED RETRIEVAL-AUGMENTED GENERATION
          </div>

          <h2>
            Ask your knowledge base.
            <br />
            <span>Inspect the entire RAG pipeline.</span>
          </h2>

          <p className="hero-description">
            Multi-query expansion, hybrid retrieval,
            reranking, confidence evaluation and
            grounded generation — all in one system.
          </p>

        </section>


        {/* ================= QUERY ================= */}

        <section className="query-section">

          <div className="query-label">

            <span>QUERY</span>

            <span className="shortcut">
              ENTER ↵
            </span>

          </div>

          <div className="query-box">

            <textarea
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Ask a question about your indexed documents..."
              rows={4}
              disabled={loading}
            />

            <div className="query-footer">

              <span className="query-hint">
                Responses are grounded in retrieved
                document context.
              </span>

              <button
                className="ask-button"
                onClick={askQuestion}
                disabled={
                  loading ||
                  !question.trim()
                }
              >

                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Running RAG pipeline...
                  </>
                ) : (
                  <>
                    Run Query
                    <span>→</span>
                  </>
                )}

              </button>

            </div>

          </div>

        </section>


        {/* ================= LOADING ================= */}

        {loading && (

          <div className="loading-panel">

            <div className="loading-spinner"></div>

            <div>

              <strong>
                Processing your query
              </strong>

              <p>
                Expanding query → Hybrid retrieval →
                Reranking → Confidence → Generation
              </p>

            </div>

          </div>

        )}


        {/* ================= ERROR ================= */}

        {error && (

          <div className="error-box">

            <div className="error-icon">
              !
            </div>

            <div>

              <strong>
                Request failed
              </strong>

              <p>
                {error}
              </p>

            </div>

          </div>

        )}


        {/* ================= RESULTS ================= */}

        {result && (

          <section className="results">

            {/* ================= ANSWER ================= */}

            <div className="answer-card">

              <div className="section-heading">

                <div>

                  <span className="eyebrow">
                    GENERATED RESPONSE
                  </span>

                  <h3>
                    Answer
                  </h3>

                </div>

                {result.confidence && (

                  <div
                    className={`confidence confidence-${confidenceLevel}`}
                  >

                    <span className="confidence-dot"></span>

                    {result.confidence.level}

                  </div>

                )}

              </div>


              <div className="answer-content">

                {result.answer}

              </div>


              {result.confidence && (

                <div className="confidence-details">

                  <div className="confidence-item">

                    <span>
                      Confidence score
                    </span>

                    <strong>
                      {formatScore(
                        result.confidence.score
                      )}
                    </strong>

                  </div>

                  <div className="confidence-item">

                    <span>
                      Decision
                    </span>

                    <strong>
                      {result.confidence.should_answer
                        ? "ANSWER"
                        : "REJECT"}
                    </strong>

                  </div>

                </div>

              )}

            </div>


            {/* ================= METRICS ================= */}

            <div className="metrics-section">

              <div className="section-heading">

                <div>

                  <span className="eyebrow">
                    PERFORMANCE
                  </span>

                  <h3>
                    Pipeline Metrics
                  </h3>

                </div>

              </div>


              <div className="metrics-grid">

                <div className="metric-card">

                  <span>
                    Retrieval
                  </span>

                  <strong>
                    {formatTime(
                      metrics.retrieval_time
                    )}
                  </strong>

                  <small>
                    Dense + BM25 + reranking
                  </small>

                </div>


                <div className="metric-card">

                  <span>
                    Context
                  </span>

                  <strong>
                    {formatTime(
                      metrics.context_time
                    )}
                  </strong>

                  <small>
                    Context construction
                  </small>

                </div>


                <div className="metric-card">

                  <span>
                    Generation
                  </span>

                  <strong>
                    {formatTime(
                      metrics.generation_time
                    )}
                  </strong>

                  <small>
                    LLM response
                  </small>

                </div>


                <div className="metric-card metric-total">

                  <span>
                    Total latency
                  </span>

                  <strong>
                    {formatTime(
                      metrics.total_time
                    )}
                  </strong>

                  <small>
                    End-to-end pipeline
                  </small>

                </div>

              </div>

            </div>


            {/* ================= RETRIEVAL ================= */}

            <div className="retrieval-card">

              <div className="section-heading">

                <div>

                  <span className="eyebrow">
                    RETRIEVAL ANALYSIS
                  </span>

                  <h3>
                    Retrieval Pipeline
                  </h3>

                </div>

              </div>


              <div className="retrieval-stats">

                <div>
                  <span>
                    Search queries
                  </span>

                  <strong>
                    {retrieval.query_count ?? "—"}
                  </strong>
                </div>

                <div>
                  <span>
                    Candidates
                  </span>

                  <strong>
                    {retrieval.candidate_count ?? "—"}
                  </strong>
                </div>

                <div>
                  <span>
                    Reranked
                  </span>

                  <strong>
                    {retrieval.reranked_count ?? "—"}
                  </strong>
                </div>

                <div>
                  <span>
                    Sources used
                  </span>

                  <strong>
                    {retrieval.sources_used ??
                      result.sources?.length ??
                      "—"}
                  </strong>
                </div>

              </div>


              {/* GENERATED QUERIES */}

              {retrieval.queries &&
                retrieval.queries.length > 0 && (

                <div className="query-expansion">

                  <div className="subheading">

                    <span>
                      QUERY EXPANSION
                    </span>

                    <small>
                      {retrieval.queries.length}
                      queries
                    </small>

                  </div>


                  <div className="expanded-queries">

                    {retrieval.queries.map(
                      (searchQuery, index) => (

                        <div
                          className="expanded-query"
                          key={index}
                        >

                          <span className="query-index">
                            {String(
                              index + 1
                            ).padStart(2, "0")}
                          </span>

                          <span>
                            {searchQuery}
                          </span>

                        </div>

                      )
                    )}

                  </div>

                </div>

              )}

            </div>


            {/* ================= SOURCES ================= */}

            {result.sources &&
              result.sources.length > 0 && (

              <div className="sources-card">

                <div className="section-heading">

                  <div>

                    <span className="eyebrow">
                      DOCUMENT EVIDENCE
                    </span>

                    <h3>

                      Retrieved Sources

                      <span className="source-count">
                        {result.sources.length}
                      </span>

                    </h3>

                  </div>

                </div>


                <div className="sources-list">

                  {result.sources.map(
                    (source, index) => {

                      const metadata =
                        source.metadata || {};

                      const filename =
                        metadata.filename ||
                        metadata.source ||
                        "Unknown document";

                      const page =
                        metadata.page;

                      return (

                        <details
                          className="source-item"
                          key={
                            source.parent_id ||
                            `${filename}-${page}-${index}`
                          }
                        >

                          <summary>

                            <div className="source-number">
                              {String(
                                index + 1
                              ).padStart(2, "0")}
                            </div>


                            <div className="source-main">

                              <div className="source-title">
                                {filename}
                              </div>

                              <div className="source-meta">

                                {page !== undefined &&
                                  page !== null && (

                                  <span>
                                    Page {page}
                                  </span>

                                )}

                                {metadata.file_type && (

                                  <span>
                                    {metadata.file_type.toUpperCase()}
                                  </span>

                                )}

                              </div>

                            </div>


                            <div className="source-score-group">

                              {typeof source.rerank_score ===
                                "number" && (

                                <div className="source-score">

                                  <span>
                                    RERANK
                                  </span>

                                  <strong>
                                    {formatScore(
                                      source.rerank_score
                                    )}
                                  </strong>

                                </div>

                              )}

                              {typeof source.rrf_score ===
                                "number" && (

                                <div className="source-score">

                                  <span>
                                    RRF
                                  </span>

                                  <strong>
                                    {formatScore(
                                      source.rrf_score
                                    )}
                                  </strong>

                                </div>

                              )}

                            </div>

                            <span className="expand-icon">
                              +
                            </span>

                          </summary>


                          <div className="source-details">

                            {source.query_match_count && (

                              <div className="source-detail-row">

                                <span>
                                  Query matches
                                </span>

                                <strong>
                                  {source.query_match_count}
                                </strong>

                              </div>

                            )}


                            {source.multi_query_score && (

                              <div className="source-detail-row">

                                <span>
                                  Multi-query score
                                </span>

                                <strong>
                                  {formatScore(
                                    source.multi_query_score
                                  )}
                                </strong>

                              </div>

                            )}


                            <div className="source-text">

                              <span>
                                RETRIEVED CONTENT
                              </span>

                              <p>
                                {source.text ||
                                  "No source text available."}
                              </p>

                            </div>

                          </div>

                        </details>

                      );

                    }
                  )}

                </div>

              </div>

            )}

          </section>

        )}


        {/* ================= ARCHITECTURE ================= */}

        <section className="architecture">

          <div className="architecture-header">

            <div>

              <span className="eyebrow">
                SYSTEM ARCHITECTURE
              </span>

              <h3>
                How Advanced RAG works
              </h3>

            </div>

          </div>


          <div className="pipeline">

            <div className="pipeline-step">

              <span>01</span>

              <strong>
                Query Expansion
              </strong>

              <small>
                Multiple semantic queries
              </small>

            </div>


            <div className="pipeline-arrow">
              →
            </div>


            <div className="pipeline-step">

              <span>02</span>

              <strong>
                Hybrid Retrieval
              </strong>

              <small>
                Dense + BM25 + RRF
              </small>

            </div>


            <div className="pipeline-arrow">
              →
            </div>


            <div className="pipeline-step">

              <span>03</span>

              <strong>
                Cross Encoder
              </strong>

              <small>
                Relevance reranking
              </small>

            </div>


            <div className="pipeline-arrow">
              →
            </div>


            <div className="pipeline-step">

              <span>04</span>

              <strong>
                Confidence
              </strong>

              <small>
                Answer / reject decision
              </small>

            </div>


            <div className="pipeline-arrow">
              →
            </div>


            <div className="pipeline-step">

              <span>05</span>

              <strong>
                LLM Generation
              </strong>

              <small>
                Grounded response
              </small>

            </div>

          </div>

        </section>

      </main>


      {/* ================= FOOTER ================= */}

      <footer className="footer">

        <span>
          Advanced RAG
        </span>

        <span>
          Multi-Query · Hybrid Retrieval · Reranking ·
          Confidence · Grounded Generation
        </span>

      </footer>

    </div>
  );
}

export default App;