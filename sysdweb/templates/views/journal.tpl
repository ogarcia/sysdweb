<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>{{service}} journal · {{hostname or 'sysdweb'}} · sysdweb</title>
    <link href="/css/bootstrap.min.css" rel="stylesheet">
    <link href="/css/sysdweb.css" rel="stylesheet">
    <link rel="shortcut icon" href="/img/favicon.png">
  </head>
  <body>
    <div class="container-fluid">
      <div class="text-center">
        <h1 class="display-4">{{service}} journal</h1>
        <h2 class="display-6 text-muted">{{hostname or 'sysdweb'}}</h2>
      </div>
      <div>
<pre class="border p-2 rounded bg-dark text-white" id="journal">
% for line in journal:
{{line}}
% end
</pre>
      </div>
    </div>
  </body>
</html>
