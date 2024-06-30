/** @type {import('next').NextConfig} */
const nextConfig = {
    webpack: (config, { isServer }) => {
        // Exclude HTML files from webpack processing
        if (!isServer) {
          config.module.rules.push({
            test: /\.html$/,
            exclude: /node_modules/,
            use: {
              loader: 'babel-loader',
            },
          });
        }
        return config;
      },
};


export default nextConfig;
