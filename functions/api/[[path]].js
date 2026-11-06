export async function onRequest({ request, env }) {
  const incomingUrl = new URL(request.url);
  if (!["/api/state", "/api/command"].includes(incomingUrl.pathname)) {
    return Response.json({ error: "Not found" }, { status: 404 });
  }

  if (!env.BACKEND_URL) {
    return Response.json(
      { error: "The game backend is not configured." },
      { status: 503 },
    );
  }

  let backendUrl;
  try {
    backendUrl = new URL(env.BACKEND_URL);
  } catch {
    return Response.json(
      { error: "The game backend URL is invalid." },
      { status: 500 },
    );
  }
  if (backendUrl.protocol !== "https:") {
    return Response.json(
      { error: "The game backend URL must use HTTPS." },
      { status: 500 },
    );
  }

  const targetUrl = new URL(
    `${incomingUrl.pathname}${incomingUrl.search}`,
    backendUrl,
  );
  try {
    return await fetch(new Request(targetUrl, request));
  } catch (error) {
    console.error("Could not reach the Python game backend:", error);
    return Response.json(
      { error: "Could not reach the game server." },
      { status: 502 },
    );
  }
}
