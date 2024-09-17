Backend Developer Technical Test

This is a project to test your web development knowledge using Django and Python.
Feel free to use any third-party libraries to achieve the final goal. Treat this as a
real project was assigned to you at work and not an interview test.

Write a Django application that performs the following:

1. Upload a file, save it in your local system and perform the following tests:
   a. Only accept csv and text files
   b. File size should not exceed 10mb,
   You will find in the attachments, a file named 'schema' for pre-defined schemas. If a file
   has a similar schema:

2. Save the file content as a table to a mysql database.
   Otherwise
3. Save the file data to a nosql database: mongodb.
4. Retrieve all the files that the user uploaded.
5. Retrieve the file content requested by the user.
6. Give the user the possibility to modify the content of the file.

Bonus: The user can modify the column names of this files

- The user can upload multiple files.
- The user should not modify the original column names. Hint: create a table that contains
  the mapping of the original column names to the changed column names.

You'll need the following libraries:

- pymysql for MySQL
- pymongo for MongoDB
- pandas for handling CSV files

Key points to consider:

- The implementation uses Django models to store file information and metadata.
- It leverages pandas for CSV parsing and JSON serialization.
- The application separates concerns between file upload, storage, retrieval, and modification.
- Security considerations like file size limits and content type checks are implemented.
- The bonus feature of changing column names is implemented using a separate model and view.
