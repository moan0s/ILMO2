# Migration

This tries to provide instructions for a migration from the legacy ILMO to ILMO2.x.
The migration will most likely need manual work from you. Do not expect a streamlined migration, but some useful help.
Following are general instructions that need to be adapted to your special case.

# Gather data

To migrate, you need to export the data of the current ILMO instance from your databse. You will need the tables `TABLE_USER`, 
`TABLE_BOOKS`, `TABLE_MATERIAL` and `TABLE_LOAN` as defined in your config.
Preferably download/convert them to JSON files, one file per table.

# Run migration script

The migration script needs the Django settings e.g. for database access.

```shell
cd legacy_migration
../src/manage.py shell < migrate_legacy.py
```

# Verify

Verify that the imported data is correct. Be aware that passwords for the user have been randomly generated
and all users need to reset their password.

# Limitations

The migration tool does not

* equip user with privileges (admins)
* migrate opening hours
* create languages -> must be created beforehand