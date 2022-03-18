Backup & Restore
****************

If you do no heavy modification of the code you should be fine with backing up :file:`/etc/ilmo/` and the database.
Assuming you used a PostgreSQL database the following solution might help you with backups and restores.

Backup
++++++

The following code is a modification of `this script <https://wiki.postgresql.org/wiki/Automated_Backup_on_Linux>`_
licensed under the :ref:`postgresql_license`.

You will first need to create a backup configuration at :file:`/var/ilmo/pg_backup.config`.

.. code-block::

    ##############################
    ## POSTGRESQL BACKUP CONFIG ##
    ##############################

    # Optional system user to run backups as.  If the user the script is running as doesn't match this
    # the script terminates.  Leave blank to skip check.
    BACKUP_USER=ilmo

    # Optional hostname to adhere to pg_hba policies.  Will default to "localhost" if none specified.
    HOSTNAME=localhost

    # Optional username to connect to database as.  Will default to "postgres" if none specified.
    USERNAME=ilmo

    # This dir will be created if it doesn't exist.  This must be writable by the user the script is
    # running as.
    BACKUP_DIR=/var/ilmo/backups/postgresql

    # Enter database to backup
    DATABSE=ilmo


    #### SETTINGS FOR ROTATED BACKUPS ####

    # Which day to take the weekly backup from (1-7 = Monday-Sunday)
    DAY_OF_WEEK_TO_KEEP=7

    # Number of days to keep daily backups
    DAYS_TO_KEEP=7

    # How many weeks to keep weekly backups
    WEEKS_TO_KEEP=5

    ######################################

And then add the script that will do the actual backup at :file:`/var/ilmo/backup_rotate.sh`

.. code-block:: bash

    #!/bin/bash

    ###########################
    ####### LOAD CONFIG #######
    ###########################

    while [ $# -gt 0 ]; do
            case $1 in
                    -c)
                            CONFIG_FILE_PATH="$2"
                            shift 2
                            ;;
                    *)
                            ${ECHO} "Unknown Option \"$1\"" 1>&2
                            exit 2
                            ;;
            esac
    done

    if [ -z $CONFIG_FILE_PATH ] ; then
            SCRIPTPATH=$(cd ${0%/*} && pwd -P)
            CONFIG_FILE_PATH="${SCRIPTPATH}/pg_backup.config"
    fi

    if [ ! -r ${CONFIG_FILE_PATH} ] ; then
            echo "Could not load config file from ${CONFIG_FILE_PATH}" 1>&2
            exit 1
    fi

    source "${CONFIG_FILE_PATH}"

    ###########################
    #### PRE-BACKUP CHECKS ####
    ###########################

    # Make sure we're running as the required backup user
    if [ "$BACKUP_USER" != "" -a "$(id -un)" != "$BACKUP_USER" ] ; then
            echo "This script must be run as $BACKUP_USER. Exiting." 1>&2
            exit 1
    fi


    ###########################
    ### INITIALISE DEFAULTS ###
    ###########################

    if [ ! $HOSTNAME ]; then
            HOSTNAME="localhost"
    fi;

    if [ ! $USERNAME ]; then
            USERNAME="postgres"
    fi;


    ###########################
    #### START THE BACKUPS ####
    ###########################

    function perform_backups()
    {
            SUFFIX=$1
            FINAL_BACKUP_DIR=$BACKUP_DIR"`date +\%Y-\%m-\%d`$SUFFIX/"

            echo "Making backup directory in $FINAL_BACKUP_DIR"

            if ! mkdir -p $FINAL_BACKUP_DIR; then
                    echo "Cannot create backup directory in $FINAL_BACKUP_DIR. Go and fix it!" 1>&2
                    exit 1;
            fi;

            #######################
            ### GLOBALS BACKUPS ###
            #######################

            echo -e "\n\nPerforming backup"
            echo -e "--------------------------------------------\n"

            echo "Backup"

            set -o pipefail
            if ! pg_dump $DATABASE | gzip > $FINAL_BACKUP_DIR"$DATABASE".sql.gz.in_progress; then
                    echo "[!!ERROR!!] Failed to produce globals backup" 1>&2
            else
                    mv $FINAL_BACKUP_DIR"$DATABASE".sql.gz.in_progress $FINAL_BACKUP_DIR"$DATABSE".sql.gz
            fi
            set +o pipefail

            echo -e "\nAll database backups complete!"
    }

    # MONTHLY BACKUPS

    DAY_OF_MONTH=`date +%d`

    if [ $DAY_OF_MONTH -eq 1 ];
    then
            # Delete all expired monthly directories
            find $BACKUP_DIR -maxdepth 1 -name "*-monthly" -exec rm -rf '{}' ';'

            perform_backups "-monthly"

            exit 0;
    fi

    # WEEKLY BACKUPS

    DAY_OF_WEEK=`date +%u` #1-7 (Monday-Sunday)
    EXPIRED_DAYS=`expr $((($WEEKS_TO_KEEP * 7) + 1))`

    if [ $DAY_OF_WEEK = $DAY_OF_WEEK_TO_KEEP ];
    then
            # Delete all expired weekly directories
            find $BACKUP_DIR -maxdepth 1 -mtime +$EXPIRED_DAYS -name "*-weekly" -exec rm -rf '{}' ';'

            perform_backups "-weekly"

            exit 0;
    fi

    # DAILY BACKUPS

    # Delete daily backups 7 days old or more
    find $BACKUP_DIR -maxdepth 1 -mtime +$DAYS_TO_KEEP -name "*-daily" -exec rm -rf '{}' ';'

    perform_backups "-daily"


You should make the script executable test it and automate the execution with :program:`crontab`

.. code-block:: bash

    $ chmod +x backup_rotate.sh
    $ ./backup_rotate.sh
    $ crontab -e
    # enter the following to backup every day at 3am
    0 3 * * * /var/ilmo/backup_rotate.sh



Restore
+++++++

If you for any reason want to restore a backup you can use the following:

.. code-block:: bash

    $ sudo systemctl stop ilmo-web
    $ pg_dump ilmo > ilmo_YYYY_MM_DD-hh_mm.psql # Make a backup for later analysis
    $ dropdb ilmo
    $ cd /path/to/backup
    $ gzip -d ilmo.sql.gz
    $ sudo -u postgres createdb -O ilmo ilmo
    $ psql ilmo < ilmo.sql
    $ systemctl restart ilmo-web