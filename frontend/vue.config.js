const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  publicPath: process.env.BASE_URL,

  outputDir: "./dist/dist/",
  transpileDependencies: ["vuetify"],

  chainWebpack: (config) => {
    config
      .plugin("BundleTracker")
      .use(BundleTracker, [{ filename: "./webpack-stats.json" }]);
    config.output.filename("bundle.js");
    config.optimization.splitChunks(false);
    config.resolve.alias.set("__STATIC__", "static");
    config.devServer
      .https(false)
      .headers({ "Access-Control-Allow-Origin": ["*"] });
  },

  lintOnSave: false,
};

