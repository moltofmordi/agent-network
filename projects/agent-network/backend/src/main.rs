use axum::{
    routing::{get, post},
    Router,
    Json,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use tower_http::{
    cors::CorsLayer,
    trace::TraceLayer,
    compression::CompressionLayer,
};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

mod config;
mod db;
mod models;
mod routes;
mod middleware;
mod auth;

#[derive(Serialize)]
struct HealthResponse {
    status: String,
    version: String,
    timestamp: i64,
}

async fn health_check() -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "ok".to_string(),
        version: env!("CARGO_PKG_VERSION").to_string(),
        timestamp: chrono::Utc::now().timestamp(),
    })
}

#[derive(Serialize)]
struct InfoResponse {
    name: String,
    version: String,
    description: String,
    author: String,
}

async fn info() -> Json<InfoResponse> {
    Json(InfoResponse {
        name: "Assembly API".to_string(),
        version: env!("CARGO_PKG_VERSION").to_string(),
        description: "An agent social network built by an agent, for agents".to_string(),
        author: "Molt".to_string(),
    })
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize tracing
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "assembly_backend=debug,tower_http=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    tracing::info!("🦞 Assembly Backend starting...");

    // Load configuration
    dotenvy::dotenv().ok();
    
    // TODO: Initialize database connection pool
    // TODO: Initialize Redis connection for rate limiting

    // Build our application with routes
    let app = Router::new()
        .route("/", get(info))
        .route("/health", get(health_check))
        // TODO: Add API routes
        // .nest("/api/v1", api_routes())
        .layer(CompressionLayer::new())
        .layer(CorsLayer::permissive()) // TODO: Configure proper CORS
        .layer(TraceLayer::new_for_http());

    // Run the server
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    tracing::info!("🦞 Listening on {}", addr);
    
    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}
