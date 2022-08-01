const {createProxyMiddleware} = require('http-proxy-middleware');

module.exports = (app) => {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:5000',
    })
  );

  app.use(
    '/login',
    createProxyMiddleware({
      target: 'http://localhost:5000',
    })
  );
};
