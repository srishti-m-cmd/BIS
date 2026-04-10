import Navbar from "../components/Navbar";

function ContactPage() {
  return (
    <div className="page-shell">
      <Navbar />
      <main className="simple-page">
        <h1>Contact</h1>
        <p>Email: support@studyhub.local</p>
        <p>Phone: +91 90000 00000</p>
      </main>
    </div>
  );
}

export default ContactPage;
