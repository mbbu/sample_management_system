# SAMPLE MANAGEMENT SYSTEM API #
This is a web based application that interfaces samples available at ICIPE and acts as an intermediate tool for data management and laboratory information management system for ICIPE.

## HOW TO RUN THE API ##
***1.Clone the repository and move into the project directory***

> While here, locally checkout a new branch and pull from origin develop to update the code.
```
>> git clone https://github.com/mbbu/sample_management_system.git
>> cd sample_management_system
```

***2.Create a virtual environment***
```
 ~> Using python3; 
    >> python3 -m venv <<name_of_virtual_environment>>

 ~> Using python2 install virtualenv tool (https://pypi.org/project/virtualenv/1.7.1.2/)
    >> virtualenv <<name_of_virtual_environment>>
```
> After your virtual environment is ready, activate it by running this command :point_down:
```
   >> source venv/bin/activate
```

> Read more about virtual environments :point_right: [virtualenv tool](https://pypi.org/project/virtualenv/1.7.1.2/)

***3.Install the requirements***
> Before you install the requirements ensure you have the following in your machine.
>>   1. postgres server for server-side application. [postgres](https://www.postgresql.org/download/) 
>>   2. libpq-dev for client-side application. [libpq-dev](https://pypi.org/project/libpq-dev/)

> If these are installed, run the command below to install the requirements for the application.
```
 >> pip install -r requirements.txt
```


***4.Export required variables***
```
 >> export SAMPLE_MANAGEMENT_SYSTEM_DATABASE_URI='<<postgresql://username:password@host:port/database>>'
 >> export SAMPLE_MANAGEMENT_SYSTEM_SECRET_KEY='<<random key generated locally (os.urandom(32) )>>'
 >> export FLASK_APP=api/
```

***5.Migrate the database***
```
 >> flask db upgrade
```

***6.Run the API***
```
 >> flask run
```

***7.Test the API using a REST client e.g. Postman***
```
 >> curl --url http://127.0.0.1:5000/welcome
```

---
---
***Adding new requirements to requirements.txt file***
> The command below help fix bug by ubuntu which gives pip wrong metadata on pkg-resources.
> Run it every time you want to add new requirements to the project requirements.txt file.
```
 >> pip freeze | grep -v "pkg-resources" > requirements.txt
```

***Update multiple packages in your virtual environment***
> In case you have many outdated packages in your environment, you can do multiple
> update by running this command.

```
 >> pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
```
:+1:
