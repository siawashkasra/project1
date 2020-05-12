<h1>Reviewer</h1>

<p>A robust book rating and reviewing application
You can access almost 5000 books, see their Goodreads rating and provide your own review and rating as well.</p>


<h2>File Structure</h2>
<p>This application has been built in Flask, therefore there are three main files:</p> 

<p><b>application.py:</b> it contains the actual app and all the routes.</p>
<p><b>controller.py:</b> it is a custom file which contains the codes for database interactions and utility functions.</p>
<p><b>forms.py:</b> it contains all the forms created through Flask-WTF package.</p>
<p>Apart from the above there are following folders for this applications:</p>
<p><b>data:</b> this folder consists of a book.csv file which has the data for 5000 books in csv format and an impory.py file which reads the data from book.csv file and insert it into database.</p>
<p><b>migrations:</b> this folder consists of a queries.sql file which contains the schema for all the necessary database tables and a schema.py file which reads the queries.sql and creates the necessary tables in the database.</p>
<p><b>setup:</b> this folder consists of a .env and config.py files which consists of the Flask environment variables, there is also a requirements.txt file, which contains the necessary python modules to be installed for this application.</p>
<p><b>static:</b> this folder contains all the css, javascript and images folders and files.</p>
<p><b>templates:</b> this folder consists of all the templates and layouts for this application.</p>


<h2>Set up</h2>

<p>Make sure Python3 and its dependencies are installed, navigate into setup directory and run.</p>
<pre>$ sudo pip3 install requirements.txt</pre>
<p>Export the DATABASE_URL.</p>
<pre>$ export DATABASE_URL="postgres://kidsgevwmzrtwx:63a8ae2a9b7785cac7bbe07705db6efd1d8a1e517b2de8c8285cbbf8974a6bf5@ec2-52-202-22-140.compute-1.amazonaws.com:5432/d9g09asmej8sb2"
</pre>
<p>Navigate to migrations directory, run.</p>
<pre>$ python3 schema.py</pre>
<p>Export the environment variables from the .env file and run.</p>
<pre>$ export FLASK_APP=application.py</pre>
<pre>$ export FLASK_ENV=production</pre>
<p>Finally run the following to start the server.<p>
<pre>$ flask run</pre>