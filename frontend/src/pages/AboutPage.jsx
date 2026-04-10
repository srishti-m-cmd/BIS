import Navbar from "../components/Navbar";

function AboutPage() {
  return (
    <div className="page-shell">
      <Navbar />
      <main className="simple-page">
        <h1>About Study Hub</h1>
        <p>
          Study Hub helps students discover nearby study spots using geospatial search,
          community reviews, and ML-powered ranking.
        </p>
      </main>
    </div>
  );
}

export default AboutPage;
