import { useQuery } from "@tanstack/react-query";

export default function App() {
  const { data, isError } = useQuery({
    queryKey: ["health"],
    queryFn: () => fetch("/api/v1/health").then((r) => r.json()),
  });
  return (
    <main style={{ fontFamily: "sans-serif", padding: 24 }}>
      <h1>BELOVE</h1>
      <p>API: {isError ? "error" : data?.status ?? "..."}</p>
    </main>
  );
}
