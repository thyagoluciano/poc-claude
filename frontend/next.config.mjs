/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    optimizePackageImports: ['@telefonica/mistica'],
  },
};

export default nextConfig;
