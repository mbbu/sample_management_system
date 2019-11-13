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

> [virtualenv tool](https://pypi.org/project/virtualenv/1.7.1.2/)

***3.Install the requirements***
```
 >> pip install -r requirements.txt
```

***4.Export required variables***
```
 >> export SAMPLE_MANAGEMENT_SYSTEM_DATABASE_URI='<<SQLAlchmeny Database URI set on your computer>>'
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
>Run it every time you want to add new requirements to the project requirements.txt file.
```
 >> pip freeze | grep -v "pkg-resources" > requirements.txt
```
:+1:
