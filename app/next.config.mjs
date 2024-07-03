/** @type {import('next').NextConfig} */

const nextConfig = {
    webpack: (config) => {
        config.resolve = {
          ...config.resolve,
          fallback: {
            fs: false,
          },
        };
        config.externals = [
            ...(config.externals || []),
            'node-pre-gyp'
        ];
        return config;
      },
};

export default nextConfig;
