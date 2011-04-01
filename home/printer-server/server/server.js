var http = require('http');
var url  = require('url');


function getLocalContent(path,query){
  url.resolve("/",path)
}

http.createServer(function(req, res) {
  var request_url = url.perse(req.url);
  request_url.pathname

  res.writeHead(200, {'Content-Type': 'text/plain'});
 
  var str = 'Hello World';
 
  res.end(str);
}).listen(10080);