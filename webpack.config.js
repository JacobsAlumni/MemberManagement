const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const isDevelopment = process.env.NODE_ENV === 'development';

module.exports = {
  context: __dirname,

  // development
  mode: isDevelopment ? 'development' : 'production',
  devtool: isDevelopment ? 'eval-source-map' : false,

  // all the entry points
  entry: {
    // the base entry point that is included everywhere!
    'base': [
      './assets/src/base/index.ts',
      './assets/src/base/index.scss',
    ],

    'token_login': './assets/src/token_login/index.ts',

    'login': [
      './assets/src/login/index.ts',
      './assets/src/login/index.css',
    ],

    'tier': './assets/src/tier/index.ts',
    'subscribe': [
      './assets/src/subscribe/index.ts',
      './assets/src/subscribe/index.css',
    ],
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

  // split all the chunks
  optimization: {
    splitChunks: false,
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
