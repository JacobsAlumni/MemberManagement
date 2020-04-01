const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack4-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const isDevelopment = process.env.NODE_ENV === 'development';

module.exports = {
  context: __dirname,

  // development
  mode: isDevelopment ? 'development' : 'production',
  devtool: isDevelopment ? 'eval-source-map' : false,

  // all the entry points
  entry: {
    'atlas': './assets/src/atlas/index.ts',
    'base': './assets/src/base/index.ts',
    'login': './assets/src/login/index.ts',
    'profile': './assets/src/profile/index.ts',
    'search_form': './assets/src/search_form/index.ts',
    'subscribe': './assets/src/subscribe/index.ts',
    'tier': './assets/src/tier/index.ts',
    'token_login': './assets/src/token_login/index.ts',
  },

  // magic .ts and .js
  resolve: {
    extensions: ['.ts', '.js'],
  },

  // ts-loader
  module: {
    rules: [

      // typescript
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },

      // css
      {
        test: /\.css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
        ],
      },

      // scss
      {
        test: /\.s[ac]ss$/i,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ],
      },
    ],
  },

  optimization: {
    // we don't want a runtime chunk, because otherwise we can't have multiple entry points
    // runtimechunk: single won't work, as otherwise the main script might get run multiple times!
    runtimeChunk: false,
    
    // split all the chunks, hopefully make some things smaller
    splitChunks: {
      chunks: 'all'
    }
  },


  // output all the things
  output: {
    path: path.resolve('./assets/bundles/'),
    filename: "[name]-[hash].js"
  },

  // for django, we need to keep track of stats
  plugins: [
    new BundleTracker({ filename: './webpack-stats.json' }),
    new MiniCssExtractPlugin({
      filename: '[name]-[hash].css'
    }),
  ],

}
