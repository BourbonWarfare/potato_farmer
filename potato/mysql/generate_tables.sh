echo "---------------------------------------"
for i in {1..120}; do
    echo "exit" | mysql --host db --port 3306 --user root > /dev/null 2>&1
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "Generating tables..."
        mysql --host db --port 3306 --user root < /var/lib/mysql/gen_tables.sql
        if [ $? -eq 0 ]; then
            echo "Sucessfully generated tables"
            exit 0
        fi
        echo "Failed to generate tables!"
        exit 1
    fi
    sleep 1
done
echo "Failed to connect to DB!"
exit 1
