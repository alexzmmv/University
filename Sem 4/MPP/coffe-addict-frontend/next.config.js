module.exports = {
    allowedDevOrigins: ['*'],
    env: {
        // The API_BASE_URL will be replaced during the build process
        // Default to localhost for development
        API_BASE_URL: "http://localhost:8000/",
    },
    publicRuntimeConfig: {
        // Will be available on both server and client side
        API_BASE_URL:"http://localhost:8000/",
    },
    reactStrictMode: true,
    experimental: {
    },
    output: 'standalone',
}