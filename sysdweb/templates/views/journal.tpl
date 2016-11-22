<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>{{service}} journal · {{hostname or 'sysdweb'}} · sysdweb</title>

    <!-- Bootstrap -->
    <link href="/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom style -->
    <link href="/css/sysdweb.css" rel="stylesheet">

    <!-- Favicon -->
    <link rel="shortcut icon" href="/img/favicon.png">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="container-fluid">
      <div class="page-header text-center">
        <h1>{{service}} journal<br/>
        <small>{{hostname or 'sysdweb'}}</small></h1>
      </div>
      <div>
<pre id="journal">
% for line in journal:
{{line}}
% end
</pre>
      </div>
    </div>
  </body>
</html>
