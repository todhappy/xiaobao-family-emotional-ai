const nextConfig = {
  experimental: {
    serverActions: true
  },
  async rewrites() {
    return [
      { source: "/api/:path*", destination: "http://127.0.0.1:5001/api/:path*" },
      { source: "/socket.io", destination: "http://127.0.0.1:5001/socket.io" }
    ]
  }
}

export default nextConfig