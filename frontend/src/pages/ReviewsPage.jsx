import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import api from "../services/api";

function ReviewsPage() {
  const { placeId } = useParams();
  const navigate = useNavigate();
  const [place, setPlace] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [comment, setComment] = useState("");
  const [selectedRating, setSelectedRating] = useState(5);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const loadReviews = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/places/${placeId}/reviews`);
      setPlace(response.data.place);
      setReviews(response.data.reviews || []);
    } catch (err) {
      setError(err?.response?.data?.message || "Failed to load reviews.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReviews();
  }, [placeId]);

  const overallRating = useMemo(() => Number(place?.rating || 0).toFixed(1), [place]);

  const handleAddRating = async () => {
    setError("");
    try {
      await api.post(`/places/${placeId}/reviews`, {
        rating: selectedRating,
        comment,
      });
      setComment("");
      await loadReviews();
    } catch (err) {
      setError(err?.response?.data?.message || "Failed to submit review.");
    }
  };

  return (
    <div className="page-shell">
      <Navbar />
      <main className="reviews-page">
        <button type="button" className="outline-button" onClick={() => navigate("/map")}>
          Back to Map
        </button>
        {loading ? (
          <p>Loading reviews...</p>
        ) : (
          <>
            <h1>{place?.name || "Study Spot"}</h1>
            <section className="overall-rating">
              <h2>Reviews</h2>
              <p>{overallRating}★ overall rating</p>
            </section>

            <section className="review-form">
              <h3>Add your feedback</h3>
              <div className="star-selector">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    className={star <= selectedRating ? "star active-star" : "star"}
                    onClick={() => setSelectedRating(star)}
                  >
                    ★
                  </button>
                ))}
              </div>
              <textarea
                value={comment}
                onChange={(event) => setComment(event.target.value)}
                placeholder="the place was so calm :)"
                rows={3}
              />
              <div className="button-row">
                <button type="button" className="outline-button" onClick={() => document.activeElement?.blur()}>
                  Add comment
                </button>
                <button type="button" className="cta-button" onClick={handleAddRating}>
                  Add rating
                </button>
              </div>
            </section>

            {error && <p className="error-text">{error}</p>}

            <section className="comments-list">
              <h3>Comments</h3>
              {reviews.map((review, index) => (
                <article key={`${review.created_at}-${index}`} className="comment-card">
                  <p>
                    👤 <strong>{review.email}</strong> - {Number(review.rating || 0).toFixed(1)}★
                  </p>
                  <p>{review.comment || "No comment added."}</p>
                </article>
              ))}
              {reviews.length === 0 && <p>No comments yet. Be the first to review.</p>}
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default ReviewsPage;
