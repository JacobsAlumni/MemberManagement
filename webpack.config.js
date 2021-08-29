const path = require('path');
const BundleTracker = require('webpack4-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

const isDevelopment = process.env.NODE_ENV === 'development';

module.exports = {
  context: __dirname,

  // development
  mode: isDevelopment ? 'development' : 'production',
  devtool: isDevelopment ? 'eval-source-map' : false,

  // all the entry points
  entry: {
    'base__base': [
      'jacobs-alumni-style',
      'nodep-date-input-polyfill',
      './assets/src/base/base/cookielaw.js'
    ],

    'atlas__atlas': './assets/src/atlas/atlas/index.ts',
    'atlas__profile': './assets/src/atlas/profile/index.ts',
    'atlas__search_form': './assets/src/atlas/search_form/index.ts',

    'custom_auth__login': './assets/src/custom_auth/login/index.ts',
    'custom_auth__token_login': './assets/src/custom_auth/token_login/index.ts',

    'payments__subscribe': './assets/src/payments/subscribe/index.ts',
    'payments__tier': './assets/src/payments/tier/index.ts',

    'registry__signup': './assets/src/registry/signup/index.ts',
    'registry__approval': './assets/src/registry/approval/index.ts',
    'registry__stats': './assets/src/registry/stats/index.ts',
  },

  // magic .ts and .js
  resolve: {
    extensions: ['.ts', '.js'],
  },

  // ts-loader
  module: {
    rules: [
      // Vue SFC
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },

      // typescript
      {
        test: /\.tsx?$/,
        loader: 'ts-loader',
        exclude: /node_modules/,
        options: { appendTsSuffixTo: [/\.vue$/] }
      },

      // css
      {
        test: /\.css$/i,
        use: [
          isDevelopment ? 'vue-style-loader' : MiniCssExtractPlugin.loader,
          'css-loader'
        ],
      },

      // scss
      {
        test: /\.s[ac]ss$/i,
        use: [
          isDevelopment ? 'vue-style-loader' : MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ],
      },

      // Vue SFC - pug templates
      {
        test: /\.pug$/,
        loader: 'pug-plain-loader'
      },

      // Vue SFC - referenced images
      {
        test: /\.(png|jpg|gif)$/i,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 8192,
            },
          },
        ],
      }
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
    filename: "[name]-[fullhash].js",
    publicPath: "/static/bundles/",
  },

  // for django, we need to keep track of stats
  plugins: [
    new BundleTracker({ filename: './webpack-stats.json' }),
    new MiniCssExtractPlugin({
      filename: '[name]-[fullhash].css'
    }),
    new VueLoaderPlugin()
  ],

}

if (!isDevelopment) {
  module.exports.plugins.push(new CleanWebpackPlugin());
}