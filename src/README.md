# Prequesits

* Install python and pip
* Install and configure database (examples with mysql)
	+ Create user e.g. ilmo
	+ Create database `CREATE DATABASE ilmo;`
	+ Grant privileges `GRANT ALL PRIVILEGES ON `%ilmo%` .  * TO 'ilmo'@'%';` to also allow creation of test database.
* Install dependencies `sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`
* Create `src/.env` and fill
```
SECRET_KEY = '<your-secret>'
DEBUG=True
DATABASE_NAME=ilmo
DATABASE_USER=ilmo
DATABASE_PASSWORD=<your_db_password>
DATABASE_HOST=127.0.0.1
```

# Acknowledgment

Thanks to the amazing Django community that provides an awesome documentation and to the [MDN Web Docs](https://github.com/mdn/django-locallibrary-tutorial) that provided a very similar project where I got many ideas and quite some code from. CC-0 is an amazing license, thanks for using it.
