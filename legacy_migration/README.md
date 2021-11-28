# Migration

This tries to provide instructions for a migration from the legacy ILMO to ILMO2.x.
The migration will most likely need manual work from you. Do not expect a streamlined migration, but some useful help.
Following are general instructions that need to be adapted to your special case.

# Gather data

To migrate, you need to export the data of the current ILMO instance from your database. You will need the tables `TABLE_USER`, 
`TABLE_BOOKS`, `TABLE_MATERIAL` and `TABLE_LOAN` as defined in your config.
Preferably download/convert them to JSON files, one file per table.

# Backup

Backup your data before running the script. Make sure that you are able to roll back, as the script can mess up your data.

# Run migration script

The migration script needs the Django settings e.g. for database access.

```shell
cd src
python manage.py shell < ../legacy_migration/migrate_legacy.py
```

# Verify

Verify that the imported data is correct. Be aware that passwords for the user have been randomly generated
and all users need to reset their password.

# Limitations

The migration tool does not

* equip user with privileges (admins)
* migrate opening hours
* create languages -> must be created beforehand