# This is a list of all built-in libraries we currently have to offer.

Please note that all of these libraries are experimental and can break 

**dirlib**
Get directory, write/read files, and get environment variables

`getdir()` Get current working directory
`getenv(key)` Get environment variable
`read(name)` Read a file
`write(name, text)` Write to a file. Erases file before writing to it. Creates new one if it dosen't exist
`append(name, text)` Like `write` but appends to the file instead of erasing it. 

**jsonlib**
`jsonbuild(jsonstr)` Serialize dictionary or list into JSON
`jsonparse(jsonstr)` Deserialize JSON into dictionary or list

**random**
`randnum(a, b)` Random number from range a to b
`randchar()` Random character

**flasklib**
Note: Flasklib will store app information instead of giving you an object.
Based on Python Flask

`app(module="flasklib")` Create a app instance
`connect(func, route)` Connect a Function to a Route
`setup(userclass)` Setup app instance
`start(host="0.0.0.0", port=8080)` Start app instance.

These may cause undesired consequences if used incorrectly.
`abort(status)` Raise status code and run error method
`render_template(templatename)` Render Template
`url_for(urlname)` Return url for urlname

Very experimental:
`errorhandler(func, status)` Connect a Function to an error. Function runs on error.

**request**
Send get and post requests with python

`getmethod` Send a get request. Returns a dictionary
`postmethod` Send a post request. Returns a dictionary
`delmethod` Send a delete request. Returns a dictionary



**pakrat**
Run snippets of code as classes directly from your program. Requires internet connection.

`import(libname)` Gets the lib name from pakrat server then runs the parser and loads it into your program. **Can overwrite existing classes**