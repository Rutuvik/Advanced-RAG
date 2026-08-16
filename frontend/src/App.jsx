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

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        throw new Error(
          errorData.detail || "Failed to process the question."
        );
      }

      const data = await response.json();

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

  const getConfidenceClass = (level) => {
    if (!level) return "confidence-default";

    return `confidence-${level.toLowerCase()}`;
  };

  return (
    <div className="app">

      {/* ================================================= */}
      {/* HEADER */}
      {/* ================================================= */}

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            ◈
          </div>

          <div>
            <h1>Advanced RAG</h1>

            <p>
              Secure Retrieval-Augmented Generation
            </p>
          </div>

        </div>

        <div className="status">
          <span className="status-dot"></span>
          API Online
        </div>

      </header>


      {/* ================================================= */}
      {/* MAIN */}
      {/* ================================================= */}

      <main className="main">

        <section className="hero">

          <div className="hero-badge">
            MULTI-STAGE RETRIEVAL SYSTEM
          </div>

          <h2>
            Ask your documents.
            <br />
            <span>Get grounded answers.</span>
          </h2>

          <p className="hero-description">
            Ask questions against your indexed knowledge base
            using hybrid retrieval, multi-query expansion,
            reranking and confidence evaluation.
          </p>

        </section>


        {/* ================================================= */}
        {/* QUESTION BOX */}
        {/* ================================================= */}

        <section className="query-section">

          <div className="query-label">
            <span>QUESTION</span>

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
              placeholder="Ask something about your documents..."
              rows={4}
              disabled={loading}
            />

            <div className="query-footer">

              <span className="query-hint">
                Answers are generated only from retrieved context.
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
                    Retrieving...
                  </>
                ) : (
                  <>
                    Ask Question
                    <span>→</span>
                  </>
                )}

              </button>

            </div>

          </div>

        </section>


        {/* ================================================= */}
        {/* ERROR */}
        {/* ================================================= */}

        {error && (
          <div className="error-box">
            <div className="error-icon">!</div>

            <div>
              <strong>Request failed</strong>
              <p>{error}</p>
            </div>
          </div>
        )}


        {/* ================================================= */}
        {/* RESULT */}
        {/* ================================================= */}

        {result && (
          <section className="results">

            {/* ANSWER */}

            <div className="answer-card">

              <div className="section-heading">

                <div>
                  <span className="eyebrow">
                    GENERATED RESPONSE
                  </span>

                  <h3>Answer</h3>
                </div>

                {result.confidence && (
                  <div
                    className={`confidence ${getConfidenceClass(
                      result.confidence.level
                    )}`}
                  >
                    <span className="confidence-dot"></span>

                    {result.confidence.level || "Unknown"}
                  </div>
                )}

              </div>


              <div className="answer-content">
                {result.answer}
              </div>


              {result.confidence && (
                <div className="confidence-details">

                  <div className="confidence-item">
                    <span>Confidence score</span>

                    <strong>
                      {typeof result.confidence.score ===
                      "number"
                        ? result.confidence.score.toFixed(4)
                        : "N/A"}
                    </strong>
                  </div>

                  <div className="confidence-item">
                    <span>Decision</span>

                    <strong>
                      {result.confidence.should_answer
                        ? "Answer"
                        : "Reject"}
                    </strong>
                  </div>

                </div>
              )}

            </div>


            {/* SOURCES */}

            {result.sources &&
              result.sources.length > 0 && (

                <div className="sources-card">

                  <div className="section-heading">

                    <div>
                      <span className="eyebrow">
                        RETRIEVAL
                      </span>

                      <h3>
                        Sources
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

                        const rerankScore =
                          source.rerank_score;

                        return (
                          <div
                            className="source-item"
                            key={
                              source.parent_id ||
                              `${filename}-${page}-${index}`
                            }
                          >

                            <div className="source-number">
                              {String(index + 1).padStart(
                                2,
                                "0"
                              )}
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


                            {typeof rerankScore ===
                              "number" && (
                              <div className="source-score">

                                <span>
                                  Rerank
                                </span>

                                <strong>
                                  {rerankScore.toFixed(
                                    4
                                  )}
                                </strong>

                              </div>
                            )}

                          </div>
                        );
                      }
                    )}

                  </div>

                </div>
              )}

          </section>
        )}


        {/* ================================================= */}
        {/* ARCHITECTURE */}
        {/* ================================================= */}

        <section className="architecture">

          <div className="architecture-header">

            <div>
              <span className="eyebrow">
                PIPELINE
              </span>

              <h3>
                How the system works
              </h3>
            </div>

          </div>


          <div className="pipeline">

            <div className="pipeline-step">
              <span>01</span>
              <strong>Query Expansion</strong>
              <small>
                Multiple search queries
              </small>
            </div>

            <div className="pipeline-arrow">
              →
            </div>

            <div className="pipeline-step">
              <span>02</span>
              <strong>Hybrid Retrieval</strong>
              <small>
                Dense + BM25
              </small>
            </div>

            <div className="pipeline-arrow">
              →
            </div>

            <div className="pipeline-step">
              <span>03</span>
              <strong>Reranking</strong>
              <small>
                Cross-encoder scoring
              </small>
            </div>

            <div className="pipeline-arrow">
              →
            </div>

            <div className="pipeline-step">
              <span>04</span>
              <strong>Generation</strong>
              <small>
                Grounded LLM answer
              </small>
            </div>

          </div>

        </section>

      </main>


      {/* ================================================= */}
      {/* FOOTER */}
      {/* ================================================= */}

      <footer className="footer">

        <span>
          Advanced RAG
        </span>

        <span>
          Hybrid Retrieval · Reranking · Confidence
        </span>

      </footer>

    </div>
  );
}

export default App;