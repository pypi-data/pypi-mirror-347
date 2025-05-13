# ckanext-pycharm-debugger


CKAN extension that provides PyCharm remote debugger session attachment


Based off the good work of https://github.com/NaturalHistoryMuseum/ckanext-dev/ which is now archived 6 years ago.


**Not affiliated with JetBrains.**

Pycharm is a trademark of JetBrains s.r.o.<br/>
This project is not affiliated with, endorsed by, or sponsored by JetBrains.<br/>
The trademark is used here only to describe the tool this extension integrates with, in accordance with fair use.<br/>
This project is licensed under the terms of the


Setup
------

To enable the remote debugger session, you need:

1. Install the pydevd-pycharm.egg package on the remote machine (this file is part of the PyCharm
  distribution, see https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html)
  
  or 
  
  ```bash pip install ckanext-python-debugger['PyCharm2025.1.1']'```

  or 
 
  ```bash pip install ckanext-python-debugger['PyCharm2024.1.4']'```
 
  or
 
  ```bash pip install pydevd-pycharm ~= ##What your pycharm pro ide suggests##'```


2. Add the line 'debug.remote = True' to your configuration file (this is independent of Ckan's
  debug setting ; both can be enabled or disabled separately) ;


3. Add the plugin ``ckan.plugins = ... pycharm_debugger`` to your configuration file.


4. Setup a Remote Debugger within PyCharm, using port 5678 (or as defined by debug.host.port).

You may optionally define:
- ``debug.remote.host.ip`` for the host IP (defaults to host.docker.internal which is the default host when using Docker) ;
- ``debug.remote.host.port`` for the host port (defaults to 5678; it needs to match the setting in PyCharm) ;
- ``debug.remote.stdout_to_server`` to send stdout to the debugging host (defaults to True) ;
- ``debug.remote.stderr_to_server`` to send stderr to the debugging host (defaults to True) ;
- ``debug.remote.suspend`` defines whether the debugger should break as soon as it is started (defaults to True).

5. Ensure that pycharm remote debugging server is running on port `5678` (default) '

6. Start CKAN
```bash
  cd test-infrasturcture
  docker compose exec ckan  ckan -c ckan.ini run -H 0.0.0.0
```

7. If you wish to use in pytest, place the following above your test class
```python
  @pytest.mark.ckan_config(u'ckan.plugins', u'pycharm_debugger')
  @pytest.mark.ckan_config(u'debug.remote', u'True')
```


## Requirements

Compatibility with core CKAN versions:

  | CKAN version | Compatibility                           |
  |--------------|-----------------------------------------|
  | 2.7          | untested                                |
  | 2.8          | untested                                |
  | 2.9          | untested                                |
  | 2.10         | yes                                     |
  | 2.11         | yes                                     |
  | master       | yes as of 2025/05 (check test results)  |


## License

**Not affiliated with JetBrains.**

Pycharm is a trademark of JetBrains s.r.o.<br/>
This project is not affiliated with, endorsed by, or sponsored by JetBrains.<br/>
The trademark is used here only to describe the tool this extension integrates with, in accordance with fair use.<br/>
This project is licensed under the terms of the

**GNU Affero General Public License v3.0 (AGPL-3.0)**

See the LICENSE file for full details.