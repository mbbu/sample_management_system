const path = require('path');

module.exports = {
  assetsDir: '../static',
  <!-- baseUrl: '', -->
  publicPath: undefined,
  outputDir: path.resolve(__dirname, '../api/templates'),
  runtimeCompiler: undefined,
  productionSourceMap: undefined,
  parallel: undefined,
  css: undefined
};
