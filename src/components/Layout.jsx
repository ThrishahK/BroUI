export default function Layout({ children }) {
  return (
    <div style={{ minHeight: "100vh", background: "black", color: "white" }}>
      {children}
    </div>
  );
}
