const glob = require('glob');
const Path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const stylesHandler = "style-loader";

const getEntryObject = () => {  // eslint-disable-line
  const entries = {};
  // for javascript entry file
  glob.sync(Path.join(__dirname, "./assets/*.js")).forEach((path) => {
    const name = Path.basename(path, ".js");
    entries[name] = path;
  });
  // for typescript entry file
  glob.sync(Path.join(__dirname, "./assets/*.ts")).forEach((path) => {
    const name = Path.basename(path, ".ts");
    entries[name] = path;
  });
  return entries;
};

module.exports = {
  context: __dirname,
  entry: './assets/js/index',
  output: {
    path: Path.resolve('./backoffice/static/webpack_bundles/'),
    filename: "[name]-[hash].js"
  },
  plugins: [
    new BundleTracker({path: __dirname, filename: 'webpack-stats.json'})
  ],
  resolve: {
    extensions: ['.js', '.ts'],
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.css$/i,
        use: [stylesHandler, 'css-loader', 'postcss-loader'],
      },
    ],
  },
};
