<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>{{hostname or 'sysdweb'}} · sysdweb</title>
    <link href="/css/bootstrap.min.css" rel="stylesheet">
    <link href="/css/sysdweb.css" rel="stylesheet">
    <link rel="shortcut icon" href="/img/favicon.png">
  </head>
  <body>
    <div class="container">
      <div class="text-center">
        <h1 class="display-1">{{hostname or 'sysdweb'}}</h1>
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle" id="services">
          <tr>
            <th>Service</th>
            <th class="text-end">Actions</th>
          </tr>
          % for service in services:
          <tr>
            <td class="table-{{service['class']}}">
            % if service['class'] != 'light':
              <a href="/journal/{{service['service']}}"
                data-bs-toggle="tooltip" data-bs-placement="right"
                data-bs-title="Show journal">
            % end
                {{service['title']}}
            % if service['class'] != 'light':
                </a>
            % end
            </td>
            <td class="text-end table-{{service['class']}}">
              <button type="button" class="btn btn-success btn-sm"
              % if service['disabled_start']:
                disabled
              % end
                data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-title="Start"
                onclick="unit('{{service['service']}}', 'start')">
                <svg xmlns="http://www.w3.org/2000/svg" width="24"
                height="24" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round"
                aria-hidden="true" aria-label="Start">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg></button>
              <button type="button" class="btn btn-danger btn-sm"
              % if service['disabled_stop']:
                disabled
              % end
                data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-title="Stop"
                onclick="unit('{{service['service']}}', 'stop')">
                <svg xmlns="http://www.w3.org/2000/svg" width="24"
                height="24" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round"
                aria-hidden="true" aria-label="Stop">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2">
                </svg></button>
              <button type="button" class="btn btn-primary btn-sm"
              % if service['disabled_restart']:
                disabled
              % end
                data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-title="Restart"
                onclick="unit('{{service['service']}}', 'restart')">
                <svg xmlns="http://www.w3.org/2000/svg" width="24"
                height="24" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round"
                aria-hidden="true" aria-label="Restart">
                  <polyline points="23 4 23 10 17 10"></polyline><polyline
                  points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9
                  9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49
                  15"></path>
                </svg></button>
          </tr>
          % end
        </table>
      </div>
    </div>
    <div class="modal fade" id="warningModal" tabindex="-1"
    aria-labelledby="warningModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5"
            id="warningModalLabel">Attention</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"
            aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>The performed action cannot be done. Maybe you have
            a permissions problem.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary"
            data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
    <script src="/js/bootstrap.bundle.min.js"></script>
    <script src="/js/sysdweb.js"></script>
  </body>
</html>
