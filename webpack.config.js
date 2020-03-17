const HtmlWebPackPlugin = require('html-webpack-plugin');
const path = require('path');

const htmlPlugin = new HtmlWebPackPlugin({
  template: './src/index.html',
  filename: './index.html'
});

const adminHtmlPlugin = new HtmlWebPackPlugin({
  template: './src/admin.html',
  filename: './admin.html'
});

module.exports = [{
  entry: './src/index.jsx',
  output: { // NEW
    path: path.join(__dirname, 'dist'),
    filename: '[name].js'
  }, // NEW Ends
  plugins: [htmlPlugin],
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        }
      }, {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      }, {
        test: /\.ttf$/,
        use: ['file-loader'],
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  }
}, {
  entry: './src/admin.jsx',
  output: { // NEW
    path: path.join(__dirname, 'dist'),
    filename: 'admin.js'
  }, // NEW Ends
  plugins: [adminHtmlPlugin],
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        }
      }, {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      }, {
        test: /\.ttf$/,
        use: ['file-loader'],
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  }
}];

